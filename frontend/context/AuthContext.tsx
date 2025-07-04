import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/router';

interface AuthContextType {
    isAuthenticated: boolean;
    token: string | null;
    isLoading: boolean;
    login: (newToken: string) => void;
    logout: () => void;
    checkAuth: () => Promise<void>; // Added to verify token with backend
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
    const [token, setToken] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    const fetchCurrentUser = async (currentToken: string) => {
        try {
            const response = await fetch('/api/v1/auth/users/me', {
                headers: {
                    Authorization: `Bearer ${currentToken}`,
                },
            });
            if (response.ok) {
                // const user = await response.json(); // Optionally use user data
                setToken(currentToken);
            } else {
                localStorage.removeItem('token');
                setToken(null);
                if (router.pathname !== '/login' && router.pathname !== '/register') {
                    router.push('/login');
                }
            }
        } catch (error) {
            console.error('Error verifying token:', error);
            localStorage.removeItem('token');
            setToken(null);
            if (router.pathname !== '/login' && router.pathname !== '/register') {
                router.push('/login');
            }
        }
    };

    const checkAuth = async () => {
        setIsLoading(true);
        const storedToken = localStorage.getItem('token');
        if (storedToken) {
            await fetchCurrentUser(storedToken);
        } else {
            setToken(null);
            if (router.pathname !== '/login' && router.pathname !== '/register') {
                 // router.push('/login'); // Commented out to prevent premature redirect before _app logic
            }
        }
        setIsLoading(false);
    };

    useEffect(() => {
        checkAuth();
    // eslint-disable-next-line react-hooks/exhaustive-deps
    }, []); // Run once on mount

    const login = (newToken: string) => {
        localStorage.setItem('token', newToken);
        setToken(newToken);
        router.push('/');
    };

    const logout = () => {
        localStorage.removeItem('token');
        setToken(null);
        router.push('/login');
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated: !!token, token, isLoading, login, logout, checkAuth }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = (): AuthContextType => {
    const context = useContext(AuthContext);
    if (context === undefined) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};
