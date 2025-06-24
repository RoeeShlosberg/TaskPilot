import React from 'react';
import './LogoTitle.css';
// Import logo from the assets directory we just created
import logo from '../../assets/logo.svg';

const LogoTitle: React.FC = () => {
  return (
    <div className="logo-title">
      <img className="logo-title-logo" src={logo} alt="TaskPilot Logo" />
      <span className="logo-title-text">TaskPilot</span>
    </div>
  );
};

export default LogoTitle;
