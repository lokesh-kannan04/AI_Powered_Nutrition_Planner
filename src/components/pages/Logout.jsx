import { useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Logout = () => {
  const navigate = useNavigate();

  useEffect(() => {
    const sessionKey = localStorage.getItem('session_key');

    const logout = async () => {
      try {
        await axios.post('http://localhost:8000/api/logout/', {
          session_key: sessionKey,
        });

        // Remove session key from localStorage
        localStorage.removeItem('session_key');

        // Redirect to login page
        navigate('/login');
      } catch (error) {
        console.error('Logout failed:', error);

        // Remove session key anyway and redirect
        localStorage.removeItem('session_key');
        navigate('/login');
      }
    };

    logout();
  }, [navigate]);

  return null;
};

export default Logout;
