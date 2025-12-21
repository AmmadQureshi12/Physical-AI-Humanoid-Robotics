# Joint Control Node
# This demonstrates how to control a simulated joint using ROS 2

"""
Joint Control Node
------------------
This node demonstrates controlling a simulated joint in ROS 2.
It publishes joint position commands to control a robot joint.
"""

import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState


class JointController(Node):

    def __init__(self):
        super().__init__('joint_controller')
        
        # Publisher for joint commands
        self.joint_cmd_publisher = self.create_publisher(
            Float64,
            '/joint_position_controller/commands',
            10
        )
        
        # Subscriber for joint states
        self.joint_state_subscriber = self.create_subscription(
            JointState,
            '/joint_states',
            self.joint_state_callback,
            10
        )
        
        # Timer for publishing commands
        timer_period = 0.1  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        self.joint_position = 0.0
        self.direction = 1  # 1 for positive, -1 for negative movement
        
        self.get_logger().info('Joint Controller node initialized')

    def joint_state_callback(self, msg):
        # Update current joint position
        for i, name in enumerate(msg.name):
            if name == 'joint_name':  # Replace with actual joint name
                self.joint_position = msg.position[i]
                break

    def timer_callback(self):
        # Simple oscillating movement
        cmd_msg = Float64()
        cmd_msg.data = self.joint_position + (0.1 * self.direction)
        
        # Reverse direction at limits
        if cmd_msg.data > 1.5:
            self.direction = -1
        elif cmd_msg.data < -1.5:
            self.direction = 1
            
        self.joint_cmd_publisher.publish(cmd_msg)
        self.get_logger().info(f'Publishing joint command: {cmd_msg.data}')


def main(args=None):
    rclpy.init(args=args)

    joint_controller = JointController()

    rclpy.spin(joint_controller)

    # Destroy the node explicitly
    joint_controller.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()