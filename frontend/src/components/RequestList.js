import React, { useState, useEffect } from 'react';

const RequestList = () => {
  const [requests, setRequests] = useState([]);

  useEffect(() => {
    fetch('/api/requests')
      .then((response) => response.json())
      .then((data) => setRequests(data));
  }, []);

  return (
    <div>
      <h2>Заявки на обслуживание</h2>
      <ul>
        {requests.map((request) => (
          <li key={request.id}>
            {request.passenger_type} - {request.departure_station} -> {request.arrival_station} (Статус: {request.status})
          </li>
        ))}
      </ul>
    </div>
  );
};

export default RequestList;
