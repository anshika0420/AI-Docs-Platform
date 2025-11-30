import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isRegister, setIsRegister] = useState(false);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      const endpoint = isRegister ? "/auth/register" : "/auth/login";
      const res = await api.post(endpoint, { email, password });
      localStorage.setItem("token", res.data.access_token);
      navigate("/projects");
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = () => {
    setIsRegister(true);
  };

  return (
    <div className="page page-centered">
      <div className="auth-wrapper">
        <div className="auth-card">
          <h2 className="page-title" style={{ marginBottom: 8 }}>
            {isRegister ? "Register" : "Login"}
          </h2>
          <p className="page-subtitle" style={{ marginBottom: 20 }}>
            {isRegister
              ? "Create your account to begin generating documents."
              : "Sign in to continue creating AI-generated docs."}
          </p>

          {error && <p className="text-danger" style={{ marginBottom: 10 }}>{error}</p>}

          <form className="form" onSubmit={handleSubmit}>
            <div className="form-field">
              <label className="label">Email</label>
              <input
                className="input"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                required
              />
            </div>

            <div className="form-field">
              <label className="label">Password</label>
              <input
                className="input"
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                required
              />
            </div>

            <div style={{ display: "flex", gap: 10, marginTop: 6 }}>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? "Processing…" : isRegister ? "Register" : "Login"}
              </button>

              {!isRegister && (
                <button
                  type="button"
                  className="btn btn-ghost"
                  onClick={handleRegister}
                >
                  New user? Register
                </button>
              )}
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
