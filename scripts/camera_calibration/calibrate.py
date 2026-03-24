import cv2
import numpy as np
import glob
import os

# --- GLOBAL SETTINGS ---
# Số lượng ĐIỂM GIAO CẮT bên trong bàn cờ (Ngang, Dọc)
CHESSBOARD_CORNERS = (9, 6) 

# Kích thước thực tế của 1 ô vuông (đơn vị: mét). 3cm = 0.03m
SQUARE_SIZE = 0.03 

class PerceptionModule:
    def __init__(self, camera_matrix_file='camera_calib.npz'):
        self.camera_matrix = None
        self.dist_coeffs = None
        self.calib_file = camera_matrix_file
        
        if os.path.exists(self.calib_file):
            self.load_calibration()

    def calibrate_camera(self, images_folder):
        """
        Đọc ảnh gốc, tìm điểm giao cắt, hiển thị trực quan và tính ma trận camera.
        """
        print(f"[INFO] Bắt đầu quá trình Camera Calibration từ thư mục: {images_folder}")
        
        # Tiêu chí dừng cho thuật toán tinh chỉnh tọa độ điểm ảnh sub-pixel
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        # Chuẩn bị tọa độ các điểm 3D trong không gian thực (Z = 0)
        objp = np.zeros((CHESSBOARD_CORNERS[0] * CHESSBOARD_CORNERS[1], 3), np.float32)
        objp[:, :2] = np.mgrid[0:CHESSBOARD_CORNERS[0], 0:CHESSBOARD_CORNERS[1]].T.reshape(-1, 2)
        objp = objp * SQUARE_SIZE

        objpoints = [] # Lưu điểm 3D trong không gian thực
        imgpoints = [] # Lưu điểm 2D trên mặt phẳng ảnh

        # Lấy danh sách tất cả ảnh jpg
        images = glob.glob(f'{images_folder}/*.jpg')
        if not images:
            print("[ERROR] Không tìm thấy ảnh. Vui lòng kiểm tra lại đường dẫn!")
            return False

        # Biến lưu kích thước ảnh tự động
        frame_size = None

        for fname in images:
            img = cv2.imread(fname)
            if img is None:
                continue
                
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            # Tự động cập nhật kích thước từ ảnh đọc được (Width, Height)
            if frame_size is None:
                frame_size = gray.shape[::-1]

            # Tìm các điểm giao cắt
            ret, corners = cv2.findChessboardCorners(gray, CHESSBOARD_CORNERS, None)

            if ret == True:
                objpoints.append(objp)
                
                # Tinh chỉnh độ chính xác của các điểm tìm được
                corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
                imgpoints.append(corners2)
                
                # --- VISUALIZATION: Vẽ và hiển thị kết quả ---
                # Thu nhỏ ảnh lại một chút để hiển thị vừa màn hình laptop
                display_img = img.copy()
                cv2.drawChessboardCorners(display_img, CHESSBOARD_CORNERS, corners2, ret)
                display_img = cv2.resize(display_img, (960, 540)) 
                
                cv2.imshow('Camera Calibration - Dang tim diem...', display_img)
                cv2.waitKey(500) # Dừng 0.5 giây để bạn kịp nhìn, có thể đổi thành 1 để bấm phím qua ảnh
            else:
                print(f"[WARNING] Bỏ qua ảnh {fname} vì không nhận diện đủ {CHESSBOARD_CORNERS} điểm.")

        cv2.destroyAllWindows()

        if len(objpoints) == 0:
            print("[ERROR] Không tìm thấy bàn cờ trong bất kỳ ảnh nào. Hãy kiểm tra lại CHESSBOARD_CORNERS.")
            return False

        print(f"[INFO] Đã trích xuất thành công dữ liệu từ {len(objpoints)}/{len(images)} bức ảnh.")
        print(f"[INFO] Đang giải hệ phương trình tính ma trận với kích thước ảnh: {frame_size}...")
        
        # Tính toán ma trận
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame_size, None, None)

        self.camera_matrix = mtx
        self.dist_coeffs = dist

        # Lưu thông số
        np.savez(self.calib_file, mtx=mtx, dist=dist)
        print(f"[INFO] Calibration thành công xuất sắc. Đã lưu thông số tại: {self.calib_file}")
        
        return True

    def load_calibration(self):
        """Tải thông số calib từ file."""
        with np.load(self.calib_file) as data:
            self.camera_matrix = data['mtx']
            self.dist_coeffs = data['dist']
        print(f"[INFO] Đã tải thông số Camera Calibration từ {self.calib_file}.")

    def undistort_frame(self, frame):
        """Nắn thẳng ảnh dựa trên ma trận (Tự động thích ứng mọi độ phân giải)."""
        if self.camera_matrix is None or self.dist_coeffs is None:
            return frame
        
        h, w = frame.shape[:2]
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.dist_coeffs, (w,h), 1, (w,h))
        
        # Nắn thẳng
        undistorted_img = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs, None, new_camera_mtx)
        
        # Cắt bỏ phần viền đen bị kéo giãn
        x, y, crop_w, crop_h = roi
        undistorted_img = undistorted_img[y:y+crop_h, x:x+crop_w]
        
        return undistorted_img

# ==========================================
# KHỐI LỆNH CHẠY THỬ NGHIỆM
# ==========================================
if __name__ == "__main__":
    # Khởi tạo module
    vision = PerceptionModule()

    # 1. Chạy quá trình lấy mẫu và tính toán (Thư mục của bạn tên là 'calibration_image')
    success = vision.calibrate_camera('calibration_image')

    # 2. Test thử việc khử méo trên bức ảnh đầu tiên
    if success:
        # Lấy thử 1 file ảnh bất kỳ trong thư mục để test
        test_images = glob.glob('calibration_image/*.jpg')
        if test_images:
            test_img = cv2.imread(test_images[0])
            
            print("[INFO] Đang áp dụng khử méo (Undistort) cho ảnh test...")
            fixed_img = vision.undistort_frame(test_img)
            
            cv2.imwrite('test_original.jpg', test_img)
            cv2.imwrite('test_undistorted.jpg', fixed_img)
            
            print("[INFO] HOÀN TẤT! Hãy mở 2 file 'test_original.jpg' và 'test_undistorted.jpg' để so sánh.")