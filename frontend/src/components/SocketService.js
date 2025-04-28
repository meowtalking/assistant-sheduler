import { useEffect } from 'react';

const SocketService = () => {
  useEffect(() => {
    const socket = new WebSocket('ws://localhost:8000/ws');

    socket.onopen = () => {
      console.log('Connected to WebSocket');
    };

    socket.onmessage = (message) => {
      console.log('Received message:', message.data);
      // Обработка обновлений данных в интерфейсе
    };

    return () => socket.close();
  }, []);

  return null;
};

export default SocketService;
