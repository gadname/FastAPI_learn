import React, { useEffect } from 'react';
import type { AppProps } from 'next/app';
import { AuthProvider, useAuth } from '../context/AuthContext';
import { useRouter } from 'next/router';
import '../styles/globals.css'; // Assuming a global stylesheet

// This component will handle redirect logic based on auth state
const AppLogic: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading, checkAuth } = useAuth();
  const router = useRouter();
  const publicPaths = ['/login', '/register'];

  useEffect(() => {
    // Initial check
    checkAuth();
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);


  useEffect(() => {
    if (!isLoading) {
      const pathIsProtected = !publicPaths.includes(router.pathname);
      if (pathIsProtected && !isAuthenticated) {
        router.push('/login');
      }
    }
  }, [router, isAuthenticated, isLoading, checkAuth]);

  if (isLoading) {
    // You can render a global loading spinner here if desired
    return <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>Loading...</div>;
  }

  return <>{children}</>;
};


function MyApp({ Component, pageProps }: AppProps) {
    return (
        <AuthProvider>
            <AppLogic>
                <Component {...pageProps} />
            </AppLogic>
        </AuthProvider>
    );
}

export default MyApp;
