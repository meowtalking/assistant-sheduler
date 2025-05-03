import React, { useState } from 'react';
import Register from './components/Register';
import Login from './components/Login';
import RequestList from './components/RequestList';
import Schedule from './components/Schedule';
import RequestForm from './components/RequestForm';
import CreateEmployeeForm from './components/CreateEmployeeForm';
//import AdminRequestList from './components/AdminRequestList';

function App() {
  const [user, setUser] = useState(null);

  return (
    <div className="App">
      <h1>Assistant Scheduler</h1>

      {!user ? (
        <>
          <Register />
          <Login onLogin={setUser} />
        </>
      ) : (
        <>
          <p>
            Вы вошли как: {user.is_admin ? 'Администратор' : 'Пользователь'} (ID: {user.user_id})
          </p>

          {user.is_admin ? (
            <>
              <CreateEmployeeForm />
              {/*<AdminRequestList />*/}
            </>
          ) : (
            <RequestForm userId={user.user_id} />
          )}

          <RequestList />
          <Schedule />
        </>
      )}
    </div>
  );
}

export default App;
