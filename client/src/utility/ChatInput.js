import React, { useState } from 'react';
import './ChatInput.css'; // Import the CSS file

function ChatInput() {
  // State to store the input value
  const [message, setMessage] = useState('');

  // Handler to update the state when typing
  const handleInputChange = (e) => {
    setMessage(e.target.value);
  };

  // Handler for the "Send" button (or Enter key)
  const handleSendMessage = async () => {
    // Check if the input is non-empty
    if (message.trim()) {
      try {
        const response = await fetch('http://localhost:5001/api/chat', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          // Send message as JSON in the body
          body: JSON.stringify({ message: message.trim() }), // Ensure it's trimmed
        });

        if (response.ok) {
          // Parse the response as JSON
          const data = await response.json();
          console.log('Server response:', data); // Log the server response
          
          // Clear the input field after successful message send
          setMessage('');
        } else {
          // Handle server error
          console.error('Error: Server returned a non-OK status');
        }
      } catch (error) {
        // Handle network or other errors
        console.error('Error sending message:', error);
      }
    }
  };
  
  return (
    <div className="chat-container">
      <div className="chat-input-wrapper">
        <input
          type="text"
          className="chat-input"
          value={message}
          onChange={handleInputChange}
          placeholder="Type your message..."
          onKeyPress={(e) => {
            if (e.key === 'Enter') handleSendMessage();
          }}
        />
        <button className="send-button" onClick={handleSendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatInput;
