import styled from 'styled-components';

export const Tr = styled.tr``;

export const Td = styled.td`
  padding: 1.15rem 1rem;
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
  background: ${({ level }) =>
    level === 'BÁSICO'
      ? 'var(--basic)'
      : level === 'PREMIUM'
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