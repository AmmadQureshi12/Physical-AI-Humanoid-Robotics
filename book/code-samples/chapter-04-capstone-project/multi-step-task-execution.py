# Multi-Step Task Execution
# Implementation for executing complex multi-step tasks

import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import time

class MultiStepTaskExecutor(Node):
    def __init__(self):
        super().__init__('multi_step_task_executor')
        
        # Publishers for different subsystems
        self.nav_goal_pub = self.create_publisher(String, '/navigation/goal', 10)
        self.manip_goal_pub = self.create_publisher(String, '/manipulation/goal', 10)
        self.status_pub = self.create_publisher(String, '/multi_step/status', 10)
        
        # Subscribers for system status
        self.task_sub = self.create_subscription(String, '/vla/planned_actions', self.task_callback, 10)
        self.nav_status_sub = self.create_subscription(String, '/navigation/status', self.nav_status_callback, 10)
        self.manip_status_sub = self.create_subscription(String, '/manipulation/status', self.manip_status_callback, 10)
        
        # Task execution state
        self.current_task_sequence = []
        self.current_step_index = 0
        self.execution_active = False
        self.step_completed = False
        
        self.get_logger().info("Multi-Step Task Executor initialized")
    
    def task_callback(self, msg):
        """Process incoming multi-step tasks"""
        try:
            plan = json.loads(msg.data)
            self.get_logger().info(f"Received multi-step task: {plan['command']}")
            
            # Validate that this is a multi-step task
            steps = plan.get('steps', [])
            if len(steps) == 0:
                self.get_logger().warn("Received task with no steps")
                return
            
            # Initialize execution of the task sequence
            self.start_task_sequence(steps)
            
        except json.JSONDecodeError:
            self.get_logger().error("Could not parse task JSON")
        except Exception as e:
            self.get_logger().error(f"Error processing task: {str(e)}")
    
    def start_task_sequence(self, steps):
        """Start execution of a sequence of tasks"""
        self.get_logger().info(f"Starting execution of {len(steps)}-step task sequence")
        
        self.current_task_sequence = steps
        self.current_step_index = 0
        self.execution_active = True
        self.step_completed = False
        
        # Publish status
        status_msg = String()
        status_msg.data = json.dumps({
            "status": "started",
            "current_task": self.current_task_sequence[0]['action'],
            "step": 1,
            "total_steps": len(self.current_task_sequence)
        })
        self.status_pub.publish(status_msg)
        
        # Execute the first step
        self.execute_current_step()
    
    def execute_current_step(self):
        """Execute the current step in the sequence"""
        if self.current_step_index >= len(self.current_task_sequence):
            self.get_logger().info("All steps completed successfully")
            self.complete_task_sequence()
            return
        
        current_step = self.current_task_sequence[self.current_step_index]
        self.get_logger().info(f"Executing step {self.current_step_index + 1}: {current_step['action']}")
        
        # Execute based on action type
        if current_step['action'] == 'move_to_location':
            self.execute_navigation_step(current_step)
        elif current_step['action'] == 'pick_up_object':
            self.execute_manipulation_step(current_step)
        elif current_step['action'] == 'place_object':
            self.execute_manipulation_step(current_step)
        elif current_step['action'] == 'stand_up' or current_step['action'] == 'sit_down':
            self.execute_locomotion_step(current_step)
        else:
            self.get_logger().warn(f"Unknown action: {current_step['action']}")
            self.mark_step_complete()
    
    def execute_navigation_step(self, step):
        """Execute navigation step"""
        self.get_logger().info(f"Executing navigation: {step['parameters']}")
        
        # Publish navigation goal
        goal_msg = String()
        goal_msg.data = json.dumps(step)
        self.nav_goal_pub.publish(goal_msg)
        
        # Set step as waiting for completion
        self.step_completed = False
    
    def execute_manipulation_step(self, step):
        """Execute manipulation step"""
        self.get_logger().info(f"Executing manipulation: {step['parameters']}")
        
        # Publish manipulation goal
        goal_msg = String()
        goal_msg.data = json.dumps(step)
        self.manip_goal_pub.publish(goal_msg)
        
        # Set step as waiting for completion
        self.step_completed = False
    
    def execute_locomotion_step(self, step):
        """Execute locomotion step"""
        self.get_logger().info(f"Executing locomotion: {step['action']}")
        
        # For this example, just mark as completed immediately
        # In a real implementation, this would interface with locomotion control
        self.mark_step_complete()
    
    def nav_status_callback(self, msg):
        """Handle navigation status updates"""
        try:
            status_data = json.loads(msg.data)
            status = status_data.get('status', 'unknown')
            
            if status == 'completed':
                self.get_logger().info("Navigation step completed")
                self.mark_step_complete()
            elif status == 'failed':
                self.get_logger().warn("Navigation step failed")
                self.fail_task_sequence()
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
                self.get_logger().warn("Manipulation step failed")
                self.fail_task_sequence()
        except json.JSONDecodeError:
            self.get_logger().error("Could not parse manipulation status")
    
    def mark_step_complete(self):
        """Mark the current step as completed and proceed to next"""
        self.step_completed = True
        self.current_step_index += 1
        
        # Publish step completion status
        step_status = {
            "status": "step_completed",
            "completed_step": self.current_task_sequence[self.current_step_index - 1]['action'],
            "next_step": None,
            "step": self.current_step_index,
            "total_steps": len(self.current_task_sequence)
        }
        
        if self.current_step_index < len(self.current_task_sequence):
            step_status["next_step"] = self.current_task_sequence[self.current_step_index]['action']
        
        status_msg = String()
        status_msg.data = json.dumps(step_status)
        self.status_pub.publish(status_msg)
        
        # If there are more steps, execute the next one
        if self.current_step_index < len(self.current_task_sequence):
            self.execute_current_step()
        else:
            self.get_logger().info("All steps completed successfully")
            self.complete_task_sequence()
    
    def complete_task_sequence(self):
        """Complete the entire task sequence"""
        self.get_logger().info("Task sequence completed successfully")
        
        # Publish completion status
        status_msg = String()
        status_msg.data = json.dumps({
            "status": "completed",
            "message": "All steps completed successfully"
        })
        self.status_pub.publish(status_msg)
        
        # Reset execution state
        self.current_task_sequence = []
        self.current_step_index = 0
        self.execution_active = False
        self.step_completed = False
    
    def fail_task_sequence(self):
        """Handle failure of the task sequence"""
        self.get_logger().error("Task sequence failed")
        
        # Publish failure status
        status_msg = String()
        status_msg.data = json.dumps({
            "status": "failed",
            "message": f"Failed at step {self.current_step_index + 1}: {self.current_task_sequence[self.current_step_index]['action']}"
        })
        self.status_pub.publish(status_msg)
        
        # Reset execution state
        self.current_task_sequence = []
        self.current_step_index = 0
        self.execution_active = False
        self.step_completed = False

def main(args=None):
    rclpy.init(args=args)
    
    executor = MultiStepTaskExecutor()
    
    try:
        rclpy.spin(executor)
    except KeyboardInterrupt:
        executor.get_logger().info("Multi-step task executor interrupted by user")
    finally:
        executor.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()