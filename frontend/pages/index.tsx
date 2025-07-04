import React from 'react';
import { useAuth } from '../context/AuthContext';

const HomePage: React.FC = () => {
    const { logout, token } = useAuth(); // Assuming 'user' might be added to AuthContext later

    // If checkAuth is still running and token is not yet available,
    // or if already redirected by AppLogic, this might show briefly.
    // AppLogic in _app.tsx handles the primary redirection if not authenticated.
    if (!token) {
      // This is a fallback, AppLogic should prevent this state mostly.
      return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Authenticating...</div>;
    }

    return (
        <div style={styles.container}>
            <h1>Welcome to the Application</h1>
            <p>This is your main dashboard page.</p>
            <p>You are logged in!</p>
            {/* You could display user information here if available from useAuth() */}
            <button
                onClick={logout} // Use logout from AuthContext
                style={styles.button}
            >
                Logout
            </button>
        </div>
    );
};

const styles: { [key: string]: React.CSSProperties } = {
    container: {
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        backgroundColor: '#f8f9fa', // Light gray background
        padding: '20px',
        textAlign: 'center',
        fontFamily: 'Arial, sans-serif',
    },
    title: {
        color: '#333',
        marginBottom: '10px',
    },
    paragraph: {
        color: '#555',
        marginBottom: '20px',
    },
    button: {
        marginTop: '20px',
        padding: '12px 25px',
        backgroundColor: '#dc3545', // Bootstrap danger red
        color: 'white',
        border: 'none',
        borderRadius: '5px',
        cursor: 'pointer',
        fontSize: '16px',
        fontWeight: 'bold',
        boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
        transition: 'background-color 0.2s ease-in-out',
    },
    // button:hover pseudo-class would need to be in a CSS file or handled by a styling library
};

export default HomePage;
