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
    localStorage.getItem('access_token')
  );
  const [refreshToken, setRefreshToken] = useState<string | null>(
    localStorage.getItem('refresh_token')
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
      setUser(null);
    }
  };

  const setTokens = (access: string, refresh: string) => {
    setAccessToken(access);
    setRefreshToken(refresh);
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
    fetchUser(access); // fetch utente al login
  };

  const logout = () => {
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
  };

  // Effettua il fetch dell'utente all'avvio, se c'è un token
  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      fetchUser(token);
    }
  }, []);

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
