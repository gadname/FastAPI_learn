// frontend/pages/login.tsx
import React, { useState, FormEvent } from 'react';
import { useRouter } from 'next/router';

const LoginPage: React.FC = () => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [error, setError] = useState<string | null>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const router = useRouter();

    const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        setError(null);
        setLoading(true);

        try {
            // The backend expects form data, not JSON, for OAuth2PasswordRequestForm
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch('/api/v1/auth/login', { // Assuming Next.js proxy or direct URL
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData.toString(),
            });

            setLoading(false);

            if (response.ok) {
                const data = await response.json();
                localStorage.setItem('accessToken', data.access_token);
                // Redirect to a protected page or dashboard
                router.push('/'); // Or '/dashboard'
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Login failed. Please check your credentials.');
            }
        } catch (err) {
            setLoading(false);
            setError('An unexpected error occurred. Please try again.');
            console.error('Login error:', err);
        }
    };

    return (
        <div style={{ maxWidth: '400px', margin: '50px auto', padding: '20px', border: '1px solid #ccc', borderRadius: '5px' }}>
            <h1>Login</h1>
            <form onSubmit={handleSubmit}>
                <div style={{ marginBottom: '15px' }}>
                    <label htmlFor="username" style={{ display: 'block', marginBottom: '5px' }}>Username</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
                    />
                </div>
                <div style={{ marginBottom: '15px' }}>
                    <label htmlFor="password" style={{ display: 'block', marginBottom: '5px' }}>Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={{ width: '100%', padding: '8px', boxSizing: 'border-box' }}
                    />
                </div>
                {error && <p style={{ color: 'red' }}>{error}</p>}
                <button type="submit" disabled={loading} style={{ padding: '10px 15px', backgroundColor: '#0070f3', color: 'white', border: 'none', borderRadius: '5px', cursor: 'pointer' }}>
                    {loading ? 'Logging in...' : 'Login'}
                </button>
            </form>
            {/* Optional: Link to registration page */}
            {/* <p style={{ marginTop: '15px' }}>
                Don't have an account? <a href="/register">Register here</a>
            </p> */}
        </div>
    );
};

export default LoginPage;
