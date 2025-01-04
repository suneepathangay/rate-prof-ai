// src/App.jsx
// import React from 'react';
// import UserInput from './components/UserInput';
// import './App.css'; 

// function App() {
//   const handleSubmitQuery = (query) => {
//     console.log('User query:', query);
//     // connect to api later
//   };

//   return (
//     <div className="app-container">
//       <h1>Ask a Question!</h1>
//       <UserInput onSubmit={handleSubmitQuery} />
//     </div>
//   );
// }

// export default App;
import React from 'react';
import './App.css';
import ChatBox from './components/ChatBox';

function App() {
  return (
    <div className="app-container">
      <h1>Chat Application</h1>
      <ChatBox />
    </div>
  );
}

export default App;
