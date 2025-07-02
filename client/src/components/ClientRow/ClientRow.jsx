import { FaPhoneAlt, FaCalendarAlt } from 'react-icons/fa';
import { Tr, Td, LevelTag, StatusChip } from './ClientRow.styles';

export default function ClientRow({ client, onClick }) {
  return (
    <Tr onClick={onClick} style={{ cursor: 'pointer' }}>
      <Td>{client.name}</Td>
      <Td><FaPhoneAlt size={14} /> {client.phone}</Td>
      <Td><LevelTag level={client.level}>{client.levelName}</LevelTag></Td>
      <Td>{client.last}</Td>
      <Td><StatusChip>Activo</StatusChip></Td>
    </Tr>
  );
}
