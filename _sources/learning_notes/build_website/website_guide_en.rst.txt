Documentation Website Guide
===========================

This document explains how to **use, maintain, and contribute** to the Phibui Robotics Lab documentation website.

It covers:

* Repository structure
* Documentation structure
* Writing workflow
* reStructuredText guidelines
* Build and deployment
* Best practices
* Common mistakes to avoid

====================================================================

1. PURPOSE OF THIS WEBSITE
   ====================================================================

This website serves as an **engineering documentation portal** for robotics projects developed in Phibui Robotics Lab.

Main goals:

• Document robotics projects
• Record learning process in robotics
• Provide tutorials for ROS2 / Ubuntu / Robotics
• Maintain engineering documentation for the autonomous vehicle project

The website is built using:

Sphinx + reStructuredText + GitHub Pages.

====================================================================
2. REPOSITORY STRUCTURE
=======================

The repository is organized as follows:

phibui-robotics

├── docs
│
├── ros2_ws
├── firmware
├── hardware
├── simulations
├── scripts
│
├── .github
│   └── workflows
│
├── README.md
├── LICENSE
└── .gitignore

Explanation:

docs
Documentation website source files

ros2_ws
ROS2 workspace for the robotics software stack

firmware
STM32 firmware

hardware
Hardware design files, wiring diagrams, CAD, etc.

simulations
Simulation environment

scripts
Utility scripts for development

The documentation website is entirely located in:

docs/

====================================================================
3. DOCUMENTATION STRUCTURE
==========================

docs/source

├── index.rst
│
├── projects
│   ├── index.rst
│   └── autonomous_vehicle
│       ├── index.rst
│       ├── overview.rst
│       ├── system_architecture.rst
│       ├── hardware.rst
│       ├── software.rst
│       ├── ros2_workspace.rst
│       ├── sensors.rst
│       ├── perception.rst
│       ├── control.rst
│       ├── simulation.rst
│       └── experiments.rst
│
├── system
│   ├── index.rst
│   ├── hardware
│   ├── software
│   ├── perception
│   ├── control
│   └── simulation
│
├── tutorials
│   └── index.rst
│
├── learning_notes
│   └── index.rst
│
└── blog
└── index.rst

Meaning of each section:

projects
Documentation for robotics projects.

system
Engineering architecture documentation.

tutorials
Step-by-step tutorials.

learning_notes
Personal notes while studying robotics.

blog
Development logs and project updates.

====================================================================
4. WRITING WORKFLOW
===================

Typical workflow:

Edit .rst files
↓
git add
↓
git commit
↓
git push
↓
GitHub Actions builds the documentation
↓
GitHub Pages deploys the website

Local development workflow:

1. Edit documentation

Example:

docs/source/projects/autonomous_vehicle/overview.rst

2. Build documentation locally

cd docs
make html

3. Open the generated website

docs/build/html/index.html

4. Commit changes

git add .
git commit -m "update documentation"
git push

====================================================================
5. RESTRUCTUREDTEXT (RST) BASICS
================================

All documentation is written using reStructuredText (.rst).

---

## 5.1 Titles

Titles must use underline style.

Example:

# Autonomous Vehicle Overview

## Hardware Architecture

---

## 5.2 Paragraphs

Just write plain text.

Example:

This document describes the hardware architecture
of the autonomous vehicle platform.

---

## 5.3 Bullet Lists

Example:

* Raspberry Pi 5
* STM32 Nucleo
* IMU
* Camera

---

## 5.4 Code Blocks

Example:

.. code-block:: bash

ros2 topic list

---

## 5.5 Images

Example:

.. .. image:: images/vehicle.jpg
.. :width: 600pix
.. :align: center

====================================================================
6. TOCTREE STRUCTURE
====================

Navigation is controlled by toctree.

Example:

.. .. toctree::
.. :maxdepth: 2

.. overview
.. hardware
.. software

Rules:

• Paths are relative to the current file
• Do not include .rst extension
• Every document must have a title

====================================================================
7. ADDING A NEW PAGE
====================

Example: add a new perception document.

Step 1

Create file:

projects/autonomous_vehicle/perception_pipeline.rst

Step 2

Add a title:

# Perception Pipeline

Step 3

Add it to the toctree:

projects/autonomous_vehicle/index.rst

.. .. toctree::
.. :maxdepth: 1

.. overview
.. perception_pipeline

====================================================================
8. DEPLOYMENT PROCESS
=====================

Deployment is fully automated.

When code is pushed to GitHub:

GitHub Actions will:

1. Install dependencies
2. Build Sphinx documentation
3. Deploy to GitHub Pages

The live website is available at:

https://phibui3110.github.io/phibui-robotics

====================================================================
9. BEST PRACTICES
=================

Write clear titles

Example:

# Control System

instead of

Control

Keep documents focused

One document = one topic

Use diagrams when possible

Architecture diagrams help readers understand the system faster.

Mirror repository structure

Example:

ros2_ws → ros2 documentation
hardware → hardware documentation

====================================================================
10. COMMON MISTAKES
===================

Missing title

Every .rst file must start with a title.

Incorrect toctree paths

Wrong:

projects/autonomous_vehicle/overview

Correct:

overview

File not added to toctree

If a page is not in toctree, it will not appear in navigation.

Forgetting to rebuild

Always run:

make html

before committing.

====================================================================
11. DEVELOPMENT ENVIRONMENT
===========================

Python virtual environment:

docs-env

Activate environment:

source docs-env/bin/activate

Install dependencies:

pip install sphinx
pip install sphinx_rtd_theme

Build documentation:

cd docs
make html

====================================================================
12. FUTURE IMPROVEMENTS
=======================

Possible extensions:

sphinx-mermaid
Architecture diagrams

sphinx-copybutton
Copy code button

sphinx-design
Better UI components

====================================================================
END OF DOCUMENT
===============
