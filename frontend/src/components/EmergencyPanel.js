import React, { useState } from 'react';

const EmergencyPanel = () => {
  const [requestId, setRequestId] = useState('');
  const [message, setMessage] = useState('');
  const [status, setStatus] = useState('');

  const sendHelpRequest = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await fetch('http://localhost:8000/emergency/report', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          request_id: Number(requestId),
          message
        })
      });

      if (response.ok) {
        setStatus('Сообщение об экстренной ситуации отправлено.');
      } else {
        const data = await response.json();
        setStatus(data.detail || 'Ошибка отправки.');
      }
    } catch (error) {
      console.error("Ошибка при отправке запроса:", error);
      setStatus("Ошибка соединения.");
    }
  };

  return (
    <div>
      <h2>Экстренная помощь</h2>
      <input
        type="number"
        placeholder="ID заявки"
        value={requestId}
        onChange={e => setRequestId(e.target.value)}
      />
      <br />
      <textarea
        placeholder="Сообщение"
        value={message}
        onChange={e => setMessage(e.target.value)}
      />
      <br />
      <button onClick={sendHelpRequest}>Отправить сигнал</button>
      <p>{status}</p>
    </div>
  );
};

export default EmergencyPanel;
