// src/components/SubmitButton.jsx
import React from 'react';

function SubmitButton({ onClick }) {
  return (
    <button onClick={onClick} className="submit-button">
      Submit
    </button>
  );
}

export default SubmitButton;
