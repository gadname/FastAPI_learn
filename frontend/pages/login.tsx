import React, { useState, FormEvent, useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../context/AuthContext';

const LoginPage: React.FC = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState<string | null>(null);
    const { login, isAuthenticated, isLoading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isLoading && isAuthenticated) {
            router.push('/');
        }
    }, [isAuthenticated, isLoading, router]);

    const handleSubmit = async (event: FormEvent) => {
        event.preventDefault();
        setError(null);

        try {
            const response = await fetch('/api/v1/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams({
                    username: username,
                    password: password,
                }),
            });

            if (response.ok) {
                const data = await response.json();
                login(data.access_token); // Use login from AuthContext
            } else {
                const errorData = await response.json();
                setError(errorData.detail || 'Login failed');
            }
        } catch (err) {
            setError('An unexpected error occurred. Please try again.');
            console.error('Login error:', err);
        }
    };

    // Prevent rendering login form if already authenticated and not loading
    if (isLoading || (!isLoading && isAuthenticated)) {
        return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
    }

    return (
        <div style={styles.container}>
            <form onSubmit={handleSubmit} style={styles.form}>
                <h2>Login</h2>
                {error && <p style={styles.error}>{error}</p>}
                <div style={styles.inputGroup}>
                    <label htmlFor="username" style={styles.label}>Username</label>
                    <input
                        type="text"
                        id="username"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                        style={styles.input}
                    />
                </div>
                <div style={styles.inputGroup}>
                    <label htmlFor="password" style={styles.label}>Password</label>
                    <input
                        type="password"
                        id="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                        style={styles.input}
                    />
                </div>
                <button type="submit" style={styles.button}>Login</button>
                 <p style={styles.registerLink}>
                    Don't have an account? <a href="/register">Register here</a>
                </p>
            </form>
        </div>
    );
};

// Styles remain the same as previously defined
const styles: { [key: string]: React.CSSProperties } = {
    container: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        backgroundColor: '#f0f2f5',
    },
    form: {
        padding: '40px',
        borderRadius: '8px',
        backgroundColor: '#ffffff',
        boxShadow: '0 4px 12px rgba(0, 0, 0, 0.1)',
        width: '100%',
        maxWidth: '400px',
        textAlign: 'center',
    },
    inputGroup: {
        marginBottom: '20px',
        textAlign: 'left',
    },
    label: {
        display: 'block',
        marginBottom: '8px',
        color: '#333',
        fontWeight: 'bold',
    },
    input: {
        width: '100%',
        padding: '12px',
        border: '1px solid #ccc',
        borderRadius: '4px',
        boxSizing: 'border-box',
        fontSize: '16px',
    },
    button: {
        width: '100%',
        padding: '12px',
        backgroundColor: '#007bff',
        color: 'white',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        fontSize: '16px',
        fontWeight: 'bold',
        transition: 'background-color 0.3s ease',
    },
    error: {
        color: 'red',
        marginBottom: '20px',
    },
    registerLink: {
        marginTop: '20px',
    }
};

export default LoginPage;
