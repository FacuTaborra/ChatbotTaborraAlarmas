import { FiLogOut } from 'react-icons/fi';
import logo from '../../assets/logo.png';
import { HeaderWrap, Logo, Nav, HeaderLink, LogoutBtn } from './Header.styles';

export default function Header({ onLogout }) {
  return (
    <HeaderWrap>
      <Logo>
        <img src={logo} alt="logo" width="32" height="32" />
        Taborra Alarmas SRL
      </Logo>
      <Nav>
        <HeaderLink to="/dashboard">Dashboard</HeaderLink>
        <HeaderLink to="/faqs">Preguntas Frecuentes</HeaderLink>
      </Nav>
      <LogoutBtn onClick={onLogout}>
        <FiLogOut /> Cerrar Sesión
      </LogoutBtn>
    </HeaderWrap>
  );
}