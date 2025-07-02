import styled from 'styled-components';
import { Link } from 'react-router-dom';

export const Wrapper = styled.div``;

export const Main = styled.main`
  padding: 1rem 2rem 2rem; /* Reducir solo el padding superior */
  background: var(--surface);
  height: auto; /* Ajustar el alto automáticamente al contenido */
`;

export const Stats = styled.div`
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;

  @media (max-width: 768px) {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
  }
`;

export const StatCard = styled.div`
  background: var(--surface);
  padding: 1rem;
  border: 1px solid var(--border);
  border-radius: 12px;
  text-align: center;
  width: 160px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;

  > div:first-child {
    font-size: 28px;
    font-weight: 700;
    color: var(--brand-dark);
  }
`;

export const WeeklyActivityCard = styled(StatCard)`
  background: var(--weekly);
`;

export const MonthlyActivityCard = styled(StatCard)`
  background: var(--monthly);
`;

export const SearchBar = styled.div`
  display: flex;
  gap: 12px;
  margin-bottom: 1rem;
  flex-wrap: wrap;
`;

export const Input = styled.input`
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  flex: 1;
  min-width: 0;

  &:focus {
    outline: none;
    border-color: var(--brand-gold);
  }
`;

export const Select = styled.select`
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  width: 200px;
`;

export const LoadBtn = styled.button`
  padding: 0.5rem 1rem;
  background: var(--brand-dark);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;

  &:hover {
    background: #16283c;
  }
`;

export const Table = styled.table`
  width: 100%;
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  overflow: hidden;

  tbody tr:hover {
    background: #f1f5f9;
  }

  @media (max-width: 640px) {
    display: block;
    overflow-x: auto;
  }
`;

export const Th = styled.th`
  text-align: left;
  padding: 0.75rem 1rem;
  background: var(--surface);
  position: sticky;
  top: 0;
  box-shadow: 0 2px 2px rgba(0,0,0,0.05);
`;

export const StyledTh = styled.th`
  text-align: center;
  width: calc(100% / 5);
`;

export const StyledTable = styled.table`
  table-layout: fixed;
  width: 100%;
`;

export const Td = styled.td`
  padding: 0.75rem 1rem;
  border-top: 1px solid var(--border);

  svg {
    vertical-align: middle;
    margin-right: 4px;
  }
`;

export const LevelTag = styled.span`
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--brand-dark);
  background: ${({level}) =>
    level === 1
      ? 'var(--basic)'
      : level === 2
      ? 'var(--premium)'
      : 'var(--vip)'};
`;

export const StatusChip = styled.span`
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--success);
  color: #fff;
`;