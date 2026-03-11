Camera–IMU Assisted BEV Lane Following for Autonomous RC Car
=============================================================

Overview
--------

This document defines the development roadmap for the graduation project:

**Camera - IMU Assisted BEV Lane Following for Autonomous RC Car**

The objective of this project is to design and implement a **mini autonomous driving system**
using a **1/16 scale RC car** equipped with:

- Raspberry Pi 5
- Raspberry Pi Camera Module 3 Wide (120° FOV)
- BNO055 IMU
- Nucleo F411RE microcontroller
- ESC 1060WP
- 550 Brushed Motor
- Servo 17g

The project aims to reproduce a **simplified autonomous driving stack** using classical
computer vision techniques, sensor fusion, and ROS2 architecture.

Final System Architecture
-------------------------

The final system should follow a structured autonomous driving pipeline.

::

   Camera
      ↓
   Image Processing
      ↓
   BEV Transformation
      ↓
   Lane Detection
      ↓
   Lane Geometry Estimation
      ↓
   IMU Orientation Estimation
      ↓
   Sensor Fusion
      ↓
   Vehicle Controller
      ↓
   Vehicle Interface (Nucleo)

ROS2 Node Architecture
----------------------

The ROS2 system should be modular and divided into multiple nodes.

::

   /camera_node
   /bev_transform_node
   /lane_detection_node
   /imu_node
   /sensor_fusion_node
   /control_node
   /vehicle_interface_node

Example ROS2 topics:

::

   /camera/image_raw
   /camera/camera_info
   /lane_detection/lane_center
   /lane_detection/lane_angle
   /imu/data
   /vehicle/steering_cmd

Global Learning Priorities
--------------------------

The following knowledge areas must be prioritized:

1. ROS2 system architecture
2. OpenCV image processing
3. Camera calibration
4. Bird's Eye View (BEV) transformation
5. Control systems and IMU fusion

All other topics are secondary.

Project Roadmap (8 Weeks)
=========================

Phase 1 — ROS2 Camera Foundation
--------------------------------

Duration: **~1 week**

Goal: build a functioning ROS2 camera pipeline.

Tasks:

Study:

- ROS2 image pipeline
- ``cv_bridge``
- ``image_transport``
- RViz visualization

System goal:

::

   Camera → ROS2 topic → RViz display

Important ROS2 topic:

::

   /camera/image_raw

Tools to learn:

- ``rqt_graph``
- ``ros2 topic echo``
- ``ros2 topic hz``
- ``rosbag``

Expected result:

- Camera streaming through ROS2
- Images accessible inside Python nodes


Phase 2 — OpenCV Lane Detection
-------------------------------

Duration: **~1 week**

Goal: implement lane detection **without ROS2 first**.

Pipeline:

::

   image
   → HSV conversion
   → color threshold
   → Gaussian blur
   → Canny edge detection
   → Hough transform
   → lane center estimation

Important OpenCV functions:

::

   cv2.cvtColor
   cv2.inRange
   cv2.GaussianBlur
   cv2.Canny
   cv2.HoughLinesP

Outputs:

::

   lane_center
   lane_angle

The detected lanes should be visualized by overlaying lines on the original image.


Phase 3 — Camera Calibration
----------------------------

Goal: remove camera lens distortion.

Because the **Camera Module 3 Wide (120°)** has strong distortion, calibration is critical.

Steps:

1. Print a chessboard pattern
2. Capture ~20 calibration images
3. Run OpenCV calibration

Important functions:

::

   cv2.findChessboardCorners
   cv2.calibrateCamera
   cv2.undistort

Outputs:

::

   camera_matrix
   distortion_coefficients

These parameters should be stored in a **YAML calibration file**.

In ROS2 this corresponds to:

::

   /camera/camera_info


Phase 4 — Bird's Eye View (BEV)
-------------------------------

Goal: convert the camera image into a **top-down road view**.

BEV uses a **perspective transformation** based on a homography matrix.

Mathematical form:

::

   x' = Hx

Where ``H`` is a **3×3 homography matrix**.

Implementation:

::

   cv2.getPerspectiveTransform
   cv2.warpPerspective

Workflow:

::

   camera image
   → undistort
   → perspective transform
   → BEV image

Result:

- lane lines become approximately parallel
- lane detection becomes easier and more stable


Phase 5 — Lane Detection on BEV
-------------------------------

After BEV transformation, perform lane detection again.

Typical algorithm:

1. threshold white lane pixels
2. sliding window search
3. polynomial curve fitting

Outputs:

::

   lane_center
   lane_curvature

Steering error:

::

   error = lane_center - vehicle_center

This value becomes the control input.


Phase 6 — IMU Integration
-------------------------

Goal: integrate **BNO055 orientation data**.

Hardware connection:

::

   BNO055 → I2C → Raspberry Pi

ROS2 node publishes:

::

   /imu/data

Important signals:

::

   yaw
   angular_velocity_z


Phase 7 — Sensor Fusion
-----------------------

Combine camera heading with IMU orientation.

Simple fusion model:

::

   heading_estimate =
       0.7 * camera_heading +
       0.3 * imu_heading

More advanced alternatives:

- complementary filter
- Kalman filter


Phase 8 — Vehicle Control
-------------------------

Implement a steering controller.

Control equation:

::

   steering_angle = Kp * error + Kd * error_rate

Publish command:

::

   /vehicle/steering_cmd

This command is transmitted through **serial communication** to the Nucleo F411.


Phase 9 — System Integration
----------------------------

Full perception-to-control pipeline:

::

   Camera
      ↓
   Calibration
      ↓
   BEV Transform
      ↓
   Lane Detection
      ↓
   IMU Fusion
      ↓
   PID Controller
      ↓
   Nucleo Steering Control

The RC car should autonomously follow a **tape-based lane track**.


Phase 10 — Simulation (Optional)
--------------------------------

Gazebo simulation can be used to evaluate **simulation vs reality**.

Example metrics:

+-----------------------+-----------------------+
| Metric                | Meaning               |
+-----------------------+-----------------------+
| Metric                | Meaning               |
+-----------------------+-----------------------+
|| Lane deviation       || distance from center |
|| Steering oscillation || control stability    |
|| Success rate         || track completion     |
+-----------------------+-----------------------+

This comparison can strengthen the research contribution.


Development Architecture
------------------------

Recommended computing architecture:

::

   Laptop
      ├ perception processing
      ├ BEV transformation
      └ ROS2 core

   Raspberry Pi
      ├ camera driver
      └ hardware interface

   Nucleo
      └ motor and servo control

Communication is handled via **ROS2 DDS network**.


Expected Final Demonstration
----------------------------

The final project demonstration should show:

1. Autonomous RC car lane following
2. BEV visualization
3. Lane detection overlay
4. IMU orientation monitoring
5. ROS2 node graph visualization

This structure represents a **mini autonomous driving platform**.


Daily Study Priorities
----------------------

Recommended study order:

1. ROS2 camera pipeline
2. OpenCV fundamentals
3. Camera calibration
4. BEV transformation
5. Lane detection
6. IMU integration
7. Control systems

Control implementation should **only begin after perception is stable**.


Conclusion
----------

This project replicates a **simplified autonomous driving stack** combining:

- perception (camera)
- localization (IMU)
- control (steering controller)

The system demonstrates how **low-cost hardware can be used to implement
core autonomous driving technologies** using classical computer vision
and ROS2-based robotics architecture.