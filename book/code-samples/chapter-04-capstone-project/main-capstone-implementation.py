# Main Capstone Implementation
# Complete autonomous humanoid system integration

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Pose, Twist
from sensor_msgs.msg import JointState, Image, LaserScan
from builtin_interfaces.msg import Duration
import json
import time

class CapstoneHumanoidSystem(Node):
    def __init__(self):
        super().__init__('capstone_humanoid_system')
        
        # Publishers for different subsystems
        self.nav_goal_pub = self.create_publisher(String, '/navigation/goal', 10)
        self.manip_goal_pub = self.create_publisher(String, '/manipulation/goal', 10)
        self.control_cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.joint_cmd_pub = self.create_publisher(JointState, '/joint_commands', 10)
        
        # Subscribers for system status
        self.voice_cmd_sub = self.create_subscription(String, '/vla/recognized_text', self.voice_command_callback, 10)
        self.nav_status_sub = self.create_subscription(String, '/navigation/status', self.nav_status_callback, 10)
        self.manip_status_sub = self.create_subscription(String, '/manipulation/status', self.manip_status_callback, 10)
        self.sensor_sub = self.create_subscription(LaserScan, '/scan', self.sensor_callback, 10)
        
        # System state
        self.current_task = None
        self.system_status = "idle"
        self.navigation_active = False
        self.manipulation_active = False
        
        self.get_logger().info("Capstone Humanoid System initialized")
    
    def voice_command_callback(self, msg):
        """Process voice commands and initiate appropriate actions"""
        try:
            self.get_logger().info(f"Received voice command: {msg.data}")
            
            # Parse the command to determine required actions
            command_plan = self.parse_command(msg.data)
            
            if command_plan:
                self.get_logger().info(f"Command plan: {command_plan}")
                self.execute_plan(command_plan)
            else:
                self.get_logger().error("Could not parse command")
                
        except Exception as e:
            self.get_logger().error(f"Error processing voice command: {str(e)}")
    
    def parse_command(self, command):
        """Parse natural language command into executable actions"""
        # In a real implementation, this would use the cognitive planner
        # For this example, we'll implement simple parsing
        command = command.lower()
        
        if "navigate" in command or "go to" in command or "move to" in command:
            # Extract destination if possible
            if "kitchen" in command:
                return {"action": "navigate", "destination": "kitchen"}
            elif "living room" in command:
                return {"action": "navigate", "destination": "living_room"}
            else:
                return {"action": "navigate", "destination": "unknown"}
        
        elif "pick up" in command or "grasp" in command or "take" in command:
            # Extract object if possible
            if "cup" in command:
                return {"action": "manipulate", "task": "pick_up", "object": "cup"}
            elif "book" in command:
                return {"action": "manipulate", "task": "pick_up", "object": "book"}
            else:
                return {"action": "manipulate", "task": "pick_up", "object": "unknown"}
        
        elif "place" in command or "put" in command:
            return {"action": "manipulate", "task": "place", "object": "held_object"}
        
        elif "stop" in command or "halt" in command:
            return {"action": "stop"}
        
        else:
            return {"action": "unknown", "command": command}
    
    def execute_plan(self, plan):
        """Execute the parsed plan"""
        action = plan.get('action')
        
        if action == "navigate":
            self.execute_navigation(plan)
        elif action == "manipulate":
            self.execute_manipulation(plan)
        elif action == "stop":
            self.execute_stop()
        else:
            self.get_logger().warn(f"Unknown action: {action}")
    
    def execute_navigation(self, plan):
        """Execute navigation task"""
        self.get_logger().info(f"Executing navigation to: {plan.get('destination')}")
        
        # Set navigation active flag
        self.navigation_active = True
        self.system_status = "navigating"
        
        # Publish navigation goal
        goal_msg = String()
        goal_msg.data = json.dumps(plan)
        self.nav_goal_pub.publish(goal_msg)
        
        # Simple timeout mechanism
        timeout_start = time.time()
        timeout = 30  # seconds
        
        while self.navigation_active and time.time() - timeout_start < timeout:
            time.sleep(0.5)  # Check status every 0.5 seconds
        
        if self.navigation_active:
            self.get_logger().warn("Navigation timeout - stopping")
            self.execute_stop()
    
    def execute_manipulation(self, plan):
        """Execute manipulation task"""
        self.get_logger().info(f"Executing manipulation: {plan.get('task')} {plan.get('object', '')}")
        
        # Set manipulation active flag
        self.manipulation_active = True
        self.system_status = "manipulating"
        
        # Publish manipulation goal
        goal_msg = String()
        goal_msg.data = json.dumps(plan)
        self.manip_goal_pub.publish(goal_msg)
        
        # Simple timeout mechanism
        timeout_start = time.time()
        timeout = 30  # seconds
        
        while self.manipulation_active and time.time() - timeout_start < timeout:
            time.sleep(0.5)  # Check status every 0.5 seconds
        
        if self.manipulation_active:
            self.get_logger().warn("Manipulation timeout - stopping")
            self.execute_stop()
    
    def execute_stop(self):
        """Stop all ongoing activities"""
        self.get_logger().info("Stopping all activities")
        
        # Publish stop command
        stop_msg = Twist()
        self.control_cmd_pub.publish(stop_msg)
        
        # Reset flags
        self.navigation_active = False
        self.manipulation_active = False
        self.system_status = "idle"
        
        # Publish stop to all subsystems
        stop_cmd = String()
        stop_cmd.data = json.dumps({"action": "stop"})
        self.nav_goal_pub.publish(stop_cmd)
        self.manip_goal_pub.publish(stop_cmd)
    
    def nav_status_callback(self, msg):
        """Handle navigation system status updates"""
        try:
            status_data = json.loads(msg.data)
            status = status_data.get('status', 'unknown')
            
            if status == 'completed':
                self.get_logger().info("Navigation completed")
                self.navigation_active = False
                self.system_status = "idle"
            elif status == 'failed':
                self.get_logger().warn("Navigation failed")
                self.navigation_active = False
                self.system_status = "idle"
        except json.JSONDecodeError:
            self.get_logger().error("Could not parse navigation status")
    
    def manip_status_callback(self, msg):
        """Handle manipulation system status updates"""
        try:
            status_data = json.loads(msg.data)
            status = status_data.get('status', 'unknown')
            
            if status == 'completed':
                self.get_logger().info("Manipulation completed")
                self.manipulation_active = False
                self.system_status = "idle"
            elif status == 'failed':
                self.get_logger().warn("Manipulation failed")
                self.manipulation_active = False
                self.system_status = "idle"
        except json.JSONDecodeError:
            self.get_logger().error("Could not parse manipulation status")
    
    def sensor_callback(self, msg):
        """Handle sensor data for obstacle avoidance and safety"""
        # Process laser scan for obstacle detection
        # In a real implementation, this would feed into navigation safety
        pass

def main(args=None):
    rclpy.init(args=args)
    
    capstone_system = CapstoneHumanoidSystem()
    
    try:
        rclpy.spin(capstone_system)
    except KeyboardInterrupt:
        capstone_system.get_logger().info("Capstone system interrupted by user")
    finally:
        capstone_system.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()