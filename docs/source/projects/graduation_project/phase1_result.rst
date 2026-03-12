Phase 1 - ROS2 Camera Foundation - Results
==========================================
This document summarizes the results of **Phase 1** of the graduation project.

Objective
---------

The goal of Phase 1 is to build a **complete ROS2 camera pipeline** that allows the system to:

1. Capture images from the camera
2. Publish images as a ROS2 topic
3. Visualize the camera stream in RViz
4. Access camera data inside a Python ROS2 node
5. Record and replay camera data using rosbag

Once this pipeline works reliably, the perception system can later integrate **OpenCV processing, BEV transformation, and lane detection**.

System Pipeline
---------------

The system should achieve the following data flow:

::

   Raspberry Pi Camera
          ↓
     ROS2 camera node
          ↓
     /camera/image_raw
          ↓
      RViz visualization
          ↓
      Python subscriber node


Result 1 — Camera Publishing ROS2 Images
----------------------------------------

First, ensure the camera node publishes image data.

Check available topics:

.. code-block:: bash

   ros2 topic list

You should see topics similar to:

::

   /camera/image_raw
   /camera/camera_info

Verify that data is being published:

.. code-block:: bash

   ros2 topic echo /camera/image_raw

Expected message type:

::

   sensor_msgs/msg/Image


Result 2 — Camera Visible in RViz
---------------------------------

Start RViz:

.. code-block:: bash

   rviz2

Add a display:

::

   Image

Set the topic:

::

   /camera/image_raw

If the camera pipeline works correctly, RViz should display **live video from the camera**.


Result 3 — Python Node Can Read Images
--------------------------------------

Create a ROS2 Python node that subscribes to the camera topic.

Example minimal subscriber node:

.. code-block:: python

   import rclpy
   from rclpy.node import Node
   from sensor_msgs.msg import Image

   class CameraSubscriber(Node):

       def __init__(self):
           super().__init__('camera_subscriber')

           self.subscription = self.create_subscription(
               Image,
               '/camera/image_raw',
               self.listener_callback,
               10)

       def listener_callback(self, msg):
           self.get_logger().info('Received image')

   def main(args=None):
       rclpy.init(args=args)

       node = CameraSubscriber()
       rclpy.spin(node)

       node.destroy_node()
       rclpy.shutdown()

   if __name__ == '__main__':
       main()

Run the node and confirm that the terminal prints:

::

   Received image
   Received image
   Received image


Result 4 — Understand the Camera Message Type
---------------------------------------------

The topic ``/camera/image_raw`` publishes messages of type:

::

   sensor_msgs/msg/Image

Important fields inside this message include:

::

   height
   width
   encoding
   data

Understanding this message structure is important for converting images into OpenCV format later.


Result 5 — Convert ROS Image to OpenCV Image
--------------------------------------------

Install the required bridge package:

.. code-block:: bash

   sudo apt install ros-humble-cv-bridge

Example conversion:

.. code-block:: python

   from cv_bridge import CvBridge

   bridge = CvBridge()
   cv_image = bridge.imgmsg_to_cv2(msg, "bgr8")

This conversion allows the pipeline to become:

::

   ROS Image → OpenCV Image → Computer Vision Processing


Result 6 — Record Camera Data with rosbag
-----------------------------------------

Record camera data:

.. code-block:: bash

   ros2 bag record /camera/image_raw

Stop recording using ``Ctrl+C``.

Replay the recorded data:

.. code-block:: bash

   ros2 bag play <bag_folder>

This allows testing perception algorithms **without requiring the physical camera**.


Result 7 — ROS2 Camera Debugging Tools
--------------------------------------

Check topic frequency:

.. code-block:: bash

   ros2 topic hz /camera/image_raw

Example output:

::

   average rate: 30.1 Hz

Inspect the message definition:

.. code-block:: bash

   ros2 interface show sensor_msgs/msg/Image

Visualize node connections:

.. code-block:: bash

   rqt_graph

Expected graph structure:

::

   camera_node → /camera/image_raw → camera_subscriber


Workspace Structure
-------------------

By the end of Phase 1, your ROS2 workspace may look like:

::

   ros2_ws/
    ├── src/
    │   ├── camera_driver
    │   └── camera_subscriber
    │
    ├── build
    ├── install
    └── log

Inside ``camera_subscriber``:

::

   camera_subscriber/
    ├── package.xml
    ├── setup.py
    └── camera_subscriber/
        └── camera_subscriber.py


Phase 1 Completion Checklist
----------------------------

Phase 1 is complete when the following conditions are satisfied:

::

   [ ] Camera publishes /camera/image_raw
   [ ] RViz displays the live camera stream
   [ ] Python node successfully subscribes to images
   [ ] ROS images convert to OpenCV images using cv_bridge
   [ ] rosbag records and replays camera data
   [ ] rqt_graph shows the node connections

Once all items are completed, **Phase 1 is finished**.


Why Phase 1 Is Critical
-----------------------

All future perception components depend on this camera pipeline.

The future perception system will follow this architecture:

::

   Camera
      ↓
   ROS2 Image
      ↓
   OpenCV Processing
      ↓
   BEV Transformation
      ↓
   Lane Detection
      ↓
   Vehicle Control

If the camera pipeline is unstable, the later perception stages will fail.


Next Phase
----------

After completing Phase 1, the next step is:

**Phase 2 — OpenCV Lane Detection**

Pipeline:

::

   ROS Image
      ↓
   cv_bridge
      ↓
   OpenCV Image
      ↓
   Lane Detection