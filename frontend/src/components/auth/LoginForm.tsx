import { useState } from 'react';
import { Form, Button, Alert, Card } from 'react-bootstrap';
import axios from '@api/axios';
import { useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

const LoginForm = () => {
  const { setTokens } = useAuth();
  const navigate = useNavigate();

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg('');

    try {
      const response = await axios.post('/token/', {
        username,
        password,
      });

      const { access, refresh } = response.data;

      // Salva i token nel contesto
      setTokens(access, refresh);

      // Reindirizza alla dashboard
      navigate('/dashboard');
    } catch (error) {
      console.error(error);
      setErrorMsg('Credenziali non valide');
    }
  };

  return (
    <Card style={{ maxWidth: '400px', margin: '0 auto' }}>
      <Card.Body>
        <h4 className="mb-4 text-center">Login</h4>
        <Form onSubmit={handleSubmit}>
          <Form.Group className="mb-3" controlId="formUsername">
            <Form.Label>Username</Form.Label>
            <Form.Control
              type="text"
              placeholder="Inserisci username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoFocus
              required
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="formPassword">
            <Form.Label>Password</Form.Label>
            <Form.Control
              type="password"
              placeholder="Inserisci password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </Form.Group>

          {errorMsg && <Alert variant="danger">{errorMsg}</Alert>}

          <div className="d-grid">
            <Button variant="primary" type="submit">
              Accedi
            </Button>
          </div>
        </Form>
      </Card.Body>
    </Card>
  );
};

export default LoginForm;
