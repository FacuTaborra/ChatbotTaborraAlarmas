import styled from 'styled-components';

export const Container = styled.div`
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--surface);
`;

export const Card = styled.div`
  background: var(--bg);
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0,0,0,0.08);
  width: 100%;
  max-width: 400px;
`;

export const Logo = styled.img`
  display: block;
  border-radius: 20px;
  margin: 0 auto 1rem;
  width: 80px;
`;

export const Title = styled.h1`
  text-align: center;
  margin-bottom: 1rem;
  font-weight: 600;
`;

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

export const Input = styled.input`
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-size: 1rem;

  &:focus {
    outline: none;
    border-color: var(--brand-gold);
  }
`;

export const Button = styled.button`
  padding: 0.75rem 1rem;
  background: var(--brand-dark);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;

  &:disabled {
    opacity: 0.65;
  }
`;