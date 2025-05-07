import React, { useState, useEffect } from 'react';

const RequestForm = ({ userId }) => {
  const [form, setForm] = useState({
    passenger_type: '',
    departure_station_id: '',
    arrival_station_id: '',
    departure_time: '',
    luggage: false,
  });

  const [stations, setStations] = useState([]);
  const [disruptions, setDisruptions] = useState([]);
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        const [stationsRes, disruptionsRes] = await Promise.all([
          fetch('http://localhost:8000/stations'),
          fetch('http://localhost:8000/disruptions'),
        ]);

        const stationsData = await stationsRes.json();
        const disruptionsData = await disruptionsRes.json();

        setStations(stationsData);
        setDisruptions(disruptionsData);
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
        setMessage('Ошибка при загрузке станций или данных о сбоях');
      }
    };

    fetchInitialData();
  }, []);

  const activeDisruptionStationIds = disruptions.map(d => d.station_id);
  const availableStations = stations.filter(
    (station) => !activeDisruptionStationIds.includes(station.id)
  );

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const validateForm = () => {
    const { passenger_type, departure_station_id, arrival_station_id, departure_time } = form;

    if (!passenger_type || !departure_station_id || !arrival_station_id || !departure_time) {
      setMessage('Пожалуйста, заполните все обязательные поля!');
      return false;
    }

    if (departure_station_id === arrival_station_id) {
      setMessage('Станции отправления и назначения не должны совпадать');
      return false;
    }

    const departure = new Date(departure_time);
    if (departure <= new Date()) {
      setMessage('Время отправления должно быть в будущем');
      return false;
    }

    return true;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');

    if (!validateForm()) return;

    const formattedTime = form.departure_time.length === 16
      ? `${form.departure_time}:00`
      : form.departure_time;

    const payload = {
      user_id: userId,
      passenger_type: form.passenger_type,
      departure_station_id: parseInt(form.departure_station_id),
      arrival_station_id: parseInt(form.arrival_station_id),
      departure_time: formattedTime,
      luggage: form.passenger_type === 'blind' ? form.luggage : false,
    };

    try {
      setLoading(true);
      const res = await fetch('http://localhost:8000/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await res.json();

      if (res.ok) {
        setMessage('✅ Заявка успешно отправлена!');
        setForm({
          passenger_type: '',
          departure_station_id: '',
          arrival_station_id: '',
          departure_time: '',
          luggage: false,
        });
      } else {
        setMessage(`❌ ${data.detail || 'Ошибка при отправке заявки'}`);
      }
    } catch (error) {
      console.error('Ошибка при отправке:', error);
      setMessage('❌ Произошла ошибка при отправке заявки');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h3>Новая заявка</h3>

      {disruptions.length > 0 && (
      <div style={{ backgroundColor: '#ffe0e0', padding: '10px', borderRadius: '5px', marginBottom: '1em' }}>
        <strong>⚠️ Внимание! Сбои на станциях:</strong>
        <ul>
          {disruptions.map((d) => {
            const stationName = d.station?.name || 'Неизвестная станция';
            return (
              <li key={d.id}>
                {d.type} на <strong>{stationName}</strong><br />
                с {new Date(d.start_time).toLocaleString()} по {new Date(d.end_time).toLocaleString()}<br />
                {Boolean(d.description && d.description.trim()) && <em>{d.description}</em>}
              </li>
            );
          })}
        </ul>
      </div>
    )}


      <form onSubmit={handleSubmit}>
        <label>Тип пассажира:</label><br />
        <select name="passenger_type" onChange={handleChange} value={form.passenger_type}>
          <option value="">Выберите тип</option>
          <option value="blind">Слабовидящий</option>
          <option value="wheelchair">Коляска</option>
        </select><br />

        <label>Станция отправления:</label><br />
        <select name="departure_station_id" onChange={handleChange} value={form.departure_station_id}>
          <option value="">Выберите станцию</option>
          {availableStations.map((station) => (
            <option key={station.id} value={station.id}>{station.name}</option>
          ))}
        </select><br />

        <label>Станция назначения:</label><br />
        <select name="arrival_station_id" onChange={handleChange} value={form.arrival_station_id}>
          <option value="">Выберите станцию</option>
          {availableStations.map((station) => (
            <option key={station.id} value={station.id}>{station.name}</option>
          ))}
        </select><br />

        <label>Время отправления:</label><br />
        <input
          type="datetime-local"
          name="departure_time"
          onChange={handleChange}
          value={form.departure_time}
        /><br />

        {form.passenger_type === 'blind' && (
          <label>
            <input
              type="checkbox"
              name="luggage"
              checked={form.luggage}
              onChange={handleChange}
            />
            Багаж
          </label>
        )}<br />

        <button type="submit" disabled={loading}>
          {loading ? 'Отправка...' : 'Отправить заявку'}
        </button>
      </form>

      {message && <p style={{ marginTop: '1em' }}>{message}</p>}
    </div>
  );
};

export default RequestForm;
