import styled from 'styled-components';

export const Tr = styled.tr``;

export const Td = styled.td`
  padding: 1.15rem 1rem;
  border-top: 1px solid var(--border);
  text-align: center;

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
  color: #fff;
  background: ${({ level }) => {
    switch (level) {
      case 1:
        return '#e57373'; 
      case 2:
        return '#64b5f6'; 
      case 3:
        return '#81c784'; 
      default:
        return '#b0bec5';
    }
  }};
`;

export const StatusChip = styled.span`
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  background: var(--success);
  color: #fff;
`;