import styled from 'styled-components';
import { Link } from 'react-router-dom';

export const HeaderWrap = styled.header`
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #000;
  padding: 0 2rem;
  height: 64px;
  box-shadow: 0 2px 4px rgba(0,0,0,.05);
`;

export const Logo = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 600;
  color: #fff;
  img {
    width: 40px;
    height: 40px;
    border-radius: 10px;
  }
`;

export const Nav = styled.nav`
  display: flex;
  gap: 1rem;
`;

export const HeaderLink = styled(Link)`
  color: #fff;
  text-decoration: none;
  font-weight: 600;
  font-size: 1rem;
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  transition: background-color 0.5s ease;

  &:hover {
    background-color: rgba(255, 255, 255, 0.43);
    text-decoration: none;
  }
`;

export const LogoutBtn = styled.button`
  background: var(--brand-gold);
  color: #000;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 8px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;

  &:hover {
    background: #e2b94d;
  }
`;