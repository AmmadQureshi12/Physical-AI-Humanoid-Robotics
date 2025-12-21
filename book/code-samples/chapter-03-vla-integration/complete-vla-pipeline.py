# Complete VLA Pipeline Integration
# This demonstrates the complete integration of vision, language, and action components

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from std_msgs.msg import String
import json
import openai
from openai import OpenAI
import os
import numpy as np
from geometry_msgs.msg import Pose

class VLAPipeline:
    def __init__(self):
        # Initialize ROS node for the complete VLA pipeline
        rospy.init_node('vla_pipeline', anonymous=True)
        
        # Initialize OpenAI client
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Bridge for converting ROS images to OpenCV
        self.bridge = CvBridge()
        
        # Publishers and subscribers
        self.voice_sub = rospy.Subscriber('/vla/recognized_text', String, self.voice_callback)
        self.image_sub = rospy.Subscriber('/camera/image_raw', Image, self.image_callback)
        self.action_pub = rospy.Publisher('/vla/planned_actions', String, queue_size=10)
        
        # Store latest image for vision processing
        self.latest_image = None
        
        # Store conversation context
        self.conversation_context = []
        
        rospy.loginfo("VLA Pipeline initialized")
    
    def image_callback(self, msg):
        """Process incoming camera images"""
        try:
            # Convert ROS image message to OpenCV image
            cv_image = self.bridge.imgmsg_to_cv2(msg, "bgr8")
            self.latest_image = cv_image
            rospy.loginfo("Received new image")
        except Exception as e:
            rospy.logerr(f"Error converting image: {str(e)}")
    
    def voice_callback(self, msg):
        """Process voice commands with vision context"""
        rospy.loginfo(f"Received voice command: {msg.data}")
        
        # Process the command with vision context
        self.process_command_with_vision(msg.data)
    
    def process_command_with_vision(self, command):
        """Process command using both voice and vision inputs"""
        try:
            # Prepare the vision + language prompt
            system_prompt = """
            You are an AI assistant for a robot with vision and language capabilities. 
            The robot has cameras to see its environment and can understand natural language commands.
            Based on the user's command and the visual environment, determine the appropriate robot actions.
            
            The robot has the following capabilities:
            1. Navigation: move_to_location(location_name)
            2. Manipulation: pick_up_object(object_name), place_object(object_name, location_name)
            3. Locomotion: stand_up(), sit_down(), walk_forward(distance), turn_left(), turn_right()
            4. Perception: look_for_object(object_name), detect_person()
            
            Respond with a JSON object containing:
            {
              "command": "original command",
              "steps": [
                {
                  "action": "action_name",
                  "parameters": {"param_name": "param_value", ...}
                }
              ]
            }
            """
            
            # Prepare the user prompt with visual context if available
            if self.latest_image is not None:
                # In a real implementation, we would use a vision-language model
                # like GPT-4V or similar to analyze the image
                user_prompt = f"Command: {command}\n\nVisual context: The robot sees its environment."
            else:
                user_prompt = f"Command: {command}\n\nVisual context: No image available."
            
            # Add conversation history for context
            messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            # Add recent conversation history
            for msg in self.conversation_context[-5:]:  # Last 5 exchanges
                messages.append(msg)
            
            # Add the current prompt
            messages.append({"role": "user", "content": user_prompt})
            
            # Call the OpenAI API
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.3,
                max_tokens=500
            )
            
            # Extract the plan from the response
            plan_text = response.choices[0].message.content
            plan_text = plan_text.strip()
            if plan_text.startswith("```json"):
                plan_text = plan_text[7:]  # Remove starting ```json
            if plan_text.endswith("```"):
                plan_text = plan_text[:-3]  # Remove ending ```
            
            # Parse the JSON plan
            plan = json.loads(plan_text)
            
            # Add to conversation history
            self.conversation_context.append({"role": "user", "content": user_prompt})
            self.conversation_context.append({"role": "assistant", "content": plan_text})
            
            # Limit conversation history to prevent it from growing too large
            if len(self.conversation_context) > 20:
                self.conversation_context = self.conversation_context[-20:]
            
            # Publish the planned actions
            action_msg = String()
            action_msg.data = json.dumps(plan)
            self.action_pub.publish(action_msg)
            
            rospy.loginfo(f"Published VLA plan: {plan}")
            
        except json.JSONDecodeError:
            rospy.logerr("Could not parse JSON from LLM response")
        except Exception as e:
            rospy.logerr(f"Error in VLA processing: {str(e)}")
    
    def run(self):
        """Run the VLA pipeline"""
        rospy.loginfo("VLA Pipeline is running...")
        rospy.spin()

if __name__ == '__main__':
    try:
        vla_pipeline = VLAPipeline()
        vla_pipeline.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("VLA Pipeline shutdown")