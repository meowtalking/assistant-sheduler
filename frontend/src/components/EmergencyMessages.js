import React, { useEffect, useState } from 'react';

const EmergencyMessages = () => {
  const [messages, setMessages] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchMessages = async () => {
      const token = localStorage.getItem('token');
      try {
        const response = await fetch('http://localhost:8000/emergency/requests', {
          headers: {
            'Authorization': `Bearer ${token}`
          }
        });


        if (!response.ok) {
          const data = await response.json();
          setError(data.detail || 'Ошибка загрузки сообщений');
          return;
        }

        const data = await response.json();
        setMessages(data);
      } catch (error) {
        setError('Ошибка соединения с сервером');
      }
    };

    fetchMessages();
  }, []);

  return (
    <div>
      <h2>Экстренные сообщения</h2>
      {error && <p>{error}</p>}
      <ul>
        {messages.map(msg => (
          <li key={msg.id}>
            <strong>Заявка #{msg.request_id}</strong>: {msg.message}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default EmergencyMessages;
