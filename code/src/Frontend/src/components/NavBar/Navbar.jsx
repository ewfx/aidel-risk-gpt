import React from "react";
import { Link } from "react-router-dom";
import "./NavBar.css";

const NavBar = () => {
  return (
    <header className="header">
      <div className="logo">
        <img src="/Icons/WF-logo.png" alt="RiskGPT Logo" style={{ height: "75px", width: "75px" }} />
      </div>
      <nav className="navbar">
        <ul className="nav-links">
          <li><Link to="/" className="nav-item">Home</Link></li>
          <li><Link to="/risk-analysis" className="nav-item">Risk Analysis</Link></li>
          <li><Link to="/about" className="nav-item">About</Link></li>
        </ul>
      </nav>
    </header>
  );
};

export default NavBar;
