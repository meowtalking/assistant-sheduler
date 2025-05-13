import React, { useEffect, useState } from 'react';
//import './styles/requests.css'; // Убедитесь, что путь правильный

const AssistantRequests = () => {
  const [requests, setRequests] = useState([]);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchRequests = async () => {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://localhost:8000/assistant/requests', {
          headers: {
            'Authorization': `Bearer ${token}`,
          }
        });

        if (!response.ok) {
          const data = await response.json();
          setMessage(data.detail || 'Ошибка загрузки заявок');
          return;
        }

        const data = await response.json();
        setRequests(data);
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
      minute: '2-digit'
    });
  };
// Внутри AssistantRequests компонента, добавим:
const handleStatusChange = async (id, newStatus) => {
  const token = localStorage.getItem('token');
  try {
    const response = await fetch(`http://localhost:8000/assistant/requests/${id}/status`, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({ status: newStatus })
    });

    if (response.ok) {
      setRequests(prev =>
        prev.map(r => (r.id === id ? { ...r, status: newStatus } : r))
      );
    } else {
      const data = await response.json();
      alert(data.detail || 'Ошибка обновления статуса');
    }
  } catch (error) {
    alert('Ошибка соединения с сервером');
  }
};

  return (
    <div className="requests-container">
      <h2 className="requests-title">Мои заявки</h2>
      {message && <p className="error-message">{message}</p>}

      {requests.length === 0 ? (
        <p className="no-requests">Нет назначенных заявок</p>
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

                {req.assigned_employees.length > 0 && (
                  <div className="assigned-employees">
                    <span className="detail-label">Назначенные сотрудники:</span>
                    <div className="employees-list">
                      {req.assigned_employees.map(e => (
                        <span key={e.id} className="employee-tag">{e.name}</span>
                      ))}
                    </div>
                  </div>

                )}

              </div>
              <div className="detail-row">
                <label>Изменить статус:</label>
                <select
                  value={req.status}
                  onChange={e => handleStatusChange(req.id, e.target.value)}
                >
                  <option value="Ожидает">Ожидает</option>
                  <option value="В процессе">В процессе</option>
                  <option value="Завершена">Завершена</option>
                </select>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};











export default AssistantRequests;