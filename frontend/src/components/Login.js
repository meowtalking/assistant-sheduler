import React, { useState } from 'react';

const Login = ({ onLogin }) => {
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
      // ✅ Сохраняем сам токен
      localStorage.setItem('token', data.access_token);

      // ✅ Сохраняем инфо о пользователе (если нужно)
      localStorage.setItem('user', JSON.stringify({
        user_id: data.user_id,
        is_admin: data.is_admin,
        name: data.name,
        role_id: data.role_id
      }));

      setMessage(data.message || 'Успешный вход');
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
