import styled from 'styled-components';

export const FaqContainer = styled.div`
  border: 1px solid #ccc;
  border-radius: 8px;
  padding: 1rem;
  margin-bottom: 1rem;
  background-color: #f9f9f9;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: background-color 0.3s ease, box-shadow 0.3s ease;
  max-width: 800px; /* Limitar el ancho de las tarjetas */
  margin-left: auto;
  margin-right: auto;

  &.active {
    background-color: #e0e0e0; /* Cambiar el color de activación a gris */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
`;

export const FaqTitle = styled.h3`
  margin: 0;
  font-size: 1.25rem;
  color: #333;
`;

export const FaqDetails = styled.div`
  margin-top: 0.5rem;
  display: none;

  ${FaqContainer}.active & {
    display: block;
  }
`;

export const FaqLink = styled.a`
  color: #007bff;
  text-decoration: none;

  &:hover {
    text-decoration: underline;
  }
`;

export const FaqButtons = styled.div`
  margin-top: 1rem;
  display: flex;
  gap: 0.5rem;

  button {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
    transition: background-color 0.3s ease;

    &:hover {
      background-color: #007bff;
      color: #fff;
    }
  }
`;

export const StatsSection = styled.div`
  margin-top: 1rem;
  padding: 1rem;
  background-color: #f1f5f9;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

  h4 {
    margin-bottom: 0.5rem;
    font-size: 1.1rem;
    color: #333;
  }

  ul {
    list-style: none;
    padding: 0;

    li {
      margin-bottom: 0.5rem;
      font-size: 0.9rem;
      color: #555;

      strong {
        color: #007bff;
      }
    }
  }
`;
