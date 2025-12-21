import React, { useState } from 'react';
import Chatbot from '../components/Chatbot/Chatbot';

const DocWithChatbot = ({ children, context }) => {
  const [showChatbot, setShowChatbot] = useState(false);

  return (
    <div style={{ position: 'relative' }}>
      <div style={{ marginBottom: showChatbot ? '520px' : '20px' }}>
        {children}
      </div>
      
      <div style={{
        position: 'fixed',
        bottom: '20px',
        right: '20px',
        zIndex: 1000
      }}>
        <button 
          onClick={() => setShowChatbot(!showChatbot)}
          style={{
            backgroundColor: '#2563eb',
            color: 'white',
            border: 'none',
            borderRadius: '50%',
            width: '60px',
            height: '60px',
            fontSize: '24px',
            cursor: 'pointer',
            boxShadow: '0 4px 8px rgba(0,0,0,0.2)'
          }}
        >
          💬
        </button>
        
        {showChatbot && (
          <div style={{
            position: 'absolute',
            bottom: '70px',
            right: '0',
            width: '400px',
            height: '500px'
          }}>
            <Chatbot context={context} />
          </div>
        )}
      </div>
    </div>
  );
};

export default DocWithChatbot;