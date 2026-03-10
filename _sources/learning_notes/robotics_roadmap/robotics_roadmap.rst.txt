Robotics Learning Roadmap
=========================

Project Context
---------------

This project is developed under **Phibui Robotics Lab** and focuses on building a robotics system using:

- Ubuntu
- ROS2

The main objectives of the project are:

1. Build a robotics system that communicates with custom hardware using ROS2.
2. Develop a perception system using Camera and IMU sensors.
3. Compare results between simulation and real-world hardware.
4. Complete a bachelor thesis project.
5. Build a foundation for publishing a robotics research paper.

Current Background
------------------

The current development stage of the project can be described as:

**Robotics System Foundation**

Current components available:

- Ubuntu development environment
- ROS2 learning phase
- Custom-built robot hardware platform
- Documentation website built with Sphinx

The documentation website serves several purposes:

- Document robotics research
- Track project development
- Share experiment results
- Support future research publications

Research Direction
------------------

The research direction of this project focuses on:

**Visual-Inertial Perception**

Sensors used:

- Camera
- IMU

Main research goals:

- Camera + IMU fusion
- Robot perception system
- Simulation vs real-world comparison

Frameworks used:

- ROS2
- Gazebo

System Architecture
-------------------

The planned robotics system architecture is:

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

Example ROS2 topics:

::

   /camera/image_raw
   /imu/data

Possible perception approaches include:

- Visual Odometry
- Visual-Inertial Odometry
- Visual SLAM

Possible frameworks:

- ORB-SLAM3
- OpenVINS

Simulation Environment
----------------------

Simulation will be used to:

- Debug algorithms
- Test perception pipelines
- Compare results with real hardware

The simulator used in this project:

**Gazebo**

Simulation pipeline:

::

   Gazebo
      ↓
   Simulated Sensors
      ↓
   ROS2 Topics
      ↓
   Perception Algorithm

Real Hardware System
--------------------

The robot hardware platform includes:

- Camera
- IMU
- Embedded computer
- Motor controller

Real system pipeline:

::

   Real Sensors
        ↓
   ROS2 Drivers
        ↓
   Perception Algorithm
        ↓
   Robot Motion

Important design principle:

The perception algorithm should remain **identical** between simulation and real hardware.

Research Objective
------------------

The main research question:

**How different is robotics perception between simulation and real-world deployment?**

Evaluation metrics may include:

- trajectory accuracy
- drift error
- latency
- robustness

Example metrics:

- Absolute Trajectory Error (ATE)
- processing latency
- sensor noise sensitivity

Experiment Design
-----------------

Experiment 1 — Simulation
^^^^^^^^^^^^^^^^^^^^^^^^^

Run the robot in simulation and evaluate:

- robot trajectory
- perception output
- trajectory estimation accuracy

Experiment 2 — Real Robot
^^^^^^^^^^^^^^^^^^^^^^^^^

Run the robot in real-world experiments:

- same robot trajectory
- same perception pipeline

Experiment 3 — Comparison
^^^^^^^^^^^^^^^^^^^^^^^^^

Compare:

- simulation results
- real-world performance

Development Roadmap
-------------------

Phase 1 — Linux & ROS2 Foundation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Topics to learn:

- Ubuntu environment
- ROS2 basics
- nodes
- topics
- services
- launch files

Goal:

Build ROS2 communication with robot hardware.

Phase 2 — Hardware Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Implement ROS2 drivers for sensors:

- camera driver
- imu driver
- motor driver

System pipeline:

::

   Sensors → ROS2 → Robot Control

Phase 3 — Perception Development
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Focus on perception algorithms:

- Camera perception
- IMU fusion
- Visual Odometry

Possible algorithms:

- ORB-SLAM3
- OpenVINS
- custom perception modules

Phase 4 — Simulation Integration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Use Gazebo to:

- test perception algorithms
- debug ROS2 pipeline
- compare simulation and real-world results

Expected Outcomes
-----------------

Expected results of the project:

- Fully integrated ROS2 robotics system
- Visual-Inertial perception pipeline
- Simulation vs real-world evaluation

Project outputs:

- Bachelor thesis
- Robotics experiments
- Possible research publication