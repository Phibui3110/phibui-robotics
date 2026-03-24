Lộ trình 6 tuần cho đồ án xe tự lái
===================================

Tác giả: Bùi Nhật Phi  
Định hướng: Research-oriented development  
Mốc hoàn thành: 30/04/2026  

Tổng quan
---------

Tài liệu này mô tả lộ trình phát triển trong 6 tuần để xây dựng hệ thống xe tự lái hoàn chỉnh:

    Perception → State Estimation → Planning → NMPC Control → Vehicle

Mục tiêu chính:

    Xây dựng hệ thống end-to-end hoạt động:
    Camera → Lane Detection → Trajectory → NMPC → Xe thực

Nguyên tắc cốt lõi
------------------

- Sử dụng **computer vision truyền thống (không deep learning)**
- Tập trung vào **trajectory generation (planning)**
- NMPC chỉ dùng để **bám quỹ đạo (tracking)**
- Tránh over-engineering giai đoạn đầu (SLAM, VO)

Kiến trúc hệ thống
------------------

::

    Camera + IMU
         ↓
    [Perception]
         ↓
    [State Estimation]
         ↓
    [Local Planning]  ← PHẦN QUAN TRỌNG NHẤT
         ↓
    [NMPC Controller]
         ↓
    Actuators (servo + motor)

.. toctree::
   :maxdepth: 1
   :caption: Chi tiết từng tuần

   week1
   week2
   week3
   week4
   week5
   week6


.. _week1:

Tuần 1: Calibration camera & Bird-eye view
------------------------------------------

Mục tiêu
~~~~~~~~
- Tạo được ảnh nhìn từ trên xuống (bird-eye view)
- Loại bỏ méo ảnh (distortion)

Deliverables
~~~~~~~~~~~~
- Tham số calibration camera
- Pipeline undistort
- Perspective transform hoạt động
- ROS2 camera node

Công việc
~~~~~~~~~
- Chụp ~20 ảnh checkerboard
- Dùng OpenCV:

  - ``cv2.calibrateCamera``
  - Lưu camera matrix và distortion coefficients

- Implement undistort
- Xác định ROI (4 điểm)
- Warp perspective:

  ::

      M = cv2.getPerspectiveTransform(src, dst)

- Tích hợp ROS2
- Visualize bằng RViz2

Lưu ý
~~~~~
- Sai perspective → lane bị cong
- Không xử lý distortion → lỗi dây chuyền về sau

---

.. _week2:

Tuần 2: Lane Detection
----------------------

Mục tiêu
~~~~~~~~
- Detect lane ổn định ~80%

Deliverables
~~~~~~~~~~~~
- Binary lane mask
- Tách được left/right lane

Pipeline
~~~~~~~~

::

    Image
    → Grayscale
    → Gaussian Blur
    → Canny Edge
    → Threshold (white)
    → Combine

Công việc
~~~~~~~~~
- Tune threshold
- Morphology (erode/dilate)
- Implement sliding window:

  - Histogram phần dưới ảnh
  - Track lane pixel

- Fit polynomial:

  ::

      x = a*y^2 + b*y + c

Lưu ý
~~~~~
- Noise gây sai lane
- Lane bị đứt

Cách xử lý:
- Smoothing
- Dùng thông tin frame trước

---

.. _week3:

Tuần 3: Centerline & Stabilization
----------------------------------

Mục tiêu
~~~~~~~~
- Tạo centerline mượt, không rung

Deliverables
~~~~~~~~~~~~
- Centerline curve
- Visualization trên RViz

Công việc
~~~~~~~~~
- Tính centerline:

  ::

      center = (left_lane + right_lane) / 2

- Smoothing:

  - Moving average
  - Exponential smoothing

- Temporal filtering
- Xử lý khi mất 1 lane

Lưu ý
~~~~~
- Jitter → NMPC mất ổn định
- Mất lane → xe lệch hướng

---

.. _week4:

Tuần 4: Trajectory Generation (CỐT LÕI)
---------------------------------------

Mục tiêu
~~~~~~~~
Chuyển centerline thành trajectory cho NMPC

Deliverables
~~~~~~~~~~~~
- ROS2 trajectory message
- Bao gồm:

  - x, y
  - yaw
  - vận tốc tham chiếu

Công việc
~~~~~~~~~
- Sample N điểm (10-20)
- Tính yaw:

  ::

      yaw_i = atan2(y_{i+1} - y_i, x_{i+1} - x_i)

- Thiết kế velocity profile:

  - Đường thẳng → nhanh
  - Đường cong → chậm

- Implement node:

  ::

      /planner_node

Lưu ý
~~~~~
- Trajectory không mượt → NMPC fail
- Ít điểm → xe chạy giật

---

.. _week5:

Tuần 5: Tích hợp NMPC (Simulation)
----------------------------------

Mục tiêu
~~~~~~~~
- Hệ thống chạy closed-loop trong Gazebo

Deliverables
~~~~~~~~~~~~
- Hệ thống hoàn chỉnh trong simulation

Công việc
~~~~~~~~~
- Định nghĩa ROS2 topics:

  ::

      /state
      /trajectory
      /control_cmd

- Đồng bộ tần số (10-20 Hz)
- Tune NMPC:

  - Q matrix
  - R matrix

- Debug hệ tọa độ

Lưu ý
~~~~~
- Delay → dao động
- Sai frame → điều khiển sai

---

.. _week6:

Tuần 6: Chạy xe thực & tối ưu
-----------------------------

Mục tiêu
~~~~~~~~
- Xe chạy ổn định ngoài thực tế

Deliverables
~~~~~~~~~~~~
- Video demo
- Đánh giá hiệu năng

Công việc
~~~~~~~~~
- Deploy lên Raspberry Pi 5
- Tối ưu CPU
- Tune ga và lái
- Test:

  - Ánh sáng khác nhau
  - Lane xấu

- Record video

Lưu ý
~~~~~
- Độ trễ phần cứng
- Nhiễu môi trường

---

Mở rộng (tuỳ chọn)
------------------

Tránh vật cản
~~~~~~~~~~~~~
- Detect object
- Dịch trajectory:

  ::

      centerline → offset

Visual Odometry
~~~~~~~~~~~~~~~
- ORB-based tracking (nếu còn thời gian)

---

KPI từng tuần
-------------

+--------+------------------------------+
| Tuần   | KPI                          |
+========+==============================+
| 1      | Bird-eye view đúng           |
+--------+------------------------------+
| 2      | Lane detection ổn định       |
+--------+------------------------------+
| 3      | Centerline mượt              |
+--------+------------------------------+
| 4      | Trajectory hợp lệ            |
+--------+------------------------------+
| 5      | Simulation chạy được         |
+--------+------------------------------+
| 6      | Xe thực chạy được            |
+--------+------------------------------+

---

Ghi chú cuối
------------

- KHÔNG bỏ qua phần planning (trajectory)
- Không tối ưu quá sớm
- Luôn visualize (RViz, overlay)
- Debug từng module, không debug toàn hệ thống cùng lúc

Kết thúc tài liệu