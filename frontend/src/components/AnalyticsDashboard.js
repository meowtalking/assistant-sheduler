import React, { useEffect, useState } from 'react';

const AnalyticsDashboard = () => {
  const [stats, setStats] = useState(null);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const response = await fetch('http://localhost:8000/analytics/stats');
        const data = await response.json();

        if (response.ok) {
          setStats(data);
        } else {
          setMessage(data.detail || 'Ошибка получения данных');
        }
      } catch (error) {
        console.error("Ошибка загрузки статистики:", error);
        setMessage("Ошибка загрузки статистики");
      }
    };

    fetchStats();
  }, []);

  if (!stats) return <div>{message || 'Загрузка статистики...'}</div>;

  return (
    <div>
      <h2>Аналитика заявок</h2>
      <ul>
        <li>Всего заявок: {stats.total_requests}</li>
        <li>Выполнено: {stats.completed_requests}</li>
        <li>В ожидании: {stats.pending_requests}</li>
      </ul>
    </div>
  );
};

export default AnalyticsDashboard;
