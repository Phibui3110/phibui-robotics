Overview
========

The autonomous vehicle system is composed of several subsystems
that work together to perceive the environment and control the vehicle.

Subsystems
----------

The system consists of the following main subsystems:

* **Perception**  
  Processes camera data and extracts useful information from the environment.

* **State Estimation**  
  Estimates the current state of the vehicle using sensor data such as the IMU.

* **Control**  
  Computes steering and throttle commands based on perception and state information.

* **Hardware Interface**  
  Communicates with the STM32 microcontroller to control actuators.


System Architecture Diagram
---------------------------

The following diagram shows the high-level architecture of the system.

.. mermaid:

   flowchart LR

      Camera --> Perception
      IMU --> StateEstimation

      Perception --> Control
      StateEstimation --> Control

      Control --> STM32

      STM32 --> Motor
      STM32 --> Servo