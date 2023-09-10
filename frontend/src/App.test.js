import { render, screen } from '@testing-library/react';
import App from './App';

test('Базовая проверка', () => {
  render(<App />);
  const linkElement = screen.getByText(/Карта/i);
  expect(linkElement).toBeInTheDocument();
});
