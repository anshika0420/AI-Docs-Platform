import React from "react";
import { useNavigate, Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const location = useLocation();
  const token = localStorage.getItem("token");

  const handleLogout = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  const onLogoClick = () => {
    if (token) navigate("/projects");
    else navigate("/login");
  };

  const isLoginPage = location.pathname === "/login";

  return (
    <header className="top-nav">
      <div className="top-nav-inner">
        <button className="brand" onClick={onLogoClick} style={{ border: "none", background: "transparent", padding: 0 }}>
          <div className="brand-logo" />
          <span className="brand-title">AI Docs Platform</span>
        </button>

        <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
          <span className="badge-pill">Gemini-powered</span>

          {token ? (
            <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
              Logout
            </button>
          ) : !isLoginPage ? (
            <Link to="/login" className="btn btn-secondary btn-sm" style={{ textDecoration: "none" }}>
              Login
            </Link>
          ) : null}
        </div>
      </div>
    </header>
  );
}
