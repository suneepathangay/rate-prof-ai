import React from 'react';

function ChatMessage({ text, sender }) {
  return (
    <div className={`chat-message ${sender}`}>
      <div className="message-bubble">{text}</div>
    </div>
  );
}

export default ChatMessage;
