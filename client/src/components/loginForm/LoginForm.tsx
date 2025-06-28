import React, { useEffect } from 'react';
import AuthForm from './AuthForm';
import './LoginForm.css';
import { useNavigate } from 'react-router-dom';
import api from '../../api';

export default function LoginForm() {
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      navigate('/main');
    }
  }, [navigate]);

  const handleLogin = async (username: string, password: string) => {
    try {
      // FastAPI expects application/x-www-form-urlencoded for OAuth2PasswordRequestForm
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);
      const response = await api.post('/users/login', params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });
      // Save token to localStorage
      localStorage.setItem('access_token', response.data.access_token);
      navigate('/main');
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        alert(err.response.data.detail);
      } else {
        alert('Login failed. Please try again.');
      }
    }
  };

  return <AuthForm mode="login" buttonText="Log In" onSubmit={handleLogin} />;
}
