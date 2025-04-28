import React, { useState, useEffect } from 'react';

const Schedule = () => {
  const [schedule, setSchedule] = useState([]);

  useEffect(() => {
    fetch('/api/schedule')
      .then((response) => response.json())
      .then((data) => setSchedule(data));
  }, []);

  return (
    <div>
      <h2>Расписание сотрудников</h2>
      <ul>
        {schedule.map((employee) => (
          <li key={employee.id}>
            {employee.name}: {employee.shift_time}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Schedule;
