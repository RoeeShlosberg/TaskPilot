import React from 'react';
import './Header.css';
import { useNavigate, useLocation } from 'react-router-dom';
import LogoTitle from './LogoTitle';

export default function Header() {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem('access_token');
  
  // Check if we're on login or register page
  const isAuthPage = location.pathname === '/' || location.pathname === '/register';

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };
  
  return (
    <header className="header">
      {token && !isAuthPage && (
        <button className="header-logout-btn" onClick={handleLogout}>
          Log out
        </button>
      )}
      <LogoTitle />
      <div></div>
    </header>
  );
}
