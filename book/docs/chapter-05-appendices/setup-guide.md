# Comprehensive Setup Guide for AI-Humanoid Robotics Curriculum

## Overview

This guide provides step-by-step instructions for setting up the complete AI-Humanoid Robotics development environment. The curriculum requires several technologies to be installed and configured properly to work together.

## Prerequisites

- Ubuntu 22.04 LTS (recommended) or compatible Linux distribution
- At least 16GB RAM (32GB recommended for simulation)
- NVIDIA GPU with CUDA support (RTX 4070 Ti recommended)
- Minimum 200GB free disk space
- Internet connection for package downloads

## 1. ROS 2 Humble Hawksbill Installation

1. Set up locale:
   ```bash
   sudo locale-gen en_US.UTF-8
   ```

2. Add ROS 2 repository:
   ```bash
   sudo apt update && sudo apt install -y software-properties-common
   sudo add-apt-repository universe
   sudo apt update && sudo apt install curl -y
   sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
   echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
   ```

3. Install ROS 2 Humble:
   ```bash
   sudo apt update
   sudo apt install ros-humble-desktop
   sudo apt install python3-rosdep
   ```

4. Initialize rosdep:
   ```bash
   sudo rosdep init
   rosdep update
   ```

5. Source the ROS 2 installation:
   ```bash
   echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
   source ~/.bashrc
   ```

## 2. Gazebo Installation

1. Install Gazebo Garden (recommended version):
   ```bash
   wget https://packages.osrfoundation.org/gazebo.gpg -O /tmp/gazebo.gpg
   sudo cp /tmp/gazebo.gpg /usr/share/keyrings/
   echo "deb [arch=amd64 signed-by=/usr/share/keyrings/gazebo.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
   sudo apt update
   sudo apt install gz-garden
   ```

## 3. Unity 2022.3 LTS Installation

1. Download Unity Hub from: https://unity.com/download
2. Install Unity Hub:
   ```bash
   chmod +x UnityHub.AppImage
   ./UnityHub.AppImage
   ```

2. Through Unity Hub, install Unity 2022.3 LTS version
3. Install the following modules:
   - Android Build Support (if needed)
   - iOS Build Support (if needed)
   - Linux Build Support

## 4. NVIDIA Isaac ROS Tools

1. Install NVIDIA drivers (if not already installed):
   ```bash
   sudo apt install nvidia-driver-535
   sudo reboot
   ```

2. Install CUDA:
   ```bash
   wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
   sudo dpkg -i cuda-keyring_1.0-1_all.deb
   sudo apt-get update
   sudo apt-get -y install cuda
   ```

3. Install Isaac ROS packages:
   ```bash
   sudo apt update
   sudo apt install ros-humble-isaac-ros-suite
   ```

## 5. OpenAI Whisper Installation

1. Install Python dependencies:
   ```bash
   sudo apt install python3-pip python3-venv
   python3 -m venv ~/whisper_env
   source ~/whisper_env/bin/activate
   pip install openai-whisper
   ```

## 6. Docusaurus Setup

1. Install Node.js (v18 or higher):
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs
   ```

2. Install Yarn:
   ```bash
   npm install -g yarn
   ```

3. Create and set up Docusaurus project:
   ```bash
   cd ~/AI-humanoid-robotices/book
   npm install
   ```

## 7. Project Workspace Setup

1. Create ROS 2 workspace:
   ```bash
   mkdir -p ~/humanoid_ws/src
   cd ~/humanoid_ws
   colcon build
   source install/setup.bash
   echo "source ~/humanoid_ws/install/setup.bash" >> ~/.bashrc
   ```

2. Clone necessary repositories:
   ```bash
   cd ~/humanoid_ws/src
   git clone https://github.com/ros-planning/navigation2.git
   git clone https://github.com/ros-planning/moveit2.git
   git clone https://github.com/NVIDIA/isaac_ros_common.git
   ```

## 8. Environment Validation

1. Test basic ROS 2 functionality:
   ```bash
   source /opt/ros/humble/setup.bash
   ros2 topic list
   ```

2. Test Gazebo:
   ```bash
   gz sim
   ```

3. Test Python environment:
   ```bash
   source ~/whisper_env/bin/activate
   python -c "import whisper; print('Whisper installed successfully')"
   ```

## Troubleshooting Common Issues

### ROS 2 Installation Issues
- If package installation fails, ensure your Ubuntu version is supported
- Check that your locale settings are correct
- Verify that your system time is synchronized (NTP)

### GPU/CUDA Issues
- If CUDA is not recognized, verify NVIDIA drivers are properly installed
- Check CUDA installation: `nvidia-smi` and `nvcc --version`
- For Isaac packages, ensure correct CUDA version compatibility

### Audio Setup for Whisper
- Install audio packages: `sudo apt install alsa-utils pulseaudio`
- Test audio input: `arecord -d 3 test.wav && play test.wav`

## Hardware Validation

After completing the software setup, validate your system with the following hardware requirements:

- RTX 4070 Ti: Run `nvidia-smi` to confirm detection
- Jetson Orin Nano: Connect and test with `lsusb` or direct connection
- Robot hardware: Connect and confirm ROS 2 can interface with actuators/sensors

## Next Steps

Once this setup is complete, you can:
1. Run the simulation environment: `cd ~/AI-humanoid-robotices/book && npm run start`
2. Execute the ROS 2 simulation: `source ~/humanoid_ws/install/setup.bash && ros2 launch ...`
3. Begin with Chapter 1: ROS 2 Fundamentals

For additional help, refer to the troubleshooting guides in each chapter or the dedicated troubleshooting section of this curriculum.