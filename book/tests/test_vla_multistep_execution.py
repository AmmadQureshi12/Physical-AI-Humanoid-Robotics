# VLA Multi-Step Command Execution Test

"""
VLA Multi-Step Command Execution Test
--------------------------------------
This script tests the ability of the VLA system to execute multi-step commands.
"""

import rospy
import time
from std_msgs.msg import String
import json

def test_multi_step_commands():
    """Test multi-step command execution in the VLA system."""
    rospy.init_node('vla_tester', anonymous=True)
    
    # Publisher for simulated voice commands
    command_pub = rospy.Publisher('/vla/recognized_text', String, queue_size=10)
    
    # Subscriber for action plans
    action_sub = rospy.Subscriber('/vla/planned_actions', String, action_callback)
    
    rospy.loginfo("VLA Multi-Step Command Execution Test Starting...")
    time.sleep(2)  # Allow publishers/subscribers to connect
    
    # Test case 1: Simple navigation command
    rospy.loginfo("Test 1: Simple navigation command")
    command_msg = String()
    command_msg.data = "Go to the kitchen"
    command_pub.publish(command_msg)
    time.sleep(3)
    
    # Test case 2: Manipulation command
    rospy.loginfo("Test 2: Manipulation command")
    command_msg.data = "Pick up the red cup"
    command_pub.publish(command_msg)
    time.sleep(3)
    
    # Test case 3: Multi-step command
    rospy.loginfo("Test 3: Multi-step command")
    command_msg.data = "Go to the kitchen, pick up the red cup, and bring it to me"
    command_pub.publish(command_msg)
    time.sleep(5)
    
    # Test case 4: Complex command with locomotion
    rospy.loginfo("Test 4: Complex command with locomotion")
    command_msg.data = "Stand up, walk to the table, and sit down"
    command_pub.publish(command_msg)
    time.sleep(5)
    
    rospy.loginfo("All tests completed.")

def action_callback(msg):
    """Callback for receiving action plans"""
    try:
        plan = json.loads(msg.data)
        rospy.loginfo(f"Received action plan: {plan['command']}")
        for i, step in enumerate(plan['steps']):
            rospy.loginfo(f"  Step {i+1}: {step['action']} with params: {step.get('parameters', {})}")
    except json.JSONDecodeError:
        rospy.logerr("Could not parse action plan JSON")

if __name__ == "__main__":
    try:
        test_multi_step_commands()
        rospy.spin()
    except rospy.ROSInterruptException:
        rospy.loginfo("VLA tester shutdown")