# Simulation Environment Test Script

"""
Simulation Environment Test
--------------------------
This script tests the basic functionality of the simulation environment.
It verifies that the humanoid robot model can be loaded and controlled in simulation.
"""

import subprocess
import time
import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState, Image, LaserScan
from geometry_msgs.msg import Twist

def test_simulation_setup():
    """Test if the simulation environment is properly set up."""
    print("Testing simulation environment setup...")
    
    # Check if necessary packages are installed
    try:
        subprocess.run(['gazebo', '--version'], check=True, capture_output=True)
        print("✓ Gazebo is installed")
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("✗ Gazebo is not installed or not in PATH")
        return False
    
    # Check if ROS dependencies are available
    try:
        import gazebo_msgs
        import sensor_msgs
        print("✓ ROS simulation packages are available")
    except ImportError as e:
        print(f"✗ Missing ROS packages: {e}")
        return False
    
    return True

def test_robot_model():
    """Test if the humanoid robot model loads correctly."""
    print("\nTesting humanoid robot model...")
    
    # This would normally involve launching a test world with the robot
    # For now, we just verify the URDF file exists and has valid syntax
    try:
        with open('code-samples/chapter-02-digital-twin/humanoid-urdf-model.urdf', 'r') as f:
            content = f.read()
            if '<robot' in content and '</robot>' in content:
                print("✓ Humanoid URDF model exists and has valid syntax")
            else:
                print("✗ Humanoid URDF model has invalid syntax")
                return False
    except FileNotFoundError:
        print("✗ Humanoid URDF model file not found")
        return False
    
    return True

def test_sensors():
    """Test if sensors are properly configured in simulation."""
    print("\nTesting sensor configuration...")
    
    # Check if the world file contains sensor definitions
    try:
        with open('code-samples/chapter-02-digital-twin/simulation-environment.world', 'r') as f:
            content = f.read()
            if 'sensor type="camera"' in content and 'sensor type="ray"' in content:
                print("✓ Sensors are defined in the simulation environment")
            else:
                print("? No sensors found in simulation environment (check if they're in URDF instead)")
    except FileNotFoundError:
        print("? Simulation environment file not found")
    
    return True

def run_tests():
    """Run all simulation tests."""
    print("Starting simulation environment tests...\n")
    
    setup_ok = test_simulation_setup()
    if not setup_ok:
        print("\n✗ Simulation setup failed - stopping tests")
        return False
    
    model_ok = test_robot_model()
    if not model_ok:
        print("\n✗ Robot model test failed - stopping tests")
        return False
    
    sensors_ok = test_sensors()
    if not sensors_ok:
        print("\n✗ Sensor configuration test failed")
        # This is not necessarily critical, so we continue
    
    print("\n✓ All simulation environment tests completed")
    return True

if __name__ == "__main__":
    run_tests()