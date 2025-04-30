import React, { useState } from 'react';

const Register = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isDisabled, setIsDisabled] = useState(false);
  const [message, setMessage] = useState('');

  const handleRegister = async () => {
    const response = await fetch('http://localhost:8000/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, is_disabled: isDisabled }),
    });

    const data = await response.json();
    setMessage(data.message || data.detail);
  };

  return (
    <div>
      <h2>Регистрация</h2>
      <input type="email" placeholder="Email" value={email}
             onChange={(e) => setEmail(e.target.value)} /><br />
      <input type="password" placeholder="Пароль" value={password}
             onChange={(e) => setPassword(e.target.value)} /><br />
      <label>
        <input type="checkbox" checked={isDisabled}
               onChange={() => setIsDisabled(!isDisabled)} />
        Я нуждаюсь в сопровождении (инвалид)
      </label><br />
      <button onClick={handleRegister}>Зарегистрироваться</button>
      <p>{message}</p>
    </div>
  );
};

export default Register;
