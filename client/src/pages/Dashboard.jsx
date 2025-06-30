import { useState, useEffect } from 'react';
import { LogOut, Users, Search, Filter, Shield, Phone, Calendar, AlertCircle } from 'lucide-react';

export default function Dashboard({ onLogout }) {
  const [clients, setClients] = useState([]);
  const [filteredClients, setFilteredClients] = useState([]);
  const [levelFilter, setLevelFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);

  // Mock data - replace with actual API call
  useEffect(() => {
    const mockClients = [
      {
        id: 1,
        full_name: 'Juan Carlos Pérez',
        phone: '5491123456789',
        level: 1,
        created_at: '2024-01-15',
        last_activity: '2024-01-20'
      },
      {
        id: 2,
        full_name: 'María González',
        phone: '5491198765432',
        level: 2,
        created_at: '2024-01-10',
        last_activity: '2024-01-19'
      },
      {
        id: 3,
        full_name: 'Roberto Silva',
        phone: '5491156789012',
        level: 3,
        created_at: '2024-01-05',
        last_activity: '2024-01-18'
      },
      {
        id: 4,
        full_name: 'Ana Martínez',
        phone: '5491134567890',
        level: 1,
        created_at: '2024-01-12',
        last_activity: '2024-01-17'
      },
      {
        id: 5,
        full_name: 'Carlos López',
        phone: '5491187654321',
        level: 2,
        created_at: '2024-01-08',
        last_activity: '2024-01-16'
      }
    ];

    setTimeout(() => {
      setClients(mockClients);
      setFilteredClients(mockClients);
      setLoading(false);
    }, 1000);
  }, []);

  useEffect(() => {
    let filtered = clients;

    // Filter by level
    if (levelFilter !== 'all') {
      filtered = filtered.filter(client => client.level === parseInt(levelFilter));
    }

    // Filter by search term
    if (searchTerm) {
      filtered = filtered.filter(client =>
        client.full_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        client.phone.includes(searchTerm)
      );
    }

    setFilteredClients(filtered);
  }, [clients, levelFilter, searchTerm]);

  const getLevelBadge = (level) => {
    const badges = {
      1: { text: 'Básico', class: 'level-basic' },
      2: { text: 'Premium', class: 'level-premium' },
      3: { text: 'VIP', class: 'level-vip' }
    };
    return badges[level] || { text: 'Desconocido', class: 'level-unknown' };
  };

  const formatPhone = (phone) => {
    return phone.replace(/(\d{2})(\d{2})(\d{4})(\d{4})/, '+$1 $2 $3-$4');
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('es-AR');
  };

  return (
    <div className="dashboard-container">
      <header className="dashboard-header">
        <div className="header-content">
          <div className="header-left">
            <div className="logo-container">
              <Shield className="logo-icon" />
              <div className="logo-text">
                <h1>TABORRA</h1>
                <span>ALARMAS SRL</span>
              </div>
            </div>
          </div>
          <div className="header-right">
            <span className="admin-text">Panel de Administración</span>
            <button onClick={onLogout} className="logout-button">
              <LogOut size={20} />
              Cerrar Sesión
            </button>
          </div>
        </div>
      </header>

      <main className="dashboard-main">
        <div className="dashboard-content">
          <div className="page-header">
            <div className="page-title">
              <Users className="page-icon" />
              <h2>Gestión de Clientes</h2>
            </div>
            <div className="stats-summary">
              <div className="stat-card">
                <span className="stat-number">{clients.length}</span>
                <span className="stat-label">Total Clientes</span>
              </div>
              <div className="stat-card">
                <span className="stat-number">{clients.filter(c => c.level === 3).length}</span>
                <span className="stat-label">VIP</span>
              </div>
              <div className="stat-card">
                <span className="stat-number">{clients.filter(c => c.level === 2).length}</span>
                <span className="stat-label">Premium</span>
              </div>
            </div>
          </div>

          <div className="filters-section">
            <div className="search-container">
              <Search className="search-icon" />
              <input
                type="text"
                placeholder="Buscar por nombre o teléfono..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="search-input"
              />
            </div>
            <div className="filter-container">
              <Filter className="filter-icon" />
              <select
                value={levelFilter}
                onChange={(e) => setLevelFilter(e.target.value)}
                className="level-filter"
              >
                <option value="all">Todos los niveles</option>
                <option value="1">Básico</option>
                <option value="2">Premium</option>
                <option value="3">VIP</option>
              </select>
            </div>
          </div>

          {loading ? (
            <div className="loading-container">
              <div className="loading-spinner"></div>
              <p>Cargando clientes...</p>
            </div>
          ) : (
            <div className="clients-table-container">
              <table className="clients-table">
                <thead>
                  <tr>
                    <th>Cliente</th>
                    <th>Teléfono</th>
                    <th>Nivel</th>
                    <th>Fecha de Registro</th>
                    <th>Última Actividad</th>
                    <th>Estado</th>
                  </tr>
                </thead>
                <tbody>
                  {filteredClients.map((client) => {
                    const badge = getLevelBadge(client.level);
                    return (
                      <tr key={client.id} className="client-row">
                        <td className="client-name">
                          <div className="client-avatar">
                            {client.full_name.split(' ').map(n => n[0]).join('').toUpperCase()}
                          </div>
                          <span>{client.full_name}</span>
                        </td>
                        <td className="client-phone">
                          <Phone size={16} />
                          {formatPhone(client.phone)}
                        </td>
                        <td>
                          <span className={`level-badge ${badge.class}`}>
                            {badge.text}
                          </span>
                        </td>
                        <td className="client-date">
                          <Calendar size={16} />
                          {formatDate(client.created_at)}
                        </td>
                        <td className="client-activity">
                          {formatDate(client.last_activity)}
                        </td>
                        <td>
                          <span className="status-badge status-active">
                            Activo
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>

              {filteredClients.length === 0 && (
                <div className="empty-state">
                  <AlertCircle size={48} />
                  <h3>No se encontraron clientes</h3>
                  <p>Intenta ajustar los filtros de búsqueda</p>
                </div>
              )}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}