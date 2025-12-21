# Full Capstone System Integration
# This module integrates all components of the humanoid system

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
from sensor_msgs.msg import JointState, LaserScan, Image
from geometry_msgs.msg import Twist, Pose
import json
import time
import threading
from collections import deque

class FullCapstoneSystem(Node):
    def __init__(self):
        super().__init__('full_capstone_system')
        
        # Publishers for all subsystems
        self.nav_goal_pub = self.create_publisher(String, '/navigation/goal', 10)
        self.manip_goal_pub = self.create_publisher(String, '/manipulation/goal', 10)
        self.control_cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.joint_cmd_pub = self.create_publisher(JointState, '/joint_commands', 10)
        self.system_status_pub = self.create_publisher(String, '/capstone/system_status', 10)
        self.sim_real_transfer_pub = self.create_publisher(Bool, '/sim_real_transfer/enable', 10)
        
        # Subscribers for status updates and sensor data
        self.voice_cmd_sub = self.create_subscription(String, '/vla/recognized_text', self.voice_command_callback, 10)
        self.nav_status_sub = self.create_subscription(String, '/navigation/status', self.nav_status_callback, 10)
        self.manip_status_sub = self.create_subscription(String, '/manipulation/status', self.manip_status_callback, 10)
        self.sensor_sub = self.create_subscription(LaserScan, '/scan', self.sensor_callback, 10)
        self.joint_state_sub = self.create_subscription(JointState, '/joint_states', self.joint_state_callback, 10)
        
        # System state variables
        self.current_task_sequence = []
        self.current_step_index = 0
        self.system_active = False
        self.safety_engaged = False
        self.performance_metrics = {
            'navigation_accuracy': 0.0,
            'manipulation_success_rate': 0.0,
            'response_time_avg': 0.0,
            'task_completion_rate': 0.0
        }
        self.metrics_history = deque(maxlen=100)  # Keep last 100 metrics
        
        # Performance monitoring
        self.startup_time = time.time()
        
        self.get_logger().info("Full Capstone System initialized and ready")
        
        # Start performance monitoring in a separate thread
        self.monitoring_thread = threading.Thread(target=self.performance_monitor, daemon=True)
        self.monitoring_thread.start()
    
    def voice_command_callback(self, msg):
        """Process incoming voice commands"""
        self.get_logger().info(f"Received voice command: {msg.data}")
        
        # Check if system is safe to accept commands
        if self.safety_engaged:
            self.get_logger().warn("System in safety mode - rejecting command")
            return
        
        # Parse the command
        try:
            # In a real implementation, this would interface with the VLA pipeline
            # For this example, we'll simulate parsing
            command_plan = self.parse_command(msg.data)
            
            if command_plan:
                self.get_logger().info(f"Executing plan: {command_plan}")
                self.execute_task_sequence(command_plan.get('steps', []))
            else:
                self.get_logger().error("Could not parse command")
        except Exception as e:
            self.get_logger().error(f"Error processing command: {str(e)}")
    
    def parse_command(self, command):
        """Parse natural language commands into executable steps"""
        # This is a simplified parser - in reality, this would use NLP/LLM
        command_lower = command.lower()
        
        if "go to" in command_lower or "navigate to" in command_lower:
            # Determine destination
            if "kitchen" in command_lower:
                return {
                    "command": command,
                    "steps": [
                        {"action": "move_to_location", "parameters": {"location_name": "kitchen"}}
                    ]
                }
            elif "living room" in command_lower:
                return {
                    "command": command,
                    "steps": [
                        {"action": "move_to_location", "parameters": {"location_name": "living_room"}}
                    ]
                }
        
        elif "pick up" in command_lower or "take" in command_lower:
            # Determine object
            if "cup" in command_lower:
                return {
                    "command": command,
                    "steps": [
                        {"action": "pick_up_object", "parameters": {"object_name": "cup"}}
                    ]
                }
            elif "book" in command_lower:
                return {
                    "command": command,
                    "steps": [
                        {"action": "pick_up_object", "parameters": {"object_name": "book"}}
                    ]
                }
        
        elif "go to kitchen then pick up cup" in command_lower:
            return {
                "command": command,
                "steps": [
                    {"action": "move_to_location", "parameters": {"location_name": "kitchen"}},
                    {"action": "pick_up_object", "parameters": {"object_name": "cup"}}
                ]
            }
        
        # Default: unknown command
        return None
    
    def execute_task_sequence(self, steps):
        """Execute a sequence of tasks"""
        if self.system_active:
            self.get_logger().warn("System already executing a task - queueing not implemented")
            return
        
        if len(steps) == 0:
            self.get_logger().warn("No steps to execute")
            return
        
        self.get_logger().info(f"Starting execution of {len(steps)}-step task sequence")
        self.current_task_sequence = steps
        self.current_step_index = 0
        self.system_active = True
        
        # Publish system status
        self.publish_system_status("executing", f"Starting task sequence with {len(steps)} steps")
        
        # Execute first step
        self.execute_current_step()
    
    def execute_current_step(self):
        """Execute the current step in the sequence"""
        if self.current_step_index >= len(self.current_task_sequence):
            self.get_logger().info("All steps completed successfully")
            self.complete_task_sequence()
            return
        
        current_step = self.current_task_sequence[self.current_step_index]
        self.get_logger().info(f"Executing step {self.current_step_index + 1}: {current_step['action']}")
        
        # Based on action type, publish appropriate command
        if current_step['action'] in ['move_to_location', 'walk_forward', 'turn_left', 'turn_right']:
            # Navigation action
            goal_msg = String()
            goal_msg.data = json.dumps(current_step)
            self.nav_goal_pub.publish(goal_msg)
        elif current_step['action'] in ['pick_up_object', 'place_object']:
            # Manipulation action
            goal_msg = String()
            goal_msg.data = json.dumps(current_step)
            self.manip_goal_pub.publish(goal_msg)
        else:
            # Other actions - handle as needed
            self.get_logger().warn(f"Unknown action type: {current_step['action']}")
            self.mark_step_complete()  # Skip unknown actions
    
    def mark_step_complete(self):
        """Mark current step as complete and move to next"""
        self.current_step_index += 1
        
        # Check if all steps are done
        if self.current_step_index < len(self.current_task_sequence):
            # More steps to execute
            self.get_logger().info(f"Completed step {self.current_step_index}, moving to next")
            self.execute_current_step()
        else:
            # All steps completed
            self.get_logger().info("All steps completed successfully")
            self.complete_task_sequence()
    
    def complete_task_sequence(self):
        """Mark task sequence as completed"""
        self.system_active = False
        self.current_task_sequence = []
        self.current_step_index = 0
        
        self.publish_system_status("idle", "Task sequence completed successfully")
        self.get_logger().info("System returned to idle state")
    
    def nav_status_callback(self, msg):
        """Handle navigation status updates"""
        try:
            status_data = json.loads(msg.data)
            status = status_data.get('status', 'unknown')
            
            if status == 'completed':
                self.get_logger().info("Navigation step completed")
                self.mark_step_complete()
            elif status == 'failed':
                self.get_logger().error("Navigation step failed")
                self.publish_system_status("error", "Navigation step failed")
                self.system_active = False
        except json.JSONDecodeError:
            self.get_logger().error("Could not parse navigation status")
    
    def manip_status_callback(self, msg):
        """Handle manipulation status updates"""
        try:
            status_data = json.loads(msg.data)
            status = status_data.get('status', 'unknown')
            
            if status == 'completed':
                self.get_logger().info("Manipulation step completed")
                self.mark_step_complete()
            elif status == 'failed':
                self.get_logger().error("Manipulation step failed")
                self.publish_system_status("error", "Manipulation step failed")
                self.system_active = False
        except json.JSONDecodeError:
            self.get_logger().error("Could not parse manipulation status")
    
    def sensor_callback(self, msg):
        """Process sensor data for safety and environment awareness"""
        # Check for obstacles
        min_distance = min(msg.ranges) if msg.ranges else float('inf')
        
        if min_distance < 0.5:  # Less than 0.5m to obstacle
            if not self.safety_engaged:
                self.get_logger().warn("Obstacle detected, engaging safety mode")
                self.safety_engaged = True
                self.publish_system_status("safety_engaged", f"Obstacle at {min_distance:.2f}m")
                
                # Stop all movement
                stop_cmd = Twist()
                self.control_cmd_pub.publish(stop_cmd)
        
        elif self.safety_engaged and min_distance > 1.0:  # Safety distance restored
            self.get_logger().info("Obstacle cleared, disengaging safety mode")
            self.safety_engaged = False
            self.publish_system_status("safety_restored", "Environment clear")
    
    def joint_state_callback(self, msg):
        """Process joint state data for system monitoring"""
        # This could be used to monitor joint positions, velocities, efforts
        # For now, we'll just log some basic info
        if len(msg.position) > 0:
            self.get_logger().debug(f"Received joint state with {len(msg.position)} joints")
    
    def publish_system_status(self, status, details=""):
        """Publish system status to monitoring systems"""
        status_msg = String()
        status_msg.data = json.dumps({
            "status": status,
            "details": details,
            "active": self.system_active,
            "safety_engaged": self.safety_engaged,
            "current_step": self.current_step_index,
            "total_steps": len(self.current_task_sequence) if self.current_task_sequence else 0,
            "uptime": time.time() - self.startup_time
        })
        self.system_status_pub.publish(status_msg)
    
    def performance_monitor(self):
        """Monitor system performance in background thread"""
        while rclpy.ok():
            # Calculate performance metrics periodically
            time.sleep(5)  # Update metrics every 5 seconds
            
            # In a real system, this would calculate actual metrics
            # For this example, we'll just log the call
            self.get_logger().debug("Performance monitoring tick")

def main(args=None):
    rclpy.init(args=args)
    
    capstone_system = FullCapstoneSystem()
    
    try:
        # Publish initial system ready status
        time.sleep(1)  # Allow publishers to connect
        capstone_system.publish_system_status("ready", "System initialized and ready for commands")
        
        rclpy.spin(capstone_system)
    except KeyboardInterrupt:
        capstone_system.get_logger().info("Full capstone system interrupted by user")
    finally:
        capstone_system.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()