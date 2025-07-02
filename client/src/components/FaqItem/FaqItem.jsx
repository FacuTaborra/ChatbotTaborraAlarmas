import React, { useState } from 'react';
import { FaqContainer, FaqTitle, FaqDetails, FaqLink, FaqButtons, StatsSection } from './FaqItem.styles';

export default function FaqItem({ faq, onEdit, onDelete }) {
  const [isActive, setIsActive] = useState(false);

  const toggleActive = () => {
    setIsActive(!isActive);
  };

  return (
    <FaqContainer className={isActive ? 'active' : ''} onClick={toggleActive}>
      <FaqTitle>{faq.title}</FaqTitle>
      <FaqDetails>
        <p><strong>Modelo:</strong> {faq.model}</p>
        <p><strong>Descripción:</strong> {faq.desc}</p>
        <p><strong>Link:</strong> <FaqLink href={faq.link} target="_blank" rel="noopener noreferrer">Ver video</FaqLink></p>
        <StatsSection>
          <h4>Estadísticas</h4>
          <ul>
            <li><strong>Veces consultada:</strong> {faq.consulted}</li>
            <li><strong>Veces resuelto:</strong> {faq.resolved}</li>
            <li><strong>Veces no resuelto:</strong> {faq.unresolved}</li>
          </ul>
        </StatsSection>
      </FaqDetails>
      <FaqButtons>
        <button onClick={(e) => { e.stopPropagation(); onEdit(faq.id); }}>Editar</button>
        <button onClick={(e) => { e.stopPropagation(); onDelete(faq.id); }}>Borrar</button>
      </FaqButtons>
    </FaqContainer>
  );
}
