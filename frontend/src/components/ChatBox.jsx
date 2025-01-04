import React, { useState } from 'react';
import ChatMessage from './ChatMessage';

function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState('');

  const handleSendMessage = () => {
    if (newMessage.trim()) {
      setMessages((prev) => [...prev, { text: newMessage, sender: 'user' }]);
      setNewMessage('');
      // Simulate a response (you can replace this with an API call)
      setTimeout(() => {
        setMessages((prev) => [...prev, { text: 'This is an AI response.', sender: 'ai' }]);
      }, 500);
    }
  };

  return (
    <div className="chat-box">
      <div className="chat-messages">
        {messages.map((message, index) => (
          <ChatMessage key={index} text={message.text} sender={message.sender} />
        ))}
      </div>
      <div className="chat-input-container">
        <input
          type="text"
          className="chat-input"
          placeholder="Type your message..."
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
        />
        <button className="chat-send-button" onClick={handleSendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatBox;
