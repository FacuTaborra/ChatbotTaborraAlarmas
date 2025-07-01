import { FaPhoneAlt, FaCalendarAlt } from 'react-icons/fa';
import { Tr, Td, LevelTag, StatusChip } from './ClientRow.styles';

export default function ClientRow({ client }) {
  return (
    <Tr>
      <Td>{client.name}</Td>
      <Td><FaPhoneAlt size={14} /> {client.phone}</Td>
      <Td><LevelTag level={client.level}>{client.level}</LevelTag></Td>
      <Td><FaCalendarAlt size={14} /> {client.registered}</Td>
      <Td>{client.last}</Td>
      <Td><StatusChip>Activo</StatusChip></Td>
    </Tr>
  );
}
