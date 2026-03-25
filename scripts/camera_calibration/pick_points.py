import cv2
import numpy as np
from calibrate import PerceptionModule

# --- CẤU HÌNH ĐỘ PHÂN GIẢI CHẠY ROS 2 THỰC TẾ ---
# RPi 5 rất mạnh, nhưng để xử lý realtime 15-20fps cho xe tự lái, 
# 640x360 (tỷ lệ 16:9) là một con số "vàng". 
RUN_TIME_SIZE = (640, 360)

# 1. Khởi tạo module (nó sẽ tự load file camera_calib.npz)
print("[INFO] Đang load thông số Calibration...")
vision = PerceptionModule('camera_calib.npz')

# 2. Đọc ảnh hệ quy chiếu
img = cv2.imread('bev_ref.jpg')
if img is None:
    print("[ERROR] Không tìm thấy file bev_ref.jpg. Hãy kiểm tra lại tên file!")
    exit()

# 3. Khử méo ảnh trước khi chọn điểm
print("[INFO] Đang nắn thẳng ảnh...")
img_undistorted = vision.undistort_frame(img)

# 4. Resize về kích thước chạy thực tế để lấy tọa độ cho chuẩn
img_resized = cv2.resize(img_undistorted, RUN_TIME_SIZE)

# Danh sách lưu tọa độ
points = []

def click_event(event, x, y, flags, params):
    global points
    # Bắt sự kiện click chuột trái
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(points) < 4:
            points.append([x, y])
            
            # Vẽ 1 dấu chấm đỏ tại nơi vừa click
            cv2.circle(img_resized, (x, y), 5, (0, 0, 255), -1)
            # Viết số thứ tự điểm
            cv2.putText(img_resized, str(len(points)), (x+10, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.imshow('Interactive Picker', img_resized)

            # Nếu đã click đủ 4 điểm
            if len(points) == 4:
                # Vẽ hình thang nối 4 điểm lại
                pts_array = np.array(points, np.int32)
                cv2.polylines(img_resized, [pts_array], True, (255, 0, 0), 2)
                cv2.imshow('Interactive Picker', img_resized)
                
                print("\n" + "="*50)
                print("🎉 ĐÃ LẤY ĐỦ 4 TỌA ĐỘ (SOURCE POINTS) 🎉")
                print("Hãy copy y nguyên dòng code mảng numpy bên dưới gửi cho tui:")
                print(f"SRC_POINTS = np.float32({points})")
                print("="*50 + "\n")
                print("[INFO] Bấm phím bất kỳ trên cửa sổ ảnh để thoát...")

print("[INFO] Hãy click vào 4 góc của bàn cờ theo đúng thứ tự...")
cv2.imshow('Interactive Picker', img_resized)
cv2.setMouseCallback('Interactive Picker', click_event)
cv2.waitKey(0)
cv2.destroyAllWindows()