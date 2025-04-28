import React from 'react';
import RequestList from './components/RequestList';
import Schedule from './components/Schedule';

function App() {
  return (
    <div className="App">
      <h1>Assistant Scheduler</h1>
      <RequestList />
      <Schedule />
    </div>
  );
}

export default App;
