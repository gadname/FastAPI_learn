import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import '@testing-library/jest-dom';
import Home from './index';

// Mock fetch
global.fetch = jest.fn();

// Mock environment variable
const mockApiUrl = 'http://mockapi.com';
process.env.NEXT_PUBLIC_API_URL = mockApiUrl;

describe('Home Page - Create Cat Form', () => {
  beforeEach(() => {
    // Reset fetch mock for each test
    (global.fetch as jest.Mock).mockClear();
    // Reset message by re-rendering or specific state reset if possible,
    // for now, re-rendering is implicit with each `render` call in tests.
  });

  test('renders the form elements correctly', () => {
    render(<Home />);
    expect(screen.getByRole('heading', { name: /create a new cat/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/breed/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/age/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/weight/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /create cat/i })).toBeInTheDocument();
  });

  test('allows user to fill the form', () => {
    render(<Home />);
    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Whiskers' } });
    fireEvent.change(screen.getByLabelText(/breed/i), { target: { value: 'Siamese' } });
    fireEvent.change(screen.getByLabelText(/age/i), { target: { value: '2' } });
    fireEvent.change(screen.getByLabelText(/weight/i), { target: { value: '5' } });

    expect(screen.getByLabelText(/name/i)).toHaveValue('Whiskers');
    expect(screen.getByLabelText(/breed/i)).toHaveValue('Siamese');
    expect(screen.getByLabelText(/age/i)).toHaveValue(2);
    expect(screen.getByLabelText(/weight/i)).toHaveValue(5);
  });

  test('submits the form successfully and displays success message', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: true,
      json: async () => ({ id: 1, name: 'Whiskers', breed: 'Siamese', age: 2, weight: 5 }),
    });

    render(<Home />);

    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'Whiskers' } });
    fireEvent.change(screen.getByLabelText(/breed/i), { target: { value: 'Siamese' } });
    fireEvent.change(screen.getByLabelText(/age/i), { target: { value: '2' } });
    fireEvent.change(screen.getByLabelText(/weight/i), { target: { value: '5' } });
    fireEvent.click(screen.getByRole('button', { name: /create cat/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledWith(`${mockApiUrl}/api/v1/cat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name: 'Whiskers', breed: 'Siamese', age: 2, weight: 5 }),
      });
    });

    await waitFor(() => {
      expect(screen.getByText(/cat "Whiskers" created successfully!/i)).toBeInTheDocument();
    });

    // Check if form is cleared
    expect(screen.getByLabelText(/name/i)).toHaveValue('');
    expect(screen.getByLabelText(/breed/i)).toHaveValue('');
    expect(screen.getByLabelText(/age/i)).toHaveValue(null); // Assuming number input clears to null or empty string handled as such
    expect(screen.getByLabelText(/weight/i)).toHaveValue(null);
  });

  test('displays error message on API failure', async () => {
    (global.fetch as jest.Mock).mockResolvedValueOnce({
      ok: false,
      statusText: 'Bad Request',
      json: async () => ({ detail: 'Invalid data provided' }),
    });

    render(<Home />);

    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'BadCat' } });
    // ... fill other fields ...
    fireEvent.click(screen.getByRole('button', { name: /create cat/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    await waitFor(() => {
      expect(screen.getByText(/error: Invalid data provided/i)).toBeInTheDocument();
    });

    // Form should not be cleared
    expect(screen.getByLabelText(/name/i)).toHaveValue('BadCat');
  });

  test('displays error message on network error', async () => {
    (global.fetch as jest.Mock).mockRejectedValueOnce(new Error('Network failure'));

    render(<Home />);
    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'NetErrorCat' } });
    // ... fill other fields ...
    fireEvent.click(screen.getByRole('button', { name: /create cat/i }));

    await waitFor(() => {
      expect(global.fetch).toHaveBeenCalledTimes(1);
    });

    await waitFor(() => {
      expect(screen.getByText(/failed to submit the form. please check the console./i)).toBeInTheDocument();
    });
  });

  test('displays error if API URL is not configured', async () => {
    process.env.NEXT_PUBLIC_API_URL = ''; // Temporarily unset
    render(<Home />);

    fireEvent.change(screen.getByLabelText(/name/i), { target: { value: 'NoApiUrlCat' } });
    // ... fill other fields ...
    fireEvent.click(screen.getByRole('button', { name: /create cat/i }));

    await waitFor(() => {
      expect(screen.getByText(/api url is not configured./i)).toBeInTheDocument();
    });
    expect(global.fetch).not.toHaveBeenCalled();
    process.env.NEXT_PUBLIC_API_URL = mockApiUrl; // Reset for other tests
  });

  // Note on input validation:
  // HTML5 'required' and 'type="number"' with 'min' attributes handle many client-side validation cases.
  // Testing these exact behaviors is often better suited for E2E tests.
  // These unit tests focus on the component's reaction to submission attempts and API responses.
  // For example, if age were not a number, `Number(age)` would become `NaN`,
  // which the backend should ideally validate and return an error for.
  // We've tested the display of such backend errors.
});
