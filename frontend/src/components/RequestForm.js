import React, { useState } from 'react';

const RequestForm = ({ userId }) => {
  const [departureStation, setDepartureStation] = useState('');
  const [arrivalStation, setArrivalStation] = useState('');
  const [departureTime, setDepartureTime] = useState('');
  const [passengerType, setPassengerType] = useState('инвалид');
  const [luggage, setLuggage] = useState(false);
  const [message, setMessage] = useState('');

  const handleSubmit = async () => {
    const response = await fetch('http://localhost:8000/requests', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_id: userId,
        departure_station: departureStation,
        arrival_station: arrivalStation,
        departure_time: departureTime,
        passenger_type: passengerType,
        luggage,
      }),
    });

    const data = await response.json();
    setMessage(data.message || data.detail);
  };

  return (
    <div>
      <h2>Подать заявку на сопровождение</h2>
      <input
        type="text"
        placeholder="Станция отправления"
        value={departureStation}
        onChange={(e) => setDepartureStation(e.target.value)}
      /><br />
      <input
        type="text"
        placeholder="Станция прибытия"
        value={arrivalStation}
        onChange={(e) => setArrivalStation(e.target.value)}
      /><br />
      <input
        type="datetime-local"
        value={departureTime}
        onChange={(e) => setDepartureTime(e.target.value)}
      /><br />
      <select value={passengerType} onChange={(e) => setPassengerType(e.target.value)}>
        <option value="инвалид">Инвалид</option>
        <option value="пожилой">Пожилой</option>
        <option value="беременная">Беременная</option>
        <option value="другое">Другое</option>
      </select><br />
      <label>
        <input
          type="checkbox"
          checked={luggage}
          onChange={() => setLuggage(!luggage)}
        />
        Наличие багажа
      </label><br />
      <button onClick={handleSubmit}>Отправить заявку</button>
      <p>{message}</p>
    </div>
  );
};

export default RequestForm;
