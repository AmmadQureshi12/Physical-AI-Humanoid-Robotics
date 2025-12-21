# Capstone Humanoid Project Troubleshooting Guide

## Common Issues and Solutions

### 1. System Integration Problems
**Problem**: Components don't communicate properly when integrated
**Solution**:
- Verify all ROS 2 topics and services are correctly named and matched
- Use `ros2 topic list` and `ros2 service list` to confirm availability
- Check that message types match between publishers and subscribers
- Use `rqt_graph` to visualize the system graph and identify disconnected nodes
- Implement proper launch files to ensure nodes start in correct order

### 2. Navigation Failures
**Problem**: Robot fails to navigate to designated locations
**Solution**:
- Verify map is correctly loaded: `ros2 run nav2_map_server map_server`
- Check localization is working: `ros2 run nav2_localization localization_node`
- Validate costmaps are updated: `ros2 run rviz2 rviz2`
- Ensure proper transforms (TF) between coordinate frames
- Check that navigation parameters are tuned for humanoid-specific movement

### 3. Manipulation Issues
**Problem**: Robot cannot successfully grasp or manipulate objects
**Solution**:
- Verify MoveIt configuration is correct for your robot's kinematics
- Check that object detection and pose estimation are accurate
- Validate grasp planning parameters
- Ensure robot has sufficient reach and dexterity for the task
- Test manipulation pipeline independently before integration

### 4. VLA Integration Problems
**Problem**: Voice commands are not processed or executed correctly
**Solution**:
- Confirm Whisper is properly configured and receiving audio input
- Verify LLM is generating appropriate plans from voice input
- Check that planned actions match available robot capabilities
- Validate JSON parsing of action plans
- Implement proper error handling for ambiguous commands

### 5. Performance Bottlenecks
**Problem**: System responses are too slow for real-time operation
**Solution**:
- Identify bottlenecks using ROS 2 tools like `ros2 bag` and `tracetools`
- Optimize message serialization/deserialization
- Reduce unnecessary computations in critical loops
- Consider using faster models for real-time processing
- Implement proper threading for I/O operations

### 6. Sim-to-Real Transfer Issues
**Problem**: Behaviors that work in simulation fail on real hardware
**Solution**:
- Account for sensor noise and uncertainty in real environments
- Adjust control parameters for real-world dynamics
- Implement proper safety checks before real-world execution
- Calibrate sensors and actuators properly
- Test extensively in simulation with added noise models

### 7. Multi-Step Task Failures
**Problem**: Complex multi-step tasks fail partway through execution
**Solution**:
- Implement proper state tracking and recovery mechanisms
- Add validation checks after each step
- Design tasks with error recovery in mind
- Implement timeouts and fallback behaviors
- Test individual steps before combining into complex tasks

### 8. Sensor Fusion Problems
**Problem**: Different sensor inputs are not properly combined
**Solution**:
- Verify sensor timestamps are synchronized
- Check that sensor data is properly calibrated
- Validate that sensor data is being published at appropriate rates
- Use robot_state_publisher to ensure TF tree is complete
- Implement proper filtering for noisy sensor data