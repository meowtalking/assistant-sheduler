import React, { useState, useEffect } from 'react';
import Register from './components/Register';
import Login from './components/Login';
import RequestList from './components/RequestList';
import Schedule from './components/Schedule';
import RequestForm from './components/RequestForm';
import CreateEmployeeForm from './components/CreateEmployeeForm';
import AssistantRequests from "./components/AssistantRequests";

function App() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      setUser(JSON.parse(savedUser));
    }
  }, []);

  const isAdmin = user?.role_id === 1;  // Админ
  const isAssistant = user?.role_id === 3;  // Ассистент

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
            Вы вошли как:{" "}
            {isAdmin
              ? "Администратор"
              : isAssistant
              ? "Ассистент"
              : "Пользователь"}{" "}
            (name: {user.name})
          </p>
          <button
            onClick={() => {
              localStorage.removeItem("user");
              localStorage.removeItem("token");
              setUser(null);
            }}
          >
            Выйти
          </button>

          {isAdmin ? (
            <>
              <CreateEmployeeForm />
              <Schedule />
              <RequestList />
              <AssistantRequests />
            </>
          ) : isAssistant ? (
            <>
              <AssistantRequests />
              <Schedule />
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
