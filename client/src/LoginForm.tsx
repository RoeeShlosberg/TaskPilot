import React, { useState } from 'react';

export default function LoginForm() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    // TODO: Add real authentication logic here
    setTimeout(() => {
      setLoading(false);
      if (!username || !password) {
        setError('Please enter both username and password.');
      } else {
        alert('Logged in! (stub)');
      }
    }, 800);
  };

  return (
    <form onSubmit={handleSubmit} style={{
      display: 'flex', flexDirection: 'column', gap: 16, minWidth: 280, background: '#f9f9f9', padding: 32, borderRadius: 12, boxShadow: '0 2px 12px #0001', margin: '0 auto'
    }}>
      <label style={{ fontWeight: 500 }}>
        Username
        <input
          type="text"
          value={username}
          onChange={e => setUsername(e.target.value)}
          style={{ width: '100%', padding: 8, marginTop: 4, borderRadius: 6, border: '1px solid #bbb' }}
          autoFocus
        />
      </label>
      <label style={{ fontWeight: 500 }}>
        Password
        <input
          type="password"
          value={password}
          onChange={e => setPassword(e.target.value)}
          style={{ width: '100%', padding: 8, marginTop: 4, borderRadius: 6, border: '1px solid #bbb' }}
        />
      </label>
      {error && <div style={{ color: '#d32f2f', fontSize: 14 }}>{error}</div>}
      <button type="submit" disabled={loading} style={{
        background: '#1976D2', color: '#fff', fontWeight: 600, border: 'none', borderRadius: 6, padding: '10px 0', fontSize: 16, cursor: 'pointer', opacity: loading ? 0.7 : 1
      }}>
        {loading ? 'Logging in...' : 'Log In'}
      </button>
    </form>
  );
}
