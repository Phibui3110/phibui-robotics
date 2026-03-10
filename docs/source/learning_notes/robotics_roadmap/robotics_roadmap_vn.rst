Lộ trình học Robotics
=====================

Bối cảnh dự án
--------------

Dự án này được phát triển trong **Phibui Robotics Lab** với mục tiêu xây dựng một hệ thống robot sử dụng:

- Ubuntu
- ROS2

Các mục tiêu chính của dự án:

1. Xây dựng hệ thống robot giao tiếp với hardware tự thiết kế thông qua ROS2
2. Phát triển hệ thống perception dựa trên Camera và IMU
3. So sánh kết quả giữa mô phỏng và robot thật
4. Hoàn thành đồ án tốt nghiệp
5. Xây dựng nền tảng cho một bài báo nghiên cứu robotics

Bối cảnh hiện tại
-----------------

Hiện tại dự án đang ở giai đoạn:

**Robotics System Foundation**

Các thành phần hiện có:

- môi trường phát triển Ubuntu
- đang học ROS2
- robot hardware tự thiết kế
- website documentation được xây dựng bằng Sphinx

Website documentation có mục tiêu:

- ghi lại quá trình nghiên cứu robotics
- theo dõi tiến trình phát triển hệ thống
- chia sẻ kết quả thí nghiệm
- hỗ trợ việc viết paper trong tương lai

Hướng nghiên cứu
----------------

Hướng nghiên cứu chính của dự án:

**Visual-Inertial Perception**

Các sensor sử dụng:

- Camera
- IMU

Mục tiêu nghiên cứu:

- fusion dữ liệu Camera và IMU
- xây dựng hệ thống perception cho robot
- so sánh kết quả giữa simulation và thực tế

Framework sử dụng:

- ROS2
- Gazebo

Kiến trúc hệ thống
------------------

Kiến trúc hệ thống robot dự kiến:

::

   Camera
   IMU
        ↓
   ROS2 Sensor Drivers
        ↓
   Sensor Synchronization
        ↓
   Visual-Inertial Perception
        ↓
   State Estimation
        ↓
   Robot Control

Ví dụ các ROS2 topics:

::

   /camera/image_raw
   /imu/data

Các hướng thuật toán perception có thể sử dụng:

- Visual Odometry
- Visual-Inertial Odometry
- Visual SLAM

Một số framework phổ biến:

- ORB-SLAM3
- OpenVINS

Môi trường mô phỏng
-------------------

Simulation được sử dụng để:

- debug thuật toán
- test perception pipeline
- so sánh kết quả với robot thật

Simulator được sử dụng trong dự án:

**Gazebo**

Pipeline trong simulation:

::

   Gazebo
      ↓
   Simulated Sensors
      ↓
   ROS2 Topics
      ↓
   Perception Algorithm

Hệ thống hardware thật
----------------------

Robot hardware bao gồm:

- Camera
- IMU
- máy tính nhúng
- motor controller

Pipeline hệ thống thực tế:

::

   Real Sensors
        ↓
   ROS2 Drivers
        ↓
   Perception Algorithm
        ↓
   Robot Motion

Nguyên tắc quan trọng:

Thuật toán perception cần **giữ giống nhau** giữa simulation và hardware thật.

Mục tiêu nghiên cứu
-------------------

Câu hỏi nghiên cứu chính của dự án:

**Simulation và môi trường thực tế khác nhau như thế nào đối với hệ thống perception của robot?**

Các metrics đánh giá có thể bao gồm:

- độ chính xác quỹ đạo
- drift error
- độ trễ xử lý
- độ ổn định của hệ thống

Ví dụ các metrics cụ thể:

- Absolute Trajectory Error (ATE)
- processing latency
- sensor noise sensitivity

Thiết kế thí nghiệm
-------------------

Thí nghiệm 1 — Simulation
^^^^^^^^^^^^^^^^^^^^^^^^^

Robot chạy trong môi trường mô phỏng để đánh giá:

- quỹ đạo robot
- output của perception
- độ chính xác ước lượng vị trí

Thí nghiệm 2 — Robot thật
^^^^^^^^^^^^^^^^^^^^^^^^^

Robot chạy trong môi trường thực với:

- cùng quỹ đạo
- cùng perception pipeline

Thí nghiệm 3 — So sánh
^^^^^^^^^^^^^^^^^^^^^^

So sánh:

- kết quả từ simulation
- kết quả từ robot thật

Lộ trình phát triển
-------------------

Phase 1 — Nền tảng Linux và ROS2
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Các nội dung cần học:

- Ubuntu environment
- ROS2 cơ bản
- nodes
- topics
- services
- launch files

Mục tiêu:

Xây dựng hệ thống ROS2 giao tiếp được với robot hardware.

Phase 2 — Tích hợp hardware
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Xây dựng ROS2 drivers cho các sensor:

- camera driver
- imu driver
- motor driver

Pipeline hệ thống:

::

   Sensors → ROS2 → Robot Control

Phase 3 — Phát triển perception
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Tập trung vào các thuật toán perception:

- Camera perception
- IMU fusion
- Visual Odometry

Các thuật toán có thể sử dụng:

- ORB-SLAM3
- OpenVINS
- custom perception modules

Phase 4 — Tích hợp simulation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Sử dụng Gazebo để:

- test perception algorithms
- debug ROS2 pipeline
- so sánh simulation với robot thật

Kết quả kỳ vọng
---------------

Kết quả dự kiến của dự án:

- hệ thống robotics hoàn chỉnh dựa trên ROS2
- pipeline perception sử dụng Camera và IMU
- đánh giá sự khác biệt giữa simulation và thực tế

Các sản phẩm đầu ra của dự án:

- đồ án tốt nghiệp
- hệ thống robot hoàn chỉnh
- các thí nghiệm robotics
- nền tảng cho một bài báo nghiên cứu