import React, { useState } from 'react';

const RequestForm = ({ userId }) => {
  const [form, setForm] = useState({
    passenger_type: '',
    departure_station: '',
    arrival_station: '',
    departure_time: '', // формат: YYYY-MM-DDTHH:MM
    luggage: false,
  });

  const [message, setMessage] = useState('');

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm({
      ...form,
      [name]: type === 'checkbox' ? checked : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Проверка обязательных полей
    if (!form.passenger_type || !form.departure_station || !form.arrival_station || !form.departure_time) {
      setMessage('Пожалуйста, заполните все обязательные поля!');
      return;
    }

    // Добавляем секунды, если отсутствуют
    const formattedTime = form.departure_time.length === 16
      ? `${form.departure_time}:00`
      : form.departure_time;

    try {
      const response = await fetch('http://localhost:8000/api/request', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          passenger_type: form.passenger_type,
          departure_station: form.departure_station,
          arrival_station: form.arrival_station,
          departure_time: formattedTime,
          luggage: form.luggage, // bool — true/false
        }),
      });

      const data = await response.json();
      if (response.ok) {
        setMessage('Заявка успешно отправлена!');
        setForm({
          passenger_type: '',
          departure_station: '',
          arrival_station: '',
          departure_time: '',
          luggage: false,
        });
      } else {
        setMessage(data.detail || 'Ошибка при отправке');
      }
    } catch (error) {
      setMessage('Произошла ошибка при отправке заявки');
      console.error(error);
    }
  };

  return (
    <div>
      <h3>Новая заявка</h3>
      <form onSubmit={handleSubmit}>
        <select name="passenger_type" onChange={handleChange} value={form.passenger_type}>
          <option value="">Выберите тип пассажира</option>
          <option value="blind">Слабовидящий</option>
          <option value="blind_with_baggage">Слабовидящий с багажом</option>
          <option value="wheelchair">Коляска</option>
        </select><br />

        <input
          name="departure_station"
          placeholder="Станция отправления"
          onChange={handleChange}
          value={form.departure_station}
        /><br />

        <input
          name="arrival_station"
          placeholder="Станция назначения"
          onChange={handleChange}
          value={form.arrival_station}
        /><br />

        <input
          type="datetime-local"
          name="departure_time"
          onChange={handleChange}
          value={form.departure_time}
        /><br />

        <label>
          Багаж:
          <input
            type="checkbox"
            name="luggage"
            checked={form.luggage}
            onChange={handleChange}
          />
        </label><br />

        <button type="submit">Отправить заявку</button>
      </form>
      <p>{message}</p>
    </div>
  );
};

export default RequestForm;
