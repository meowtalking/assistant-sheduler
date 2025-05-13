import React, { useState } from 'react';

const Login = ({ onLogin, switchToRegister }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleLogin = async () => {
    const response = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();

    if (response.ok) {
      localStorage.setItem('token', data.access_token);
      localStorage.setItem('user', JSON.stringify({
        user_id: data.user_id,
        is_admin: data.is_admin,
        name: data.name,
        role_id: data.role_id
      }));

      onLogin({
        user_id: data.user_id,
        is_admin: data.is_admin,
        name: data.name,
        role_id: data.role_id
      });
    } else {
      setMessage(data.detail || 'Ошибка входа');
    }
  };

  return (
    <div className="auth-form">
      <h2>Вход</h2>
      <input
        type="username"
        placeholder="Email"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />
      <input
        type="password"
        placeholder="Пароль"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />
      <button onClick={handleLogin}>Войти</button>
      {message && <p className="auth-message">{message}</p>}
      <p className="auth-toggle">
        Нет аккаунта? <button onClick={switchToRegister}>Зарегистрироваться</button>
      </p>
    </div>
  );
};

export default Login;