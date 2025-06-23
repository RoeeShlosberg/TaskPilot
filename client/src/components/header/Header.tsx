import React from 'react';
import './Header.css';
import { useNavigate } from 'react-router-dom';
import LogoTitle from './LogoTitle';

export default function Header() {
  const navigate = useNavigate();
  const token = localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    navigate('/');
  };
  return (
    <header className="header">
      <button className="header-logout-btn" onClick={handleLogout}>
        Log out
      </button>
      <LogoTitle />
      <div></div>
    </header>
  );
}
