import { useState } from 'react';
import {
  Wrapper,
  Main,
  Stats,
  StatCard,
  SearchBar,
  Input,
  Select,
  LoadBtn,
  Table,
  StyledTable,
  StyledTh,
  WeeklyActivityCard,
  MonthlyActivityCard
} from './Dashboard.styles';
import Header from '../../components/Header/Header';
import ClientRow from '../../components/ClientRow/ClientRow.jsx';

const levelMapping = {
  1: 'No asociado',
  2: 'Cliente',
  3: 'Personalizado',
};

const clients = [
  { id: 1, name: 'Juan Carlos Pérez', phone: '+54 91 1234-56789', level: 1, last: '19/1/2024' },
  { id: 2, name: 'María González', phone: '+54 91 1987-65432', level: 2, last: '18/1/2024' },
  { id: 3, name: 'Roberto Silva', phone: '+54 91 5555-5555', level: 3, last: '17/1/2024' },
  { id: 4, name: 'Ana López', phone: '+54 91 4444-4444', level: 1, last: '16/1/2024' },
  { id: 5, name: 'Carlos García', phone: '+54 91 3333-3333', level: 2, last: '15/1/2024' },
  { id: 6, name: 'Laura Martínez', phone: '+54 91 2222-2222', level: 3, last: '14/1/2024' },
  { id: 7, name: 'Pedro Sánchez', phone: '+54 91 1111-1111', level: 1, last: '13/1/2024' },
  { id: 8, name: 'Sofía Fernández', phone: '+54 91 6666-6666', level: 2, last: '12/1/2024' },
  { id: 9, name: 'Miguel Torres', phone: '+54 91 7777-7777', level: 3, last: '11/1/2024' },
  { id: 10, name: 'Isabel Gómez', phone: '+54 91 8888-8888', level: 1, last: '10/1/2024' },
  { id: 11, name: 'Luis Ramírez', phone: '+54 91 9999-9999', level: 2, last: '9/1/2024' },
  { id: 12, name: 'Carmen Ruiz', phone: '+54 91 0000-0000', level: 3, last: '8/1/2024' },
  { id: 13, name: 'Jorge Castro', phone: '+54 91 1234-0000', level: 1, last: '7/1/2024' },
  { id: 14, name: 'Elena Vega', phone: '+54 91 5678-0000', level: 2, last: '6/1/2024' },
  { id: 15, name: 'Raúl Moreno', phone: '+54 91 9101-0000', level: 3, last: '5/1/2024' },
];

export default function Dashboard({ onLogout }) {
  const [levelFilter, setLevelFilter] = useState('all');
  const [search, setSearch] = useState('');
  const [currentPage, setCurrentPage] = useState(1);
  const clientsPerPage = 8;

  const filtered = clients.filter(c => {
    const matchLevel = levelFilter === 'all' || c.level === parseInt(levelFilter);
    const matchSearch =
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.phone.includes(search);
    return matchLevel && matchSearch;
  });

  const totalPages = Math.ceil(filtered.length / clientsPerPage);
  const paginatedClients = filtered.slice(
    (currentPage - 1) * clientsPerPage,
    currentPage * clientsPerPage
  );

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  return (
    <Wrapper>
      <Header onLogout={onLogout} />
      <Main>
        <h2>Gestión de Clientes</h2>
        <Stats>
          <StatCard>
            <div>{clients.length}</div>
            <div>Total</div>
          </StatCard>
          <StatCard>
            <div>{filtered.filter(c => c.level === 1).length}</div>
            <div>No Asociados</div>
          </StatCard>
          <StatCard>
            <div>{filtered.filter(c => c.level === 2).length}</div>
            <div>Clientes</div>
          </StatCard>
          <StatCard>
            <div>{filtered.filter(c => c.level === 3).length}</div>
            <div>Personalizados</div>
          </StatCard>
          <WeeklyActivityCard>
            <div>35</div>
            <div>Actividad Semanal</div>
          </WeeklyActivityCard>
          <MonthlyActivityCard>
            <div>120</div>
            <div>Actividad Mensual</div>
          </MonthlyActivityCard>
        </Stats>
        <SearchBar>
          <Input
            placeholder="Buscar por nombre o teléfono..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <Select value={levelFilter} onChange={e => setLevelFilter(e.target.value)}>
            <option value="all">Todos los niveles</option>
            <option value="1">No asociado</option>
            <option value="2">Cliente</option>
            <option value="3">Personalizado</option>
          </Select>
        </SearchBar>
        <LoadBtn>Cargar Teléfonos</LoadBtn>
        <Table as={StyledTable}>
          <thead>
            <tr>
              <StyledTh>Cliente</StyledTh>
              <StyledTh>Teléfono</StyledTh>
              <StyledTh>Nivel</StyledTh>
              <StyledTh>Última Actividad</StyledTh>
              <StyledTh>Estado</StyledTh>
            </tr>
          </thead>
          <tbody>
            {paginatedClients.map(c => (
              <ClientRow key={c.id} client={{ ...c, levelName: levelMapping[c.level] }} />
            ))}
          </tbody>
        </Table>
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '1rem' }}>
          <button onClick={() => handlePageChange(currentPage - 1)} disabled={currentPage === 1}>
            Anterior
          </button>
          <span style={{ margin: '0 1rem' }}>Página {currentPage} de {totalPages}</span>
          <button onClick={() => handlePageChange(currentPage + 1)} disabled={currentPage === totalPages}>
            Siguiente
          </button>
        </div>
      </Main>
    </Wrapper>
  );
}