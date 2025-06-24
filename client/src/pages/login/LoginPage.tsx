import React from 'react';
import Header from '../../components/header/Header';
import LoginForm from '../../components/loginForm/LoginForm';
import { Link } from 'react-router-dom';
import './LoginPage.css';

export default function LoginPage() {
  return (
    <div className="login-page">
      <Header />
      <main className="login-page-main">
        <LoginForm />
        <div className="login-page-link-container">
          Not registered?{' '}
          <Link to="/register" className="login-page-link">
            Register here
          </Link>
        </div>
      </main>
    </div>
  );
}
