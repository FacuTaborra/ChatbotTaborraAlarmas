import styled from 'styled-components';

export const TabsContainer = styled.div`
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
`;

export const TabButton = styled.button`
  margin-right: 1rem;
  padding: 0.5rem 1rem;
  cursor: pointer;
  background: ${({ active }) => (active ? '#2196f3' : '#ccc')};
  color: #fff;
  border: none;
  border-radius: 4px;
`;

export const CenteredForm = styled.form`
  margin-top: 2rem;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;

  select,
  input,
  textarea {
    width: 50%;
    margin-top: 1rem;
  }

  button {
    margin-top: 1rem;
  }
`;

export const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 500px;
`;

export const TextArea = styled.textarea`
  padding: 0.75rem 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  font-family: inherit;
  resize: vertical;

  &:focus {
    outline: none;
    border-color: var(--brand-gold);
  }
`;

export const SubmitBtn = styled.button`
  padding: 0.75rem 1rem;
  background: var(--brand-dark);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
`;

export const FormContainer = styled.div`
  background-color: #f4f4f4;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  width: 60%;
  margin: 0 auto;
`;

export const StyledInput = styled.input`
  width: 80%;
  margin-top: 1rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
`;

export const StyledSelect = styled.select`
  width: 80%;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
`;

export const StyledTextArea = styled.textarea`
  width: 80%;
  margin-top: 1rem;
  padding: 0.5rem;
  border: 1px solid #ccc;
  border-radius: 4px;
`;

export const MainContainer = styled.div`
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  height: auto; /* Ajustar el alto automáticamente al contenido */
`;

export const FilterContainer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
  width: 100%;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;

  input {
    flex: 1;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    height: 20px;
  }

  select {
    width: 200px;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 4px;
    height: 40px; /* Ajustar altura para alineación */
  }
`;