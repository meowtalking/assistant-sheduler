import React, { useState, useEffect } from 'react';

const RequestList = () => {
  const [requests, setRequests] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchRequests = async () => {
      const token = localStorage.getItem('token');
      const userRaw = localStorage.getItem('user');

      if (!token || !userRaw) {
        setMessage('Пользователь не авторизован');
        return;
      }

      let user;
      try {
        user = JSON.parse(userRaw);
      } catch (e) {
        setMessage('Ошибка чтения данных пользователя');
        return;
      }

      try {
        const response = await fetch('http://localhost:8000/requests', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        const data = await response.json();

        if (!response.ok) {
          setMessage(data.detail || 'Ошибка загрузки заявок');
          return;
        }

        // Показывать только заявки пользователя, если не админ (role_id !== 1)
        if (user.role_id !== 1) {
          setRequests(data.filter((request) => request.user_id === user.id));
        } else {
          setRequests(data);
        }
      } catch (error) {
        setMessage('Ошибка соединения с сервером');
      }
    };

    fetchRequests();
  }, []);

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString('ru-RU', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div className="requests-container">
      <h2 className="requests-title">Заявки на обслуживание</h2>
      {message && <p className="error-message">{message}</p>}

      {requests.length === 0 ? (
        <p className="no-requests">Заявок нет</p>
      ) : (
        <div className="requests-grid">
          {requests.map((req) => (
            <div key={req.id} className="request-card">
              <h3 className="card-title">Заявка #{req.id}</h3>
              <div className="card-content">
                <div className="detail-row">
                  <span className="detail-label">Откуда:</span>
                  <span className="detail-value">{req.departure_station.name}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Куда:</span>
                  <span className="detail-value">{req.arrival_station.name}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Дата и время:</span>
                  <span className="detail-value">{formatDate(req.departure_time)}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Тип пассажира:</span>
                  <span className="detail-value">{req.passenger_type}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Багаж:</span>
                  <span className="detail-value">{req.luggage ? 'Да' : 'Нет'}</span>
                </div>
                <div className="detail-row">
                  <span className="detail-label">Статус:</span>
                  <span className={`status-badge status-${req.status.toLowerCase()}`}>
                    {req.status}
                  </span>
                </div>
                {req.assigned_employees?.length > 0 && (
                  <div className="assigned-employees">
                    <span className="detail-label">Сотрудники:</span>
                    <div className="employees-list">
                      {req.assigned_employees.map((e) => (
                        <span key={e.id} className="employee-tag">{e.name}</span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RequestList;
