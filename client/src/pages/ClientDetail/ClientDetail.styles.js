import styled from 'styled-components';

export const Wrapper = styled.div`
  background: var(--surface);
  min-height: 100vh; /* Ajustar el alto automáticamente al tamaño de pantalla */
`;

export const MainContainer = styled.div`
  max-width: 800px;
  margin: 0 auto;
  margin-top: 2rem;
  padding: 2rem;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

  h2 {
    text-align: center;
    margin-bottom: 1rem;
  }

  p {
    margin: 0.5rem 0;
    font-size: 1rem;
  }

  strong {
    font-weight: bold;
  }
`;
