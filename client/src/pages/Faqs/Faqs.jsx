import { useState } from 'react';
import {
  Wrapper,
  Main,
  Stats,
  StatCard,
  SearchBar,
  Input
} from '../Dashboard/Dashboard.styles';
import Header from '../../components/Header/Header';
import { TabsContainer, TabButton, CenteredForm, FormContainer, StyledInput, StyledSelect, StyledTextArea, SubmitBtn, MainContainer, FilterContainer } from './Faqs.styles';
import FaqItem from '../../components/FaqItem/FaqItem';

export default function Faqs({ onLogout }) {
  const models = [
    { id: 1, name: 'Modelo A' },
    { id: 2, name: 'Modelo B' },
    { id: 3, name: 'Modelo C' },
  ];
  const [model, setModel] = useState('');
  const [title, setTitle] = useState('');
  const [desc, setDesc] = useState('');
  const [link, setLink] = useState('');
  const [activeTab, setActiveTab] = useState('view');
  const [search, setSearch] = useState('');
  const [modelFilter, setModelFilter] = useState('');

  const handleSubmit = e => {
    e.preventDefault();
    const payload = { model_name: model, title_faq: title, desc_faq: desc, link };
    console.log('submit', payload);
  };

  const faqs = [
    { id: 1, model: 'Modelo A', title: 'Cómo configurar la alarma', desc: 'Pasos para configurar la alarma.', link: 'https://example.com/video1', consulted: 25 },
    { id: 2, model: 'Modelo B', title: 'Cómo reiniciar la cámara', desc: 'Instrucciones para reiniciar la cámara.', link: 'https://example.com/video2', consulted: 15 },
    { id: 3, model: 'Modelo C', title: 'Cómo cambiar la batería', desc: 'Guía para cambiar la batería.', link: 'https://example.com/video3', consulted: 30 },
  ];

  const handleEdit = id => {
    console.log(`Editar FAQ con ID: ${id}`);
  };

  const handleDelete = id => {
    console.log(`Borrar FAQ con ID: ${id}`);
  };

  return (
    <Wrapper>
      <Header onLogout={onLogout} />
      <MainContainer>
        <h2 style={{ textAlign: 'center' }}>Preguntas Frecuentes</h2>
        <Stats style={{ justifyContent: 'center' }}>
          <StatCard>
            <div>10</div>
            <div>FAQs Consultadas esta Semana</div>
          </StatCard>
          <StatCard>
            <div>40</div>
            <div>FAQs Consultadas este Mes</div>
          </StatCard>
          <StatCard>
            <div>25</div>
            <div>Total Resueltas</div>
          </StatCard>
          <StatCard>
            <div>15</div>
            <div>Total No Resueltas</div>
          </StatCard>
        </Stats>
        <hr style={{ margin: '2rem 0', border: '1px solid #ccc' }} />
        <SearchBar>
          <FilterContainer>
            <Input
              placeholder="Buscar por título o modelo..."
              value={search}
              onChange={e => setSearch(e.target.value)}
            />
            <StyledSelect value={modelFilter} onChange={e => setModelFilter(e.target.value)}>
              <option value="">Todos los modelos</option>
              {models.map(m => (
                <option key={m.id} value={m.name}>{m.name}</option>
              ))}
            </StyledSelect>
          </FilterContainer>
        </SearchBar>
        <TabsContainer>
          <TabButton active={activeTab === 'view'} onClick={() => setActiveTab('view')}>
            Ver FAQs
          </TabButton>
          <TabButton active={activeTab === 'add'} onClick={() => setActiveTab('add')}>
            Agregar FAQ
          </TabButton>
        </TabsContainer>
        {activeTab === 'view' && (
          <div>
            {faqs
              .filter(
                faq =>
                  (faq.title.toLowerCase().includes(search.toLowerCase()) || faq.model.toLowerCase().includes(search.toLowerCase())) &&
                  (modelFilter === '' || faq.model === modelFilter)
              )
              .map(faq => (
                <FaqItem key={faq.id} faq={faq} onEdit={handleEdit} onDelete={handleDelete} />
              ))}
          </div>
        )}
        {activeTab === 'add' && (
          <FormContainer>
            <h3 style={{ textAlign: 'center', marginBottom: '1rem' }}>Agregar nueva pregunta frecuente</h3>
            <CenteredForm onSubmit={handleSubmit}>
              <StyledSelect value={model} onChange={e => setModel(e.target.value)} required>
                <option value="">Modelo de Alarma/Cámara</option>
                {models.map(m => (
                  <option key={m.id} value={m.name}>{m.name}</option>
                ))}
              </StyledSelect>
              <StyledInput
                placeholder="Título"
                value={title}
                onChange={e => setTitle(e.target.value)}
                required
              />
              <StyledTextArea
                rows="4"
                placeholder="Descripción"
                value={desc}
                onChange={e => setDesc(e.target.value)}
                required
              />
              <StyledInput
                placeholder="Link de video (opcional)"
                value={link}
                onChange={e => setLink(e.target.value)}
              />
              <SubmitBtn type="submit">Guardar</SubmitBtn>
            </CenteredForm>
          </FormContainer>
        )}
      </MainContainer>
    </Wrapper>
  );
}