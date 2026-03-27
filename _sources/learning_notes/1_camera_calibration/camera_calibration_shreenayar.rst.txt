Camera_calibration
==================

Overview
--------

The key problems in computer vision: recovering the three dimensional structure  a scene from its images.

Coordinate frame (hệ quy chiếu).

e.g. 
- You have a scene in coordinate frame. 
- You would like to know where each point lies in this fram, in milimeters.
- But what you have at your disposal are images of scene where points are measured in term of pixels.

=> Images -> A full metric reconstruction: 
1. The position and orientation of the camera with respect to the world coordinate frame - external parameter of the camera.
2. How the camera maps the perspective projection points in the world onto its image plane - internal parameters of the camera (focal length).

=> Determining these 2 things (extenal & internal parameters) is called camera calibration.

Method to find a camera's internal and external parameters.

Topics
------

# We first need a model for the camera - camera model or a forward imaging model which takes you from a point in 3D to its projection in pixels in the image.
1. Linear Camera Model.
# Linear camera model - projection matrix.
2. Camera Calibration.
# Take a single picture of an object of know geometry to fully calibrate the camera => determine the projection matrix in full.
3. Extracting Intrinsic and Extrinsic Matrices.
# Tear projection matrix to figure out both internal and external parameters of the camera.
# This call intrinsic and extrinsic matrices => full calibration
4. Example Application: Simple Stereo.
# Simple example of how we use a calibratied camera to recontruct a three dimensional scene.
# 2 camera: 1 is in a particular location & 2 is displace in the horizional direction by some amount.

