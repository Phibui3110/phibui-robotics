import cv2
import numpy as np
import os

# ==========================================
# THÔNG SỐ CẤU HÌNH (GLOBAL VARIABLES)
# ==========================================

# Kích thước ảnh chạy realtime (Width, Height)
RUN_TIME_SIZE = (640, 360)

# --- SRC_POINTS ---
# 4 góc của checkerboard trên ảnh đã undistort + resize về RUN_TIME_SIZE
# Thứ tự BẮT BUỘC: Trái-Dưới, Phải-Dưới, Phải-Trên, Trái-Trên
# !! Chạy pick_points.py để lấy lại tọa độ này sau khi sửa undistort_frame !!
SRC_POINTS = np.float32([[87, 354], [553, 349], [433, 205], [207, 205]])

# --- DST_POINTS ---
# Tọa độ đích phải giữ ĐÚNG TỶ LỆ kích thước thực của checkerboard.
#
# Ví dụ board 8x5 ô, mỗi ô 3cm  →  24cm (ngang) x 15cm (dọc)
# Tỷ lệ ngang:dọc = 24:15 = 1.6
#
# Chọn chiều rộng dst = 320px  →  chiều cao dst = 320 / 1.6 = 200px
# Căn giữa theo chiều ngang của khung 640px: x_start = (640-320)/2 = 160
# Căn dưới theo chiều dọc  của khung 360px: y_bottom = 360, y_top = 360-200 = 160
#
# !! Nếu board của bạn khác kích thước, hãy tính lại theo công thức trên !!
_BEV_LEFT   = 160
_BEV_RIGHT  = 480   # rộng 320px
_BEV_BOTTOM = 360
_BEV_TOP    = 160   # cao  200px  (tỷ lệ 24:15)

DST_POINTS = np.float32([
    [_BEV_LEFT,  _BEV_BOTTOM],  # Trái  - Dưới
    [_BEV_RIGHT, _BEV_BOTTOM],  # Phải  - Dưới
    [_BEV_RIGHT, _BEV_TOP   ],  # Phải  - Trên
    [_BEV_LEFT,  _BEV_TOP   ],  # Trái  - Trên
])


# ==========================================
# PERCEPTION MODULE
# ==========================================
class PerceptionModule:
    def __init__(self, camera_matrix_file='camera_calib.npz'):
        """
        Khởi tạo module:
          1. Load intrinsic calibration (K, dist).
          2. Tính sẵn ma trận BEV (M) và nghịch đảo (M_inv).
        """
        self.camera_matrix  = None
        self.dist_coeffs    = None
        self.new_camera_mtx = None   # Ma trận camera tối ưu (tính 1 lần)
        self._calib_src_size = None  # Kích thước ảnh lúc calib (để cache)

        # 1. Load Calibration
        if os.path.exists(camera_matrix_file):
            with np.load(camera_matrix_file) as data:
                self.camera_matrix = data['mtx']
                self.dist_coeffs   = data['dist']
            print(f"[INFO] Đã load Camera Calibration từ '{camera_matrix_file}'.")
        else:
            print("[WARNING] Không tìm thấy file calib. Ảnh sẽ KHÔNG được nắn thẳng!")

        # 2. Tính sẵn ma trận BEV
        self.M     = cv2.getPerspectiveTransform(SRC_POINTS, DST_POINTS)
        self.M_inv = cv2.getPerspectiveTransform(DST_POINTS, SRC_POINTS)
        print("[INFO] Đã tính sẵn ma trận BEV (M) và nghịch đảo (M_inv).")

    # ------------------------------------------------------------------
    # TÁC VỤ 1: UNDISTORT
    # ------------------------------------------------------------------
    def undistort_frame(self, frame):
        """
        Nắn thẳng ảnh fisheye/wide-angle.

        FIX so với phiên bản cũ:
          - KHÔNG crop ROI sau undistort.
          - Cache new_camera_mtx để tránh tính lại mỗi frame (tốc độ tốt hơn).
          - Trả về ảnh cùng kích thước với đầu vào → resize về RUN_TIME_SIZE
            ở bước sau sẽ KHÔNG bị stretch.
        """
        if self.camera_matrix is None:
            return frame

        h, w = frame.shape[:2]

        # Chỉ tính new_camera_mtx 1 lần cho kích thước ảnh này
        if self.new_camera_mtx is None or self._calib_src_size != (w, h):
            self.new_camera_mtx, _ = cv2.getOptimalNewCameraMatrix(
                self.camera_matrix, self.dist_coeffs, (w, h), alpha=0, newImgSize=(w, h)
            )
            # alpha=0: cắt sạch viền đen, giữ nguyên kích thước (w, h)
            self._calib_src_size = (w, h)

        undistorted = cv2.undistort(
            frame,
            self.camera_matrix,
            self.dist_coeffs,
            None,
            self.new_camera_mtx
        )
        return undistorted   # Kích thước vẫn là (w, h) — KHÔNG crop

    # ------------------------------------------------------------------
    # TÁC VỤ 2: ROI MASKING
    # ------------------------------------------------------------------
    def process_roi(self, frame):
        """
        Xóa (tô đen) vùng phía trên không liên quan (bầu trời, tường...).

        FIX so với phiên bản cũ:
          - Tự động tính ngưỡng Y từ SRC_POINTS thay vì hardcode y=180.
          - Thêm buffer để không cắt mất cạnh trên của checkerboard.
        """
        # Y nhỏ nhất trong SRC_POINTS = hàng cao nhất của vùng quan tâm
        top_y = int(np.min(SRC_POINTS[:, 1])) - 15  # buffer 15px
        top_y = max(0, top_y)                        # tránh âm

        masked = frame.copy()
        masked[0:top_y, :] = 0
        return masked

    # ------------------------------------------------------------------
    # TÁC VỤ 3: BIRD'S EYE VIEW
    # ------------------------------------------------------------------
    def get_bird_eye_view(self, frame):
        """
        Biến đổi perspective → góc nhìn từ trên xuống (BEV).
        Ma trận M đã được tính sẵn trong __init__ để tiết kiệm CPU.
        """
        bev = cv2.warpPerspective(
            frame, self.M, RUN_TIME_SIZE,
            flags=cv2.INTER_LINEAR
        )
        return bev

    # ------------------------------------------------------------------
    # TIỆN ÍCH: Chiếu điểm / đường từ BEV về ảnh gốc
    # ------------------------------------------------------------------
    def bev_to_original(self, points_bev):
        """
        Chiếu ngược tọa độ từ không gian BEV về ảnh gốc (dùng M_inv).

        Args:
            points_bev: np.array shape (N, 2), dtype float32

        Returns:
            np.array shape (N, 2) tọa độ trên ảnh gốc (sau undistort+resize)
        """
        pts = points_bev.reshape(-1, 1, 2).astype(np.float32)
        pts_orig = cv2.perspectiveTransform(pts, self.M_inv)
        return pts_orig.reshape(-1, 2)

    # ------------------------------------------------------------------
    # PIPELINE ĐẦY ĐỦ (tiện gọi 1 lần)
    # ------------------------------------------------------------------
    def full_pipeline(self, raw_frame):
        """
        Chạy toàn bộ pipeline: Undistort → Resize → ROI → BEV.

        Returns:
            img_roi (np.array): Ảnh sau undistort + masking (cùng RUN_TIME_SIZE)
            img_bev (np.array): Ảnh BEV (cùng RUN_TIME_SIZE)
        """
        # Bước 1: Nắn thẳng (giữ nguyên kích thước gốc)
        img_undist = self.undistort_frame(raw_frame)

        # Bước 2: Resize về kích thước chạy thực tế
        img_resized = cv2.resize(img_undist, RUN_TIME_SIZE)

        # Bước 3: Masking ROI (tô đen vùng không liên quan)
        img_roi = self.process_roi(img_resized)

        # Bước 4: Biến đổi BEV
        img_bev = self.get_bird_eye_view(img_roi)

        return img_roi, img_bev


# ==========================================
# KHỐI LỆNH TEST MODULE
# ==========================================
if __name__ == "__main__":
    vision = PerceptionModule('camera_calib.npz')

    img_bgr = cv2.imread('bev_ref.jpg')
    if img_bgr is None:
        print("[ERROR] Không tìm thấy file 'bev_ref.jpg'!")
        exit(1)

    img_roi, img_bev = vision.full_pipeline(img_bgr)

    # Vẽ SRC_POINTS lên ảnh ROI để kiểm tra điểm đã chọn có đúng không
    debug_roi = img_roi.copy()
    labels = ["1:TL-Duoi", "2:Phai-Duoi", "3:Phai-Tren", "4:Trai-Tren"]
    for i, (x, y) in enumerate(SRC_POINTS):
        cv2.circle(debug_roi, (int(x), int(y)), 6, (0, 0, 255), -1)
        cv2.putText(debug_roi, labels[i], (int(x)+8, int(y)-8),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)
    pts = SRC_POINTS.astype(np.int32).reshape((-1, 1, 2))
    cv2.polylines(debug_roi, [pts], isClosed=True, color=(255, 0, 0), thickness=2)

    # Vẽ DST_POINTS lên ảnh BEV để kiểm tra vùng đích
    debug_bev = img_bev.copy()
    for i, (x, y) in enumerate(DST_POINTS):
        cv2.circle(debug_bev, (int(x), int(y)), 6, (0, 0, 255), -1)
    dst_pts = DST_POINTS.astype(np.int32).reshape((-1, 1, 2))
    cv2.polylines(debug_bev, [dst_pts], isClosed=True, color=(0, 255, 255), thickness=2)

    cv2.imwrite('result_1_roi.jpg',   img_roi)
    cv2.imwrite('result_2_bev.jpg',   img_bev)
    cv2.imwrite('debug_1_roi.jpg',    debug_roi)
    cv2.imwrite('debug_2_bev.jpg',    debug_bev)

    print("[INFO] Đã xuất 4 file:")
    print("       result_1_roi.jpg  — ROI sau undistort")
    print("       result_2_bev.jpg  — Bird's Eye View")
    print("       debug_1_roi.jpg   — ROI + SRC_POINTS (kiểm tra điểm click)")
    print("       debug_2_bev.jpg   — BEV  + DST_POINTS (kiểm tra vùng đích)")
    print()
    print("[TIPS] Nếu BEV các ô vuông chưa đều:")
    print("       1. Chạy lại pick_points.py để lấy SRC_POINTS mới.")
    print("       2. Kiểm tra tỷ lệ DST_POINTS có khớp kích thước board thực không.")