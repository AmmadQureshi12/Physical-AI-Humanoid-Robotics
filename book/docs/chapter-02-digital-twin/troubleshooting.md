# Simulation Troubleshooting Guide

## Common Issues and Solutions

### 1. Gazebo Installation and Launch Issues
**Problem**: Gazebo fails to start or crashes immediately
**Solution**:
- Ensure GPU drivers are up to date
- Install Gazebo via package manager: `sudo apt install gazebo libgazebo-dev`
- Check that your graphics drivers support OpenGL 2.1+
- Try running with software rendering: `export LIBGL_ALWAYS_SOFTWARE=1`

### 2. Robot Model Loading Issues
**Problem**: URDF model fails to load in Gazebo
**Solution**:
- Validate URDF syntax with `check_urdf` tool
- Ensure all mesh files and textures are accessible
- Check that joint limits are properly defined
- Verify all required plugins are installed

### 3. Sensor Simulation Problems
**Problem**: Sensors don't publish data or publish invalid data
**Solution**:
- Check that sensor plugins are correctly configured in URDF
- Verify sensor frames are properly attached to robot links
- Ensure sensor topics are being published: `ros2 topic list | grep sensor`
- Check sensor parameters (min/max range, resolution, etc.)

### 4. Performance Issues
**Problem**: Simulation runs slowly or with low frame rates
**Solution**:
- Reduce physics update rate in world file
- Simplify collision geometries (use boxes instead of meshes)
- Reduce sensor resolution or update rates
- Close other applications to free up resources

### 5. ROS Integration Issues
**Problem**: Cannot control simulated robot via ROS 2
**Solution**:
- Ensure gazebo_ros_pkgs are installed
- Check that controller plugins are loaded in URDF
- Verify joint names match between URDF and controller configuration
- Check ROS 2 topic names and types with `ros2 topic list` and `ros2 topic info`

### 6. Physics Issues
**Problem**: Robot falls through floor or exhibits unstable behavior
**Solution**:
- Check that models have proper inertial properties
- Verify collision geometries are correctly defined
- Adjust physics parameters (step size, solver type)
- Increase constraint parameters if needed

### 7. Unity Integration Issues
**Problem**: Cannot connect Unity to ROS 2
**Solution**:
- Install ROS# package in Unity
- Ensure correct IP addresses and ports are configured
- Check firewall settings allow communication
- Verify ROS 2 network configuration

### 8. Visualization Problems
**Problem**: Robot appears invisible or with incorrect materials
**Solution**:
- Verify that visual geometries are defined in URDF
- Check that material definitions are correct
- Ensure mesh files are in the correct location
- Try different Gazebo versions if using complex materials