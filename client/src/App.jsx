import { Routes, Route, Navigate } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Login from './pages/Login/Login';
import Dashboard from './pages/Dashboard/Dashboard';

export default function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('adminToken');
    if (token) setIsAuthenticated(true);
    setLoading(false);
  }, []);

  const handleLogin = (token) => {
    localStorage.setItem('adminToken', token);
    setIsAuthenticated(true);
  };

  const handleLogout = () => {
    localStorage.removeItem('adminToken');
    setIsAuthenticated(false);
  };

  if (loading) {
    return <div>Cargando...</div>;
  }

  return (
    <Routes>
      <Route
        path="/login"
        element={
          isAuthenticated ? <Navigate to="/dashboard" replace /> : <Login onLogin={handleLogin} />
        }
      />
      <Route
        path="/dashboard"
        element={
          isAuthenticated ? <Dashboard onLogout={handleLogout} /> : <Navigate to="/login" replace />
        }
      />
      <Route path="/" element={<Navigate to="/login" replace />} />
    </Routes>
  );
}