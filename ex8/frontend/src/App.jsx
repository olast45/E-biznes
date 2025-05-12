import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginForm from './components/LoginForm';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LoginForm />} />
        <Route path="/logged-user" element={<h2>🎉 Login successful! Welcome back.</h2>} />
      </Routes>
    </Router>
  );
}

export default App;
