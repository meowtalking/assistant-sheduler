import React, { useState, useEffect } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import RequestList from './components/RequestList';
import RequestForm from './components/RequestForm';
import CreateEmployeeForm from './components/CreateEmployeeForm';
import AssistantRequests from './components/AssistantRequests';
import AnalyticsDashboard from './components/AnalyticsDashboard';
import EmergencyPanel from './components/EmergencyPanel';
import EmergencyMessages from './components/EmergencyMessages';
import ReassignEmployees from './components/ReassignEmployees';
import Schedule from "./components/Schedule";

function App() {
  const [user, setUser] = useState(null);
  const [currentPage, setCurrentPage] = useState('login'); // 'login', 'register', или 'app'
  const [currentTab, setCurrentTab] = useState('dashboard');

  useEffect(() => {
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
      const userData = JSON.parse(savedUser);
      setUser(userData);
      setCurrentPage('app');
      setCurrentTab(
        userData.role_id === 1 ? 'dashboard' :
        userData.role_id === 3 ? 'tasks' : 'new-request'
      );
    }
  }, []);

  const handleLogin = (userData) => {
    setUser(userData);
    setCurrentPage('app');
  };

  const handleLogout = () => {
    localStorage.removeItem('user');
    localStorage.removeItem('token');
    setUser(null);
    setCurrentPage('login');
  };

  const renderContent = () => {
    if (!user) {
      switch (currentPage) {
        case 'login':
          return <Login onLogin={handleLogin} switchToRegister={() => setCurrentPage('register')} />;
        case 'register':
          return <Register switchToLogin={() => setCurrentPage('login')} />;
        default:
          return <Login onLogin={handleLogin} switchToRegister={() => setCurrentPage('register')} />;
      }
    }

    const isAdmin = user?.role_id === 1;
    const isAssistant = user?.role_id === 3;

    const tabs = isAdmin ? [
      { id: 'dashboard', label: 'Дашборд', component: <AnalyticsDashboard /> },
      { id: 'requests', label: 'Все заявки', component: <RequestList /> },
      { id: 'employees', label: 'Сотрудники', component: <CreateEmployeeForm /> },
      { id: 'emergency', label: 'Экстренные случаи', component: <EmergencyPanel /> },
      { id: 'messages', label: 'Сообщения', component: <EmergencyMessages /> },
      { id: 'reassign', label: 'Назначения', component: <ReassignEmployees /> },
      { id: 'schedule', label: 'Рапсиание', component: <Schedule/>}
    ] : isAssistant ? [
      { id: 'tasks', label: 'Мои задачи', component: <AssistantRequests /> },
      { id: 'emergency', label: 'Экстренные случаи', component: <EmergencyPanel /> },
      { id: 'messages', label: 'Сообщения', component: <EmergencyMessages /> }
    ] : [
      { id: 'new-request', label: 'Новая заявка', component: <RequestForm userId={user?.user_id} /> },
      { id: 'emergency', label: 'Экстренные случаи', component: <EmergencyPanel /> },
      { id: 'my-requests', label: 'Мои заявки', component: <RequestList />}
    ];

    return (
      <div className="user-container">
        <div className="user-header">
          <p>Вы вошли как: {isAdmin ? 'Администратор' : isAssistant ? 'Ассистент' : 'Пассажир'} ({user.name})</p>
          <button
            className="logout-btn"
            onClick={handleLogout}
          >
            Выйти
          </button>
        </div>

        <nav className="tabs">
          {tabs.map(tab => (
            <button
              key={tab.id}
              className={`tab ${currentTab === tab.id ? 'active' : ''}`}
              onClick={() => setCurrentTab(tab.id)}
            >
              {tab.label}
            </button>
          ))}
        </nav>

        <div className="tab-content">
          {tabs.find(tab => tab.id === currentTab)?.component}
        </div>
      </div>
    );
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Сервис сопровождения</h1>
      </header>

      <main className="app-main">
        {renderContent()}
      </main>
    </div>
  );
}

export default App;