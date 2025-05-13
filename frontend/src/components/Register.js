import React, { useState } from 'react';

const Register = ({ switchToLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [isDisabled, setIsDisabled] = useState(false);
  const [message, setMessage] = useState('');

  const handleRegister = async () => {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    });

    const data = await response.json();
    setMessage(data.message || data.detail);

    if (response.ok) {
      switchToLogin();
    }
  };

  return (
    <div className="auth-form">
      <h2>Регистрация</h2>
      <input
        type="email"
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
      <label>
        <input
          type="checkbox"
          checked={isDisabled}
          onChange={() => setIsDisabled(!isDisabled)}
        />
        Я подтверждаю, что являюсь инвалидом и нуждаюсь в сопровождении
      </label>
      <button onClick={handleRegister} disabled={!isDisabled}>
        Зарегистрироваться
      </button>
      {message && <p className="auth-message">{message}</p>}
      <p className="auth-toggle">
        Уже есть аккаунт? <button onClick={switchToLogin}>Войти</button>
      </p>
    </div>
  );
};

export default Register;