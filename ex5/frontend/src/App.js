import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Products from "./components/Products";
import Payments from "./components/Payments";
import "./App.css";

function App() {
  return (
    <Router>
      <div className="container">
        <h1>Sklep Internetowy</h1>
        <nav>
          <Link to="/">Produkty</Link>
          <Link to="/payments">Płatności</Link>
        </nav>
        <Routes>
          <Route path="/" element={<Products />} />
          <Route path="/payments" element={<Payments />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
