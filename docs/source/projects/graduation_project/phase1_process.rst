Phase 1 - ROS2 Camera Foundation - Process
==========================================
This document describes the development process of **Phase 1** of the graduation project.

1. ROS2 Foundation
-------------------
**Objective**: To establish a solid foundation in ROS2, enabling the development of camera-related functionalities.
What I need to study:

Core ROS2
~~~~~~~~~

1. ROS2 nodes. (done)
2. ROS2 topics. (done)
3. ROS2 services. (done)
4. ROS2 actions. (done)

System configuration
~~~~~~~~~~~~~~~~~~~~

5. ROS2 parameters. (done)
6. ROS2 launch system. 
7. ROS2 Logging.
8. ROS2 packages and workspace structure.

Perception foundations
~~~~~~~~~~~~~~~~~~~~~~

9.  ROS2 QoS. 
10. TF2 (coordinate frames)
11. sensor_msgs.

Debugging tools
~~~~~~~~~~~~~~~

12. ros2 topic echo.
13. ros2 topic hz.
14. rqt_graph. (done)

2. Understanding actions
------------------------
Goal: introspect actions in ROS2

Tutorial level: Beginner

Background
~~~~~~~~~~

Actions: communication types in ros2 & for long running tasks. They consist of three parts: 

- A goal
- feedback
- A result
  
Actions are built on topics and services. Their functionality is similar to services, except actions can be canceled.
They also provide steady feedback, as opposed to services which return a single response.

Actions use a client-server model, similar to the publisher-subsriber model. An "action client" node sends a goal to an "action server" node that acknowledges the goal and returns a stream of feedback and a result.

Summary
~~~~~~~

Actions are like services that allow you to execute long running tasks, provide regualr feedback, and are cancelable.

A robot system would like use actions for navigation. An action goal could tell a robot to travel to a poistion. 
While the robot navigates to the position, it can send updates along the way, and then a final result message once it's reached its destination.

Turtlesim has an action server that action clients can send goals to for rotating turtles.

3. Using rqt_console to view logs
---------------------------------

Goal: get to know rqt_console, a tool for introspecting log messages.

Fix the auto screen scale in rqt_console
 
.. code-block:: bash

    QT_AUTO_SCREEN_SCALE_FACTOR=1 ros2 run rqt_console rqt_console

`rqt_console documentation <https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Using-Rqt-Console/Using-Rqt-Console.html>`_

Summary
~~~~~~~

rqt_console can be very helpful if you need to closely examine the log messages from your system. You might want to examine log messages for any number of reasons, usually to find out where something went wrong and the series of events leading up to that.

4.  Launching nodes
-------------------

Goal: use a command line tool to launch multiple nodes at once.

Background
~~~~~~~~~~

In most of the introductory tutorials, you have been opening new terminals for every new node you run. As you create more complex systems with more and more nodes running simultaneously, opening terminals and reentering (nhap lai) configuration details becomes tedious (te nhat).

Launch files allow you to start up and configure a number of executables (file can run) containing ROS 2 nodes simultaneously.

Running a single launch file with the ros2 launch command will start up your entire system - all nodes and their configurations - at once.

Tasks
~~~~~

`Launching_file <https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Launching-Multiple-Nodes/Launching-Multiple-Nodes.html>`_

Summary
~~~~~~~

The significance of what you' ve done so far is that you’ve run two turtlesim nodes with one command. Once you learn to write your own launch files, you’ll be able to run multiple nodes - and set up their configuration - in a similar way, with the ros2 launch command.

5. Recording and playing back data
----------------------------------

Goal: record data published on a topic so you can replay and examine it any time.

Background
~~~~~~~~~~

ros2 bag is a command line tool for recording data published on topics in your system. It accumulates the data passed on any number of topics and saves it in a database. You can then replay the data to reproduce the results of your tests and experiments. Recording topics is also a great way to share your work and allow others to recreate it.

Tasks
~~~~~

`Recording_and_playing_back_data <https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Recording-And-Playing-Back-Data/Recording-And-Playing-Back-Data.html>`_

Summary
~~~~~~~

You can record data passed on topics in your ROS 2 system using the ros2 bag command. Whether you’re sharing your work with others or introspecting your own experiments, it's a great tool to know about.