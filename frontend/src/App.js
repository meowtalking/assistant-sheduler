import React, { useState, useEffect } from 'react';
import Register from './components/Register';
import Login from './components/Login';
import RequestList from './components/RequestList';
import Schedule from './components/Schedule';
import RequestForm from './components/RequestForm';
import CreateEmployeeForm from './components/CreateEmployeeForm';
//import AdminRequestList from './components/AdminRequestList';

function App() {
  const [user, setUser] = useState(null);
  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

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
            Вы вошли как: {user.is_admin ? 'Администратор' : 'Пользователь'} (name: {user.name})
          </p>
            <button onClick={() => {
              localStorage.removeItem('user');
              localStorage.removeItem('token');
              setUser(null);
            }}>
              Выйти
            </button>

          {user.is_admin ? (
            <>
              <CreateEmployeeForm />
              <Schedule />
              <RequestList />
              {/*<AdminRequestList />*/}
            </>
          ) : (
            <>
              <RequestForm userId={user.user_id} />
              <RequestList />
            </>

          )}



        </>
      )}
    </div>
  );
}

export default App;
