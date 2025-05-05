import React, { useState, useEffect } from 'react';

const Schedule = () => {
  const [schedule, setSchedule] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('http://localhost:8000/api/schedule')
      .then((response) => {
        if (!response.ok) throw new Error('Ошибка при загрузке расписания');
        return response.json();
      })
      .then((data) => setSchedule(data))
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Загрузка расписания...</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Свободные сотрудники</h2>
      {schedule.length === 0 ? (
        <p>Нет свободных сотрудников</p>
      ) : (
        <ul>
          {schedule.map((employee) => (
            <li key={employee.id}>
              {employee.name}: {employee.shift_time}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Schedule;
