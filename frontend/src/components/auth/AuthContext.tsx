import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

interface User {
  id: number;
  username: string;
  email: string;
}

interface AuthContextType {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null;
  setTokens: (access: string, refresh: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [accessToken, setAccessToken] = useState<string | null>(
    localStorage.getItem('accessToken')
  );
  const [refreshToken, setRefreshToken] = useState<string | null>(
    localStorage.getItem('refreshToken')
  );
  const [user, setUser] = useState<User | null>(null);

  const fetchUser = async (token: string) => {
    try {
      const response = await axios.get(
        `${import.meta.env.VITE_API_BASE_URL}/accounts/me/`,
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setUser(response.data);
    } catch (error) {
      console.error('Errore nel recupero utente:', error);
      logout(); // opzionale: logout automatico se il token non è valido
    }
  };

  const setTokens = (access: string, refresh: string) => {
    localStorage.setItem('accessToken', access);
    localStorage.setItem('refreshToken', refresh);
    setAccessToken(access);
    setRefreshToken(refresh);
    fetchUser(access);
  };

  const logout = () => {
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    window.location.href = '/login'; // oppure usa navigate se vuoi gestirlo via router
  };

  useEffect(() => {
    if (accessToken) {
      fetchUser(accessToken);
    }
  }, [accessToken]);

  return (
    <AuthContext.Provider
      value={{ accessToken, refreshToken, user, setTokens, logout }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth deve essere usato dentro AuthProvider');
  return ctx;
};
