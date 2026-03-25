import cv2
import numpy as np
import os

# ==========================================
# THÔNG SỐ CẤU HÌNH (GLOBAL VARIABLES)
# ==========================================
# Kích thước ảnh chạy realtime trên RPi 5
RUN_TIME_SIZE = (640, 360) 

# Tọa độ 4 điểm góc nhìn thực tế (Bạn vừa click)
# Thứ tự: Trái-Dưới, Phải-Dưới, Phải-Trên, Trái-Trên
SRC_POINTS = np.float32([
    [98, 353],   # Điểm 1: Trái - Dưới
    [551, 349],  # Điểm 2: Phải - Dưới
    [432, 207],  # Điểm 3: Phải - Trên
    [212, 204]   # Điểm 4: Trái - Trên
])

# Tọa độ đích (Hình chữ nhật nhìn từ trên trời xuống)
# Tui set chiều rộng làn đường bằng 1/2 khung hình (từ x=160 đến x=480)
DST_POINTS = np.float32([
    [160, RUN_TIME_SIZE[1]],  # Trái - Dưới
    [480, RUN_TIME_SIZE[1]],  # Phải - Dưới
    [480, 0],                 # Phải - Trên
    [160, 0]                  # Trái - Trên
])

class PerceptionModule:
    def __init__(self, camera_matrix_file='camera_calib.npz'):
        """Khởi tạo module, load file calib và tính toán sẵn ma trận BEV."""
        self.camera_matrix = None
        self.dist_coeffs = None
        
        # 1. Load Calibration
        if os.path.exists(camera_matrix_file):
            with np.load(camera_matrix_file) as data:
                self.camera_matrix = data['mtx']
                self.dist_coeffs = data['dist']
            print("[INFO] Đã load file Calibration thành công.")
        else:
            print("[WARNING] Không tìm thấy file calib. Ảnh sẽ không được nắn thẳng!")

        # 2. Tính toán sẵn ma trận biến đổi BEV (Để RPi không phải tính lại mỗi frame)
        self.M = cv2.getPerspectiveTransform(SRC_POINTS, DST_POINTS)
        self.M_inv = cv2.getPerspectiveTransform(DST_POINTS, SRC_POINTS) # Dùng để vẽ line ngược lại ảnh gốc

    def undistort_frame(self, frame):
        """Tác vụ 1: Nắn thẳng ảnh"""
        if self.camera_matrix is None:
            return frame
        
        h, w = frame.shape[:2]
        new_camera_mtx, roi = cv2.getOptimalNewCameraMatrix(self.camera_matrix, self.dist_coeffs, (w,h), 1, (w,h))
        undistorted = cv2.undistort(frame, self.camera_matrix, self.dist_coeffs, None, new_camera_mtx)
        x, y, crop_w, crop_h = roi
        return undistorted[y:y+crop_h, x:x+crop_w]

    def process_roi(self, frame):
        """
        Tác vụ 2: Region of Interest.
        Lưu ý: Không dùng hàm Crop (cắt ảnh) vì sẽ làm sai lệch tọa độ Y của BEV.
        Giải pháp tốt nhất là tô đen (masking) vùng từ điểm cao nhất (Y=200) trở lên.
        """
        masked_frame = np.copy(frame)
        # Điểm cao nhất của hình thang là ~200. Xóa mọi thứ từ dòng 180 trở lên đỉnh.
        masked_frame[0:180, :] = 0 
        return masked_frame

    def get_bird_eye_view(self, frame):
        """Tác vụ 3: Đổi góc nhìn từ trên xuống (BEV)"""
        # Áp dụng ma trận M vào ảnh
        bev_img = cv2.warpPerspective(frame, self.M, RUN_TIME_SIZE, flags=cv2.INTER_LINEAR)
        return bev_img

# ==========================================
# KHỐI LỆNH TEST MODULE
# ==========================================
if __name__ == "__main__":
    vision = PerceptionModule('camera_calib.npz')
    
    # 1. Đọc ảnh gốc (thay bằng tên file ảnh thực tế của bạn nếu cần)
    img_bgr = cv2.imread('bev_ref.jpg')
    if img_bgr is not None:
        # Bước 1: Khử méo
        img_undist = vision.undistort_frame(img_bgr)
        # Ép về kích thước chuẩn
        img_resized = cv2.resize(img_undist, RUN_TIME_SIZE) 
        
        # Bước 2: Lọc vùng quan tâm (Xóa bầu trời)
        img_roi = vision.process_roi(img_resized)
        
        # Bước 3: Biến đổi góc nhìn chim bay
        img_bev = vision.get_bird_eye_view(img_roi)
        
        # Lưu kết quả để xem
        cv2.imwrite('result_1_roi.jpg', img_roi)
        cv2.imwrite('result_2_bev.jpg', img_bev)
        
        print("[INFO] Đã xuất 2 file: result_1_roi.jpg và result_2_bev.jpg. Hãy mở lên để xem điều kỳ diệu!")
