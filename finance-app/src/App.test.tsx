import { render, screen } from '@testing-library/react';
import { test, expect } from '@jest/globals';
import '@testing-library/jest-dom';
import App from './App.tsx';
import React from 'react';

test('renders learn react link', () => {
 render(<App />);
 const linkElement = screen.getByText(/learn react/i);
 expect(linkElement).toBeInTheDocument();
});