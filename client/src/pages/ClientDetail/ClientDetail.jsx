import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { Wrapper, MainContainer } from './ClientDetail.styles';
import Header from '../../components/Header/Header';
import { FaArrowLeft } from 'react-icons/fa';

// Simulación de datos de clientes
const clients = [
  { id: '1', name: 'Juan Carlos Pérez', email: 'juan.perez@example.com', phone: '+54 91 1234-56789', type: 'No asociado', lastActivity: '19/1/2024' },
  { id: '2', name: 'María González', email: '', phone: '+54 91 1987-65432', type: 'Cliente', lastActivity: '18/1/2024' },
  { id: '3', name: 'Roberto Silva', email: 'roberto.silva@example.com', phone: '+54 91 5555-5555', type: 'Personalizado', lastActivity: '17/1/2024' },
];

export default function ClientDetail() {
  const { clientId } = useParams();
  const navigate = useNavigate();

  const clientData = clients.find(client => client.id === clientId);
  const [isEditing, setIsEditing] = useState(false);
  const [editedClient, setEditedClient] = useState(clientData);

  const handleEditChange = (field, value) => {
    setEditedClient({ ...editedClient, [field]: value });
  };

  const handleSave = () => {
    console.log('Cliente actualizado:', editedClient);
    setIsEditing(false);
  };

  if (!clientData) {
    return (
      <Wrapper>
        <MainContainer>
            <button onClick={() => navigate(-1)} style={{ marginBottom: '1rem', cursor: 'pointer', padding: '0.5rem 1rem', background: '#f44336', color: '#fff', border: 'none', borderRadius: '4px', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                <FaArrowLeft /> Volver
            </button>
          <h2>Cliente no encontrado</h2>
        </MainContainer>
      </Wrapper>
    );
  }

  return (
    <Wrapper>
      <Header />
      <MainContainer>
        <button onClick={() => navigate(-1)} style={{ marginBottom: '1rem', cursor: 'pointer', padding: '0.5rem 1rem', background: '#f44336', color: '#fff', border: 'none', borderRadius: '4px', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <FaArrowLeft /> Volver
        </button>
        <h2>Detalles del Cliente</h2>
        {isEditing ? (
          <form style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <input
              type="text"
              value={editedClient.name}
              onChange={e => handleEditChange('name', e.target.value)}
              placeholder="Nombre completo"
            />
            <input
              type="email"
              value={editedClient.email}
              onChange={e => handleEditChange('email', e.target.value)}
              placeholder="Email opcional"
            />
            <input
              type="text"
              value={editedClient.phone}
              onChange={e => handleEditChange('phone', e.target.value)}
              placeholder="Teléfono"
            />
            <select
              value={editedClient.type}
              onChange={e => handleEditChange('type', e.target.value)}
            >
              <option value="No asociado">No asociado</option>
              <option value="Cliente">Cliente</option>
              <option value="Personalizado">Personalizado</option>
            </select>
            <input
              type="text"
              value={editedClient.lastActivity}
              onChange={e => handleEditChange('lastActivity', e.target.value)}
              placeholder="Última actividad (fecha)"
            />
            <button type="button" onClick={handleSave} style={{ padding: '0.5rem 1rem', background: '#4caf50', color: '#fff', border: 'none', borderRadius: '4px' }}>
              Guardar
            </button>
          </form>
        ) : (
          <>
            <p><strong>Nombre completo:</strong> {clientData.name}</p>
            <p><strong>Email opcional:</strong> {clientData.email || 'No proporcionado'}</p>
            <p><strong>Teléfono:</strong> {clientData.phone}</p>
            <p><strong>Tipo Cliente:</strong> {clientData.type}</p>
            <p><strong>Última actividad:</strong> {clientData.lastActivity}</p>
            <button onClick={() => setIsEditing(true)} style={{ marginTop: '1rem', cursor: 'pointer', padding: '0.5rem 1rem', background: '#ff9800', color: '#fff', border: 'none', borderRadius: '4px' }}>
              Editar
            </button>
          </>
        )}
      </MainContainer>
    </Wrapper>
  );
}
