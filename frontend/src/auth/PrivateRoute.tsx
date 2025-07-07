import { Navigate } from 'react-router-dom';

interface PrivateRouteProps {
  children: JSX.Element;
}

const PrivateRoute = ({ children }: PrivateRouteProps) => {
  const accessToken = localStorage.getItem('accessToken');
  return accessToken ? children : <Navigate to="/login" />;
};

export default PrivateRoute;
