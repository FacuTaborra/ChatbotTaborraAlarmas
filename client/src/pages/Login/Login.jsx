import { useState } from 'react';
import { FiLoader } from 'react-icons/fi';
import { Container, Card, Form, Input, Button, Title, Logo } from './Login.styles';
import logo from '../../assets/logo.png';

export default function Login({ onLogin }) {
  const [user, setUser] = useState('');
  const [pass, setPass] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    setLoading(true);
    setTimeout(() => {
      onLogin('token');
    }, 1000);
  };

  return (
    <Container>
      <Card>
        <Logo src={logo} alt="Logo" />
        <Title>Iniciar Sesión</Title>
        <Form onSubmit={handleSubmit}>
          <Input
            placeholder="Usuario"
            value={user}
            onChange={(e) => setUser(e.target.value)}
            required
          />
          <Input
            type="password"
            placeholder="Contraseña"
            value={pass}
            onChange={(e) => setPass(e.target.value)}
            required
          />
          <Button type="submit" disabled={loading}>
            {loading && <FiLoader className="spin" />}
            Entrar
          </Button>
        </Form>
      </Card>
    </Container>
  );
}