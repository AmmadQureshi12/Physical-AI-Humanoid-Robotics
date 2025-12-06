# Cognitive Planner for VLA Systems
# This module plans multi-step tasks based on voice commands using LLMs

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Pose
import json
import openai
from openai import OpenAI
import os

class CognitivePlanner:
    def __init__(self):
        # Initialize ROS node for cognitive planning
        rospy.init_node('cognitive_planner', anonymous=True)
        
        # Subscriber for recognized text from voice processing
        self.text_sub = rospy.Subscriber('/vla/recognized_text', String, self.text_callback)
        
        # Publisher for planned actions
        self.action_pub = rospy.Publisher('/vla/planned_actions', String, queue_size=10)
        
        # Set up OpenAI client (requires API key)
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Store previous context
        self.context = ""
        
        rospy.loginfo("Cognitive Planner initialized")
    
    def text_callback(self, msg):
        """Process recognized text and generate plan"""
        rospy.loginfo(f"Received text for planning: {msg.data}")
        
        # Generate plan using LLM
        plan = self.generate_plan(msg.data)
        
        if plan:
            # Publish the planned actions
            action_msg = String()
            action_msg.data = json.dumps(plan)
            self.action_pub.publish(action_msg)
            
            rospy.loginfo(f"Published planned actions: {plan}")
        else:
            rospy.logwarn("Could not generate plan for the given command")
    
    def generate_plan(self, command):
        """Generate a plan for the given command using LLM"""
        try:
            # Define the system prompt for the LLM
            system_prompt = """
            You are an AI assistant that helps plan robot actions based on natural language commands.
            Your task is to decompose high-level commands into a sequence of specific robot actions.
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
            
            Each step should be a specific, executable action. Keep the plan simple and focused.
            """
            
            # Create the prompt with the user command
            user_prompt = f"Command: {command}"
            
            # Call the OpenAI API to generate the plan
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            # Extract the plan from the response
            plan_text = response.choices[0].message.content
            
            # Clean up the response to extract JSON
            plan_text = plan_text.strip()
            if plan_text.startswith("```json"):
                plan_text = plan_text[7:]  # Remove starting ```json
            if plan_text.endswith("```"):
                plan_text = plan_text[:-3]  # Remove ending ```
            
            # Parse the JSON plan
            plan = json.loads(plan_text)
            
            return plan
        
        except json.JSONDecodeError:
            rospy.logerr("Could not parse JSON from LLM response")
            return None
        except Exception as e:
            rospy.logerr(f"Error generating plan: {str(e)}")
            return None
    
    def run(self):
        """Run the cognitive planner"""
        rospy.loginfo("Cognitive Planner is running...")
        rospy.spin()

if __name__ == '__main__':
    try:
        cp = CognitivePlanner()
        cp.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Cognitive Planner shutdown")