import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import './Login.css'; // Import the CSS file for styling
import Footer from './Footer';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        email,
        password
      });

      if (response.status === 200) {
        alert(response.data.message);
        localStorage.setItem('session_key', response.data.session_key);
        if (response.data.form_submitted) {
          navigate('/show_report'); // Navigate to /report if form is submitted
        } else {
          navigate('/form'); // Navigate to /form if form is not submitted
        }
      }
    } catch (error) {
      alert(error.response?.data?.error || 'Login Failed');
    }
  };

  return (
    <>
      <div className="login-container">
        <div className="login-box">
          <h2>Login</h2>
          <form onSubmit={handleLogin} className="login-form">
            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                placeholder="Enter your email address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Password</label>
              <input
                type="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
            <button type="submit" className="login-button">Login</button>
          </form>
          <p className="signup-link">
            Doesn't have an account yet? <a href="/sign-up">Sign Up</a>
          </p>
        </div>
        {/* <div className='login-image'>
          <img src='/images/robo-ai.png'></img>
        </div> */}
      </div>
      <div className='footer'>
        <Footer />
      </div>
    </>
  );
};

export default Login;