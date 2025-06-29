import React, { useEffect, useState } from 'react';
import { Container, Card, Spinner, Alert } from 'react-bootstrap';
import axios from 'axios';
import { useAuth } from '../auth/AuthContext';

interface User {
  username: string;
  email: string;
}

const Dashboard: React.FC = () => {
  const { accessToken } = useAuth();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const res = await axios.get('/accounts/user/', {
          headers: { Authorization: `Bearer ${accessToken}` },
        });
        setUser(res.data);
      } catch (err: any) {
        setError('Errore nel recupero dei dati utente');
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
  }, [accessToken]);

  if (loading) return <Spinner animation="border" />;
  if (error) return <Alert variant="danger">{error}</Alert>;

  return (
    <Container className="mt-4">
      <Card>
        <Card.Header>Benvenuto</Card.Header>
        <Card.Body>
          <p>
            <strong>Username:</strong> {user?.username}
          </p>
          <p>
            <strong>Email:</strong> {user?.email}
          </p>
        </Card.Body>
      </Card>
    </Container>
  );
};

export default Dashboard;
