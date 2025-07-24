import { Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';

interface PrivateRouteProps {
  children: JSX.Element;
}

const PrivateRoute = ({ children }: PrivateRouteProps) => {
  //const accessToken = localStorage.getItem('access_token');
  const { accessToken } = useAuth();
  return accessToken ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
