# Troubleshooting Guide for AI-Humanoid Robotics Curriculum

## Overview

This guide provides solutions to common problems encountered when working with the AI-Humanoid Robotics curriculum. It covers issues related to ROS 2, simulation environments, AI integration, and hardware validation.

## General Troubleshooting Approach

1. **Check the basics**: Ensure all required software is installed and properly configured
2. **Verify environment setup**: Confirm ROS 2 environment is sourced, paths are set correctly
3. **Check system resources**: Ensure sufficient RAM, disk space, and GPU resources
4. **Review logs**: Examine ROS 2 logs and system messages for error details
5. **Isolate the problem**: Test components individually before integration

## 1. ROS 2 Common Issues

### Problem: `ros2` command not found
**Solution**:
- Source the ROS 2 installation: `source /opt/ros/humble/setup.bash`
- Add to your `.bashrc` file: `echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc`
- Verify installation: `printenv | grep ROS`

### Problem: Nodes cannot communicate across machines
**Solution**:
- Ensure machines are on the same network
- Set ROS domain ID consistently: `export ROS_DOMAIN_ID=0`
- Check firewall settings for DDS communication (usually ports 7400+)
- Verify network configuration: `ros2 topic list` on both machines

### Problem: Missing ROS 2 packages
**Solution**:
- Update package lists: `sudo apt update`
- Install missing packages: `sudo apt install ros-humble-PACKAGE_NAME`
- Use rosdep: `rosdep install --from-paths src --ignore-src -r -y`

## 2. Simulation Environment Issues

### Problem: Gazebo fails to start or crashes immediately
**Solution**:
- Check GPU drivers: `nvidia-smi` or `glxinfo | grep "OpenGL renderer"`
- Install graphics libraries: `sudo apt install mesa-utils`
- Try software rendering: `export LIBGL_ALWAYS_SOFTWARE=1`
- Ensure sufficient RAM for physics simulation

### Problem: Robot model appears invisible in Gazebo
**Solution**:
- Verify URDF file syntax: `check_urdf path/to/robot.urdf`
- Check that mesh files are in correct location
- Verify material definitions in URDF
- Try different Gazebo versions if using complex materials

### Problem: Unity does not connect to ROS 2
**Solution**:
- Install ROS# Unity package
- Verify IP addresses and ports are correctly configured
- Check firewall settings allow communication
- Ensure ROS 2 network configuration is compatible

## 3. AI Integration Issues

### Problem: Whisper fails to recognize speech
**Solution**:
- Check microphone permissions and functionality
- Verify audio input levels: `alsamixer`
- Test audio input: `arecord -d 3 test.wav && play test.wav`
- Ensure OpenAI API key is set: `export OPENAI_API_KEY='your-key'`

### Problem: LLM does not generate appropriate plans
**Solution**:
- Review system prompts for clarity and completeness
- Verify LLM response is properly parsed as JSON
- Check that robot actions exist in the action server
- Implement fallback strategies for ambiguous commands

### Problem: Vision-Language models not processing correctly
**Solution**:
- Verify camera topics are publishing: `ros2 topic echo /camera/image_raw`
- Check image format compatibility
- Ensure proper synchronization between vision and language inputs
- Test vision processing independently before integration

## 4. Performance Issues

### Problem: High latency in voice processing or planning
**Solution**:
- Optimize network calls to LLM services
- Implement caching for frequently requested information
- Consider using faster, smaller models for initial processing
- Optimize audio preprocessing pipeline
- Implement asynchronous processing where possible

### Problem: Robot movement is jerky or unstable
**Solution**:
- Check control loop timing and update rates
- Adjust PID controller parameters
- Verify sensor feedback is timely and accurate
- Confirm actuator commands are within safe ranges

### Problem: System uses too much CPU or memory
**Solution**:
- Monitor resource usage: `htop` or `nvidia-smi`
- Reduce simulation complexity (simpler collision meshes)
- Optimize sensor update rates
- Close unnecessary applications during execution

## 5. Sim-to-Real Transfer Issues

### Problem: Behavior that works in simulation fails on hardware
**Solution**:
- Account for sensor noise and uncertainty in real environments
- Adjust control parameters for real-world dynamics
- Implement proper safety checks before real-world execution
- Calibrate sensors and actuators properly
- Test extensively in simulation with added noise models

### Problem: Physical robot does not follow simulated trajectories
**Solution**:
- Verify robot kinematic model matches physical robot
- Recalibrate sensors and actuators
- Adjust for real-world friction and environmental factors
- Implement robust control methods that handle uncertainties

## 6. Multi-Step Task Execution Issues

### Problem: Complex tasks fail partway through execution
**Solution**:
- Implement proper state tracking and recovery mechanisms
- Add validation checks after each step
- Design tasks with error recovery in mind
- Implement timeouts and fallback behaviors
- Test individual steps before combining into complex tasks

### Problem: System does not respond to voice commands correctly
**Solution**:
- Verify ASR (speech-to-text) accuracy
- Check that NLP correctly parses commands
- Ensure command mapping to robot capabilities is accurate
- Implement error handling for misunderstood commands
- Add confirmation steps for critical commands

## 7. Hardware Issues

### Problem: Jetson Orin Nano not detected or communicating
**Solution**:
- Check physical connections (USB, Ethernet, etc.)
- Verify power supply is adequate
- Confirm correct drivers are installed
- Test basic communication: `ssh jetson@ip_address`
- Ensure ROS 2 setup is correct on the device

### Problem: Sensors not publishing data
**Solution**:
- Check physical connections and power
- Verify driver installation: `lsusb` or `lspci`
- Check topic availability: `ros2 topic list`
- Verify permission settings for sensor access
- Test sensors independently of ROS 2 first

## 8. Development Environment Issues

### Problem: Docusaurus development server not starting
**Solution**:
- Ensure Node.js 18+ is installed: `node --version`
- Install dependencies: `cd book && npm install`
- Clear cache: `npm start -- --clear-cache`
- Check port availability: `sudo lsof -i :3000`

### Problem: Code compilation fails
**Solution**:
- Verify all dependencies are installed
- Check ROS workspace setup: `source install/setup.bash`
- Run `colcon build` in workspace root
- Check for missing package dependencies
- Review compiler error messages for specific issues

## Getting Additional Help

If these troubleshooting steps do not resolve your issue:

1. Check the ROS Answers website: https://answers.ros.org/
2. Review the documentation for each component (ROS 2, Gazebo, Unity, etc.)
3. Search for similar issues in project repositories
4. Verify your setup against the hardware requirements
5. Consider asking for help in relevant community forums

Always include these details when seeking help:
- Operating system version
- ROS 2 version
- Steps to reproduce the issue
- Exact error messages
- What you've tried already