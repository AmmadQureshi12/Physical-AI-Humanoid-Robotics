# ROS 2 Troubleshooting Guide

## Common Issues and Solutions

### 1. Environment Setup Issues
**Problem**: `ros2` command not found
**Solution**: 
- Ensure ROS 2 Humble is installed
- Source the ROS 2 setup script: `source /opt/ros/humble/setup.bash`
- Add sourcing command to your `.bashrc` file

### 2. Network Configuration
**Problem**: Nodes on different machines can't communicate
**Solution**:
- Check if machines are on the same network
- Ensure firewall allows DDS traffic (usually ports 7400+)
- Set `ROS_DOMAIN_ID` to same value on all machines

### 3. Permission Issues
**Problem**: Can't create/modify packages
**Solution**:
- Ensure you have proper write permissions to the workspace
- Use `colcon build` in a workspace where you have write access

### 4. Dependency Installation
**Problem**: Missing dependencies when building packages
**Solution**:
- Run `rosdep install --from-paths src --ignore-src -r -y` in your workspace
- Install missing packages with `apt install ros-humble-PACKAGE_NAME`

### 5. Topic Communication Issues
**Problem**: Publishers and subscribers not connecting
**Solution**:
- Verify topic names match exactly: `ros2 topic list`
- Check if nodes are on the same domain ID
- Ensure correct QoS settings for both publisher and subscriber

### 6. Performance Issues
**Problem**: High latency in message passing
**Solution**:
- Optimize QoS settings for your use case
- Reduce message frequency if possible
- Check system resources (CPU, memory usage)