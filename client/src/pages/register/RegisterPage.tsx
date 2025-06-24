import React from 'react';
import Header from '../../components/header/Header';
import RegisterForm from '../../components/loginForm/RegisterForm';
import { Link } from 'react-router-dom';
import './RegisterPage.css';

export default function RegisterPage() {
  return (
    <div className="register-page">
      <Header />
      <main className="register-page-main">
        <RegisterForm />
        <div className="register-page-link-container">
          Already have an account?{' '}
          <Link to="/" className="register-page-link">
            Log in here
          </Link>
        </div>
      </main>
    </div>
  );
}
