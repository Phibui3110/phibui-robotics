Phase 1 — ROS2 Camera Pipeline
==============================

Overview
--------

Phase 1 focuses on building a complete ROS2 camera pipeline.
The goal is to ensure camera data can flow correctly from the sensor to ROS2 nodes and OpenCV.

Pipeline achieved in this phase::

    Camera
        ↓
    ROS2 Driver (v4l2_camera_node)
        ↓
    /image_raw topic (sensor_msgs/Image)
        ↓
    RViz Visualization
        ↓
    Python Subscriber Node
        ↓
    cv_bridge
        ↓
    OpenCV Processing


System Environment
------------------

Hardware

- Webcam (temporary testing camera)
- Later target: Raspberry Pi Camera Module 3

Software

- Ubuntu 22.04
- ROS2 Humble
- Python 3.10
- OpenCV
- cv_bridge
- VS Code
- Sphinx documentation


ROS2 Workspace Structure
------------------------

Workspace layout::

    ros2_ws
    ├── src
    │   └── camera_pipeline
    │       ├── package.xml
    │       ├── setup.py
    │       └── camera_pipeline
    │            ├── __init__.py
    │            └── camera_subscriber.py
    │
    ├── build
    ├── install
    └── log


Creating the ROS2 Package
-------------------------

Create the Python package::

    cd ~/main/1_projects/phibui-robotics/ros2_ws/src

    ros2 pkg create camera_pipeline \
        --build-type ament_python \
        --dependencies rclpy sensor_msgs cv_bridge


Camera Driver
-------------

Install the ROS2 camera driver::

    sudo apt install ros-humble-v4l2-camera

Run the camera node::

    ros2 run v4l2_camera v4l2_camera_node

Verify topics::

    ros2 topic list

Expected topics::

    /image_raw
    /camera_info


Visualizing Camera in RViz
--------------------------

Launch RViz::

    rviz2

Add an **Image display** and set the topic::

    /image_raw

The camera stream should now appear inside RViz.


Checking Camera Frame Rate
--------------------------

Check the frame rate::

    ros2 topic hz /image_raw

Expected result::

    average rate: ~30.0 Hz


Python Subscriber Node
----------------------

File::

    camera_pipeline/camera_subscriber.py

Example implementation::

    import rclpy
    from rclpy.node import Node
    from sensor_msgs.msg import Image
    from cv_bridge import CvBridge
    import cv2


    class CameraSubscriber(Node):

        def __init__(self):

            super().__init__('camera_subscriber')

            self.bridge = CvBridge()

            self.subscription = self.create_subscription(
                Image,
                '/image_raw',
                self.image_callback,
                10)

            self.get_logger().info("Camera subscriber node started")


        def image_callback(self, msg):

            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

            cv2.imshow("Camera Stream", frame)
            cv2.waitKey(1)


    def main(args=None):

        rclpy.init(args=args)

        node = CameraSubscriber()

        rclpy.spin(node)

        node.destroy_node()

        rclpy.shutdown()


    if __name__ == '__main__':
        main()


Configure setup.py
------------------

Edit ``setup.py`` and add the console script::

    entry_points={
        'console_scripts': [
            'camera_subscriber = camera_pipeline.camera_subscriber:main',
        ],
    }


Building the Workspace
----------------------

Build the workspace::

    cd ~/main/1_projects/phibui-robotics/ros2_ws

    colcon build

Source the environment::

    source install/setup.bash


Run the subscriber node::

    ros2 run camera_pipeline camera_subscriber


Expected result:

An OpenCV window appears showing the live camera feed.


Recording Camera Data
---------------------

Record camera data::

    ros2 bag record /image_raw

Stop recording with::

    Ctrl + C

This creates a dataset folder such as::

    rosbag2_YYYY_MM_DD-HH_MM_SS


Replaying Camera Data
---------------------

Playback the dataset::

    ros2 bag play rosbag2_YYYY_MM_DD-HH_MM_SS


Complete Phase 1 Architecture
-----------------------------

Final camera pipeline::

    Camera
        ↓
    v4l2_camera_node
        ↓
    /image_raw (sensor_msgs/Image)
        ↓
    camera_subscriber.py
        ↓
    cv_bridge
        ↓
    OpenCV processing


Phase 1 Completion Checklist
----------------------------

Completed tasks

- Run camera driver in ROS2
- Publish images to ``/image_raw``
- Visualize camera stream in RViz
- Subscribe to camera topic using Python
- Convert ROS image to OpenCV image
- Display camera stream with OpenCV
- Measure camera FPS (~30 Hz)
- Record camera data using rosbag
- Replay camera dataset using rosbag


Next Phase
----------

Phase 2 will focus on **Camera Calibration and Undistortion**.

Future perception pipeline::

    Camera
        ↓
    Calibration
        ↓
    Undistortion
        ↓
    Bird Eye View Transform
        ↓
    Lane Detection
        ↓
    Controller
        ↓
    Vehicle