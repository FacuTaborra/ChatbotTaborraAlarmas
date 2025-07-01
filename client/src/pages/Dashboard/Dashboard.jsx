import { useState } from 'react';
import { FiLogOut } from 'react-icons/fi';
import { FaCalendarAlt, FaPhoneAlt } from 'react-icons/fa';
import {
  Wrapper,
  Header,
  Logo,
  LogoutBtn,
  Main,
  Stats,
  StatCard,
  SearchBar,
  Input,
  Select,
  LoadBtn,
  Table,
  Th,
  Td,
  LevelTag,
  StatusChip
} from './Dashboard.styles';
import logo from '../../assets/logo.png';
import ClientRow from '../../components/ClientRow/ClientRow';

const clients = [
  {
    id: 1,
    name: 'Juan Carlos Pérez',
    phone: '+54 91 1234-56789',
    level: 'BÁSICO',
    registered: '14/1/2024',
    last: '19/1/2024',
  },
  {
    id: 2,
    name: 'María González',
    phone: '+54 91 1987-65432',
    level: 'PREMIUM',
    registered: '9/1/2024',
    last: '18/1/2024',
  },
  {
    id: 3,
    name: 'Roberto Silva',
    phone: '+54 91 5555-5555',
    level: 'VIP',
    registered: '4/1/2024',
    last: '17/1/2024',
  }
];

export default function Dashboard({ onLogout }) {
  const [levelFilter, setLevelFilter] = useState('all');
  const [search, setSearch] = useState('');

  const filtered = clients.filter(c => {
    const matchLevel = levelFilter === 'all' || c.level === levelFilter;
    const matchSearch =
      c.name.toLowerCase().includes(search.toLowerCase()) ||
      c.phone.includes(search);
    return matchLevel && matchSearch;
  });

  return (
    <Wrapper>
      <Header>
        <Logo>
          <img src={logo} alt="logo" width="32" height="32" />
          Taborra Alarmas SRL
        </Logo>
        <LogoutBtn onClick={onLogout}>
          <FiLogOut /> Cerrar Sesión
        </LogoutBtn>
      </Header>
      <Main>
        <h2>Gestión de Clientes</h2>
        <Stats>
          <StatCard>
            <div>5</div>
            <div>Total</div>
          </StatCard>
          <StatCard>
            <div>4</div>
            <div>Clientes no Asociados</div>
          </StatCard>
          <StatCard>
            <div>2</div>
            <div>Clientes Asociados</div>
          </StatCard>
          <StatCard>
            <div>1</div>
            <div>Clientes Personalizado</div>
          </StatCard>
        </Stats>
        <SearchBar>
          <Input
            placeholder="Buscar por nombre o teléfono..."
            value={search}
            onChange={e => setSearch(e.target.value)}
          />
          <Select value={levelFilter} onChange={e => setLevelFilter(e.target.value)}>
            <option value="all">Todos los niveles</option>
            <option value="BÁSICO">Básico</option>
            <option value="PREMIUM">Premium</option>
            <option value="VIP">VIP</option>
          </Select>
        </SearchBar>
        <LoadBtn>Cargar Teléfonos</LoadBtn>
        <Table>
          <thead>
            <tr>
              <Th>Cliente</Th>
              <Th>Teléfono</Th>
              <Th>Nivel</Th>
              <Th>Fecha de Registro</Th>
              <Th>Última Actividad</Th>
              <Th>Estado</Th>
            </tr>
          </thead>
          <tbody>
            {filtered.map(c => (
              <ClientRow key={c.id} client={c} />
            ))}
          </tbody>
        </Table>
      </Main>
    </Wrapper>
  );
}