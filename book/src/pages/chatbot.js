import React from 'react';
import Layout from '@theme/Layout';
import Chatbot from '../components/Chatbot';

export default function ChatbotPage() {
  return (
    <Layout title="AI-Humanoid Robotics Chatbot" description="An AI-powered chatbot to help you with the book content">
      <div className="container margin-vert--lg">
        <div className="row">
          <div className="col col--12">
            <h1>AI-Humanoid Robotics Assistant</h1>
            <p>Ask me anything about the AI-Humanoid Robotics book. I can help explain concepts, provide hints for exercises, and point you to relevant resources.</p>
            
            <div className="margin-vert--lg">
              <Chatbot context="general" />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}