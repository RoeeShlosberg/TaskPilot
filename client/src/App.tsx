import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Header from './components/header/Header';
import LoginPage from './pages/login/LoginPage';
import RegisterPage from './pages/register/RegisterPage';
import MainPage from './pages/MainPage';

function App() {
  return (
    <BrowserRouter>
      <div style={{ minHeight: '100vh', background: '#f0f4fa' }}>
        <main style={{ display: 'flex', justifyContent: 'center', alignItems: 'flex-start', minHeight: '60vh' }}>
          <Routes>
            <Route path="/" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            <Route path="/main" element={<MainPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
