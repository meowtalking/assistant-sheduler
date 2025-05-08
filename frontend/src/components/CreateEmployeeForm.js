import React, { useState } from 'react';

const CreateEmployeeForm = () => {
  const [name, setName] = useState('');
  const [contactInfo, setContactInfo] = useState('');
  const [shiftStart, setShiftStart] = useState('');
  const [shiftEnd, setShiftEnd] = useState('');
  const [skills, setSkills] = useState('');
  const [availableDays, setAvailableDays] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!name || !contactInfo || !shiftStart || !shiftEnd || !skills || availableDays.length === 0) {
      setMessage('Пожалуйста, заполните все поля.');
      return;
    }

    setLoading(true);
    const token = localStorage.getItem('token');
    const response = await fetch('http://localhost:8000/admin/employees', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        name,
        contact_info: contactInfo,
        shift_start: shiftStart,
        shift_end: shiftEnd,
        skills: skills.split(','),
        available_days: availableDays,
      }),
    });

    const data = await response.json();
    setLoading(false);

    if (!response.ok) {
      setMessage(data.detail || 'Ошибка при создании сотрудника');
      return;
    }

    setMessage(data.message || data.detail || 'Сотрудник добавлен');

    // Очистка полей формы
    setName('');
    setContactInfo('');
    setShiftStart('');
    setShiftEnd('');
    setSkills('');
    setAvailableDays([]);
  };

  const handleDayChange = (e) => {
    const { value, checked } = e.target;
    setAvailableDays((prevDays) =>
      checked ? [...prevDays, value] : prevDays.filter(day => day !== value)
    );
  };

  return (
    <div className="create-employee-form">
      <h2>Создание аккаунта сотрудника</h2>
      <input
        type="text"
        placeholder="Имя"
        value={name}
        onChange={(e) => setName(e.target.value)}
        className="input-field"
      />
      <br />
      <input
        type="text"
        placeholder="Контакты"
        value={contactInfo}
        onChange={(e) => setContactInfo(e.target.value)}
        className="input-field"
      />
      <br />
      <input
        type="time"
        placeholder="Начало смены"
        value={shiftStart}
        onChange={(e) => setShiftStart(e.target.value)}
        className="input-field"
      />
      <br />
      <input
        type="time"
        placeholder="Конец смены"
        value={shiftEnd}
        onChange={(e) => setShiftEnd(e.target.value)}
        className="input-field"
      />
      <br />
      <input
        type="text"
        placeholder="Навыки (через запятую)"
        value={skills}
        onChange={(e) => setSkills(e.target.value)}
        className="input-field"
      />
      <br />
      <div className="available-days">
        <label>Доступные дни:</label>
        {['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'].map((day) => (
          <label key={day}>
            <input
              type="checkbox"
              value={day}
              checked={availableDays.includes(day)}
              onChange={handleDayChange}
            />
            {day}
          </label>
        ))}
      </div>
      <br />
      <button onClick={handleSubmit} disabled={loading} className="submit-button">
        {loading ? 'Создание...' : 'Создать'}
      </button>
      {message && <p className={`message ${!loading && (message.includes('Ошибка') ? 'error' : 'success')}`}>{message}</p>}
    </div>
  );
};

export default CreateEmployeeForm;
