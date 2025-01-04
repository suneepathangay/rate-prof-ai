// src/components/UserInput.jsx
import React, { useState } from 'react';

function UserInput({ onSubmit }) {
  const [query, setQuery] = useState('');

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSubmit = () => {
    if (onSubmit) {
      onSubmit(query);
    }
    setQuery(''); // Optionally reset input after submitting
  };

  return (
    <div className="user-input-container">
      <input
        type="text"
        placeholder="Ask your question..."
        value={query}
        onChange={handleInputChange}
        className="user-input"
      />
      <button onClick={handleSubmit} className="submit-button">
        Submit
      </button>
    </div>
  );
}

export default UserInput;
