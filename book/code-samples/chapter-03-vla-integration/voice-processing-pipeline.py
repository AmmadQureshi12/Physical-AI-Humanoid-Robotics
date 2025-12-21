# Voice Processing Pipeline with OpenAI Whisper
# This demonstrates how to set up a voice processing pipeline for robotic applications

import os
import rospy
import speech_recognition as sr
from std_msgs.msg import String
import openai
from openai import OpenAI

class VoiceProcessingPipeline:
    def __init__(self):
        # Initialize ROS node for voice processing
        rospy.init_node('voice_processing_pipeline', anonymous=True)
        
        # Publisher for recognized text
        self.text_pub = rospy.Publisher('/vla/recognized_text', String, queue_size=10)
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Set up OpenAI client (requires API key)
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Adjust for ambient noise
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        
        rospy.loginfo("Voice Processing Pipeline initialized")
    
    def listen_and_transcribe(self):
        """Listen to audio and transcribe using Whisper"""
        try:
            rospy.loginfo("Listening for audio...")
            with self.microphone as source:
                # Listen for audio with timeout
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            rospy.loginfo("Audio captured, sending to Whisper for transcription...")
            
            # Save audio to temporary file for Whisper API
            with open("temp_audio.wav", "wb") as f:
                f.write(audio.get_wav_data())
            
            # Use OpenAI Whisper API for transcription
            with open("temp_audio.wav", "rb") as audio_file:
                transcript = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            
            # Remove temporary file
            os.remove("temp_audio.wav")
            
            rospy.loginfo(f"Transcribed text: {transcript.text}")
            return transcript.text
            
        except sr.WaitTimeoutError:
            rospy.logwarn("Timeout: No audio detected")
            return None
        except sr.UnknownValueError:
            rospy.logwarn("Whisper could not understand audio")
            return None
        except Exception as e:
            rospy.logerr(f"Error in transcription: {str(e)}")
            return None
    
    def run(self):
        """Main loop for voice processing"""
        rate = rospy.Rate(1)  # Process audio every second
        
        while not rospy.is_shutdown():
            # Get transcribed text
            text = self.listen_and_transcribe()
            
            if text:
                # Publish the recognized text
                text_msg = String()
                text_msg.data = text
                self.text_pub.publish(text_msg)
                
                rospy.loginfo(f"Published recognized text: {text}")
            else:
                rospy.loginfo("No text recognized, continuing...")
            
            rate.sleep()

if __name__ == '__main__':
    try:
        vpp = VoiceProcessingPipeline()
        vpp.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Voice Processing Pipeline shutdown")