import React, { useState, useEffect } from 'react';

const RequestList = () => {
  const [requests, setRequests] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://localhost:8000/api/requests')
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        console.log('Полученные заявки:', data);
        setRequests(data);
      })
      .catch((err) => {
        console.error('Ошибка при получении заявок:', err);
        setError(err.message);
      })
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <p>Загрузка...</p>;
  if (error) return <p style={{ color: 'red' }}>Ошибка: {error}</p>;

  return (
    <div>
      <h2>Заявки на обслуживание</h2>
      {requests.length === 0 ? (
        <p>Заявок нет</p>
      ) : (
        <ul>
          {requests.map((request) => (
            <li key={request.id}>
              {request.passenger_type} — {request.departure_station} → {request.arrival_station} <br />
              Время: {new Date(request.departure_time).toLocaleString()} <br />
              Статус: {request.status} <br />
              Багаж: {request.luggage ? 'Да' : 'Нет'} <br />
              Назначенные сотрудники: {
                  Array.isArray(request.assigned_employee_ids)
                    ? request.assigned_employee_ids.length > 0
                      ? request.assigned_employee_ids.join(', ')
                      : 'Нет'
                    : 'Нет'
                }
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default RequestList;
