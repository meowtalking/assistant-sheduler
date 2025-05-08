import React, { useState, useEffect } from 'react';

const RequestList = ({ userId, role }) => {
  const [requests, setRequests] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/requests')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log('Полученные заявки:', data);
        if (role !== 'admin') {
          // Для обычных пользователей показываем только их заявки
          setRequests(data.filter(request => request.user_id === userId));
        } else {
          // Администратору показываем все заявки
          setRequests(data);
        }
      })
      .catch((err) => {
        console.error('Ошибка при получении заявок:', err);
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, [userId, role]);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: 'red' }}>Ошибка: {error}</p>;

  return (
    <div>
      <h2>Заявки на обслуживание</h2>
      {requests.length === 0 ? (
        <p>Заявок нет</p>
      ) : (
        <ul>
          {requests.map((request) => {

            return (
              <li key={request.id}>
                {request.passenger_type} <br />
                {request.departure_station.name} → {request.arrival_station.name} <br />
                Время: {new Date(request.departure_time).toLocaleString()} <br />
                Статус: {request.status} <br />
                Багаж: {request.luggage ? 'Да' : 'Нет'} <br />
                Назначенные сотрудники: {
                  (request.assigned_employees || []).map(e => e.name).join(', ') || 'Нет'
                }
              </li>
            );
          })}
        </ul>
      )}
    </div>
  );
};

export default RequestList;
