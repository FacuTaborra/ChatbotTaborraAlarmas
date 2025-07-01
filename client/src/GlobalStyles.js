import { createGlobalStyle } from 'styled-components';

export const GlobalStyles = createGlobalStyle`
  :root {
    --brand-dark: #0d1b2a;
    --brand-gold: #ffd166;
    --bg: #ffffff;
    --surface: #f8fafc;
    --text: #111827;
    --border: #e5e7eb;
    --success: #22c55e;
    --basic: #dbeafe;
    --premium: #fef3c7;
    --vip: #f3e8ff;
  }

  body {
    margin: 0;
    font-family: 'Inter', sans-serif;
    background: var(--bg);
    color: var(--text);
  }

  ::placeholder {
    color: #9ca3af;
  }

  table {
    border-collapse: collapse;
    width: 100%;
  }

  .spin {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }
`;