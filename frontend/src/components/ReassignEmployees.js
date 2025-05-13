import React, { useEffect, useState } from 'react';

const ReassignEmployees = () => {
  const [requests, setRequests] = useState([]);
  const [employees, setEmployees] = useState([]);
  const [selectedEmployees, setSelectedEmployees] = useState({});
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      const token = localStorage.getItem('token');
      try {
        const [requestsRes, employeesRes] = await Promise.all([
          fetch('http://localhost:8000/admin/requests', { headers: { Authorization: `Bearer ${token}` } }),
          fetch('http://localhost:8000/admin/employees', { headers: { Authorization: `Bearer ${token}` } }),
        ]);

        const requestsData = await requestsRes.json();
        const employeesData = await employeesRes.json();
        setRequests(requestsData);
        setEmployees(employeesData);
      } catch (err) {
        setError('Ошибка загрузки данных');
      }
    };

    fetchData();
  }, []);

  const handleCheckboxChange = (requestId, employeeId) => {
    setSelectedEmployees(prev => {
      const current = prev[requestId] || [];
      const alreadySelected = current.includes(employeeId);
      return {
        ...prev,
        [requestId]: alreadySelected
          ? current.filter(id => id !== employeeId)
          : [...current, employeeId],
      };
    });
  };

  const handleSave = async (requestId) => {
    const token = localStorage.getItem('token');
    try {
      const response = await fetch(`http://localhost:8000/admin/reassign`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({
          request_id: requestId,
          employee_ids: selectedEmployees[requestId] || [],
        }),
      });

      if (!response.ok) {
        const data = await response.json();
        alert(data.detail || 'Ошибка при сохранении');
      } else {
        alert('Сотрудники переназначены');
      }
    } catch {
      alert('Ошибка соединения');
    }
  };

  return (
    <div>
      <h2>Переназначить сотрудников</h2>
      {error && <p>{error}</p>}
      {requests.map(req => (
        <div key={req.id} style={{ border: '1px solid #ccc', padding: '10px', marginBottom: '10px' }}>
          <p><strong>Заявка #{req.id}</strong></p>
          {employees.map(emp => (
            <label key={emp.id} style={{ display: 'block' }}>
              <input
                type="checkbox"
                checked={(selectedEmployees[req.id] || []).includes(emp.id)}
                onChange={() => handleCheckboxChange(req.id, emp.id)}
              />
              {emp.name}
            </label>
          ))}
          <button onClick={() => handleSave(req.id)} style={{ marginTop: '8px' }}>
            Сохранить
          </button>
        </div>
      ))}
    </div>
  );
};

export default ReassignEmployees;
