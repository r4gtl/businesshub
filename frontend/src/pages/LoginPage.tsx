import React from 'react';
import { Container, Row, Col, Card } from 'react-bootstrap';
import LoginForm from '../components/auth/LoginForm';

const LoginPage: React.FC = () => {
  return (
    <Container
      fluid
      className="d-flex align-items-center justify-content-center"
      style={{ height: '100vh' }}
    >
      <Row className="w-100 justify-content-center">
        <Col xs={10} sm={8} md={6} lg={4} xl={3}>
          <Card>
            <Card.Header className="text-center">Login</Card.Header>
            <Card.Body>
              <LoginForm />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  );
};

export default LoginPage;
