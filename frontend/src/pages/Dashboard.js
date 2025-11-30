import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

export default function Dashboard() {
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const loadProjects = async () => {
    setLoading(true);
    setError("");
    try {
      const res = await api.get("/projects");
      setProjects(res.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to load projects");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure you want to delete this project?")) return;
    try {
      await api.delete(`/projects/${id}`);
      setProjects((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete project");
    }
  };

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2 className="page-title">Your Projects</h2>
          <p className="page-subtitle">
            Continue where you left off or spin up a fresh AI-generated document.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate("/projects/new")}>
          + New Project
        </button>
      </div>

      <div className="surface surface-tight">
        {loading && <p className="muted">Loading your projects…</p>}
        {error && <p className="text-danger" style={{ marginBottom: 12 }}>{error}</p>}

        {!loading && projects.length === 0 && (
          <p className="muted">
            No projects yet — click <strong>+ New Project</strong> to create your first doc.
          </p>
        )}

        <div className="project-list">
          {projects.map((p) => (
            <div className="project-card" key={p.id}>
              <div className="project-meta">
                <span className="project-title">{p.title}</span>
                <span className="project-type-pill">{p.doc_type}</span>
              </div>

              <div className="project-actions">
                <button
                  className="btn btn-ghost btn-sm"
                  onClick={() => navigate(`/projects/${p.id}/edit`)}
                >
                  Open
                </button>

                <button
                  className="btn-delete"
                  onClick={() => handleDelete(p.id)}
                  title="Delete project"
                >
                  ✕
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
