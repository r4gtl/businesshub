import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import Dashboard from './pages/Dashboard';
import PrivateRoute from './components/auth/PrivateRoute';
import AppNavBar from './components/layout/NavBar';
import Layout from './components/layout/Layout';
import 'react-toastify/dist/ReactToastify.css';
import { ToastContainer } from 'react-toastify';

function App() {
  const location = useLocation();
  const isLoggedIn = !!localStorage.getItem('access_token');
  const hideNavbar = location.pathname === '/login';

  return (
    <>
      {!hideNavbar && isLoggedIn && <AppNavBar />}
      <Routes>
        <Route path="/login" element={<LoginPage />} />

        <Route
          path="/dashboard"
          element={
            <PrivateRoute>
              <Layout>
                <Dashboard />
              </Layout>
            </PrivateRoute>
          }
        />

        {/* Route di default */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />
      </Routes>

      <ToastContainer position="top-right" autoClose={3000} />
    </>
  );
}

export default App;
