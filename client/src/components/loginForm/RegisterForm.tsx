import React, { useEffect, useState } from 'react';
import AuthForm from './AuthForm';
import api from '../../api';
import { useNavigate } from 'react-router-dom';

interface RegisterFormProps {
  onRegister?: (username: string, password: string) => void;
}

export default function RegisterForm({ onRegister }: RegisterFormProps) {
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
      navigate('/main');
    }
  }, [navigate]);

  const handleRegister = async (username: string, password: string) => {
    setError(null);
    setLoading(true);
    try {
      await api.post('/users/register', { username, password });
      if (onRegister) {
        onRegister(username, password);
      } else {
        alert(`Registered as ${username}`);
        // navigate to login or home page
        navigate('/');
      }
    } catch (err: any) {
      if (err.response && err.response.data && err.response.data.detail) {
        setError(err.response.data.detail);
      } else {
        setError('Registration failed. Please try again.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <AuthForm mode="register" buttonText={loading ? 'Registering...' : 'Register'} onSubmit={handleRegister} disabled={loading} />
      {error && <div className="login-form-error" style={{ marginTop: 8 }}>{error}</div>}
    </>
  );
}
