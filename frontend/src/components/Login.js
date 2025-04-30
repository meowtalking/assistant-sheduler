import React, { useState } from 'react';

const Login = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (response.ok) {
      setMessage(data.message);
      onLogin(data); // передаём данные наверх
    } else {
      setMessage(data.detail);
    }
  };

  return (
    <div>
      <h2>Вход</h2>
      <input type="username" placeholder="Email" value={username}
             onChange={(e) => setUsername(e.target.value)} /><br />
      <input type="password" placeholder="Пароль" value={password}
             onChange={(e) => setPassword(e.target.value)} /><br />
      <button onClick={handleLogin}>Войти</button>
      <p>{message}</p>
    </div>
  );
};

export default Login;
