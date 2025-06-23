import React, { useState } from 'react';
import './LoginForm.css';

interface AuthFormProps {
  mode: 'login' | 'register';
  buttonText: string;
  onSubmit: (username: string, password: string) => void;
  disabled?: boolean;
}

export default function AuthForm({ mode, buttonText, onSubmit, disabled }: AuthFormProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setTimeout(() => {
      setLoading(false);
      if (!username || !password) {
        setError('Please enter both username and password.');
      } else {
        onSubmit(username, password);
      }
    }, 800);
  };

  return (
    <form className="login-form" onSubmit={handleSubmit}>
      <label>
        Username
        <input
          type="text"
          value={username}
          onChange={e => setUsername(e.target.value)}
          autoFocus={mode === 'login'}
          disabled={disabled}
        />
      </label>
      <label>
        Password
        <input
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          disabled={disabled}
        />
      </label>
      {error && <div className="login-form-error">{error}</div>}
      <button type="submit" disabled={loading || disabled}>
        {loading ? (mode === 'login' ? 'Logging in...' : 'Registering...') : buttonText}
      </button>
    </form>
  );
}
