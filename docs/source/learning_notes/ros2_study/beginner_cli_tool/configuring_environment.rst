Confiugring Environment
=======================

Background
----------
- Underlay: ROS2 workspace.
  
- Overlays: Subsequent local workspaces.

Tasks 
-----
1. Source the setup files
   
    .. code-block:: bash

        source /opt/ros/humble/setup.bash

2. Add sourcing to your shell startup script
   
   .. code-block:: bash

        echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc

3. Check environment variables
   
   .. code-block:: bash

          printenv | grep -i ROS

3.1. The ROS DOMAIN ID variable

DDS: Data Distribution Service, a middleware protocol and API standard for data-centric connectivity.

e.g. Node A => publish => Topic> subscibe => Node B.

All ROS2 nodes use domain ID 0 by default.

Choosing a domain ID (short version)
     
    Simply choose a number between 0 and 101, and set it as the ROS_DOMAIN_ID environment variable in your shell.


