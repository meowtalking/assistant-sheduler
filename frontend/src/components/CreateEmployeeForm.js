import React, { useState } from 'react';

const CreateEmployeeForm = () => {
  const [name, setName] = useState('');
  const [contactInfo, setContactInfo] = useState('');
  const [shiftTime, setShiftTime] = useState('');
  const [skills, setSkills] = useState('');
  const [message, setMessage] = useState('');

  const handleSubmit = async () => {
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/admin/employees', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        name,
        contact_info: contactInfo,
        shift_time: shiftTime,
        skills,
      }),
    });

    const data = await response.json();
    if (!response.ok) {
      setMessage(data.detail || 'Ошибка при создании сотрудника');
      return;
    }

    setMessage(data.message || data.detail || 'Сотрудник добавлен');

    // Очистка полей формы
    setName('');
    setContactInfo('');
    setShiftTime('');
    setSkills('');
  };

  return (
    <div>
      <h2>Создание аккаунта сотрудника</h2>
      <input type="text" placeholder="Имя" value={name} onChange={(e) => setName(e.target.value)} /><br />
      <input type="text" placeholder="Контакты" value={contactInfo} onChange={(e) => setContactInfo(e.target.value)} /><br />
      <input type="text" placeholder="Смена (например, 09:00-18:00)" value={shiftTime} onChange={(e) => setShiftTime(e.target.value)} /><br />
      <input type="text" placeholder="Навыки (через запятую)" value={skills} onChange={(e) => setSkills(e.target.value)} /><br />
      <button onClick={handleSubmit}>Создать</button>
      <p>{message}</p>
    </div>
  );
};

export default CreateEmployeeForm;
