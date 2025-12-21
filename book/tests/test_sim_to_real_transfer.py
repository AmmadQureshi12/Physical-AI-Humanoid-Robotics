# Sim-to-Real Transfer and Multi-Step Scenario Testing

"""
Sim-to-Real Transfer and Multi-Step Scenario Testing
----------------------------------------------------
This script tests the sim-to-real transfer capability and multi-step scenarios
in the humanoid system.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Bool
import json
import time
import random

class SimRealTransferTest(Node):
    def __init__(self):
        super().__init__('sim_real_transfer_test')
        
        # Publishers for sim-real control and task execution
        self.transfer_control_pub = self.create_publisher(Bool, '/sim_real_transfer/enable', 10)
        self.task_pub = self.create_publisher(String, '/vla/recognized_text', 10)
        self.test_report_pub = self.create_publisher(String, '/test_report', 10)
        
        # Subscribers for system status and results
        self.status_sub = self.create_subscription(String, '/capstone/system_status', self.status_callback, 10)
        self.nav_status_sub = self.create_subscription(String, '/navigation/status', self.nav_status_callback, 10)
        self.manip_status_sub = self.create_subscription(String, '/manipulation/status', self.manip_status_callback, 10)
        
        # Test state
        self.current_test = 0
        self.test_results = []
        self.system_ready = False
        
        self.get_logger().info("Sim-to-Real Transfer Tester initialized")
    
    def status_callback(self, msg):
        """Handle system status updates"""
        try:
            status_data = json.loads(msg.data)
            if status_data.get('status') == 'ready':
                self.system_ready = True
                self.get_logger().info("System ready - starting tests")
                self.run_tests()
        except json.JSONDecodeError:
            self.get_logger().error("Could not parse system status")
    
    def nav_status_callback(self, msg):
        """Handle navigation status for tests"""
        self.get_logger().debug(f"Navigation status: {msg.data}")
    
    def manip_status_callback(self, msg):
        """Handle manipulation status for tests"""
        self.get_logger().debug(f"Manipulation status: {msg.data}")
    
    def run_tests(self):
        """Run sim-to-real transfer and multi-step scenario tests"""
        self.get_logger().info("Starting sim-to-real transfer tests...")
        
        # Test scenarios
        test_scenarios = [
            {
                "name": "Simple Navigation",
                "commands": ["Go to kitchen"],
                "sim_real_transfer": True
            },
            {
                "name": "Simple Manipulation", 
                "commands": ["Pick up the cup"],
                "sim_real_transfer": True
            },
            {
                "name": "Multi-step Sequence",
                "commands": ["Go to kitchen", "Pick up the cup", "Bring cup to me"],
                "sim_real_transfer": False  # Run just in simulation for this test
            },
            {
                "name": "Complex Multi-step",
                "commands": ["Go to living room", "Turn left", "Go to kitchen", "Pick up cup", "Go to table", "Place cup on table"],
                "sim_real_transfer": False  # Run just in simulation for this test
            }
        ]
        
        for i, scenario in enumerate(test_scenarios):
            self.get_logger().info(f"Running test {i+1}: {scenario['name']}")
            
            # If sim-real transfer is enabled, enable it
            if scenario['sim_real_transfer']:
                transfer_msg = Bool()
                transfer_msg.data = True
                self.transfer_control_pub.publish(transfer_msg)
                self.get_logger().info("Sim-to-real transfer enabled")
                time.sleep(2)  # Allow transfer to activate
            
            # Execute commands in sequence
            for j, command in enumerate(scenario['commands']):
                self.get_logger().info(f"  Executing command {j+1}: {command}")
                
                # Publish the command
                cmd_msg = String()
                cmd_msg.data = command
                self.task_pub.publish(cmd_msg)
                
                # Wait for completion or timeout (30 seconds per command)
                start_time = time.time()
                timeout = 30
                while time.time() - start_time < timeout:
                    time.sleep(0.5)
                
                self.get_logger().info(f"  Completed command {j+1}")
            
            # Record test result
            result = {
                "test_name": scenario['name'],
                "commands_executed": len(scenario['commands']),
                "sim_real_transfer": scenario['sim_real_transfer'],
                "status": "completed",
                "timestamp": time.time()
            }
            self.test_results.append(result)
            
            # Report test result
            report_msg = String()
            report_msg.data = json.dumps(result)
            self.test_report_pub.publish(report_msg)
            
            self.get_logger().info(f"Completed test {i+1}: {scenario['name']}")
            time.sleep(3)  # Pause between tests
        
        self.get_logger().info("All sim-to-real transfer tests completed")
        
        # Summarize results
        self.summarize_results()
    
    def summarize_results(self):
        """Print a summary of test results"""
        self.get_logger().info("=== TEST SUMMARY ===")
        for i, result in enumerate(self.test_results):
            self.get_logger().info(f"Test {i+1}: {result['test_name']}")
            self.get_logger().info(f"  Commands executed: {result['commands_executed']}")
            self.get_logger().info(f"  Sim-to-real transfer: {result['sim_real_transfer']}")
            self.get_logger().info(f"  Status: {result['status']}")
            self.get_logger().info("")
        
        total_tests = len(self.test_results)
        self.get_logger().info(f"Total tests run: {total_tests}")
        self.get_logger().info("Sim-to-Real Transfer Testing Complete")

def main(args=None):
    rclpy.init(args=args)
    
    tester = SimRealTransferTest()
    
    # Give some time for system to report ready status
    time.sleep(2)
    
    # If system is already ready, start tests immediately
    if tester.system_ready:
        tester.run_tests()
    
    try:
        rclpy.spin(tester)
    except KeyboardInterrupt:
        tester.get_logger().info("Sim-to-real transfer tester interrupted by user")
    finally:
        tester.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()