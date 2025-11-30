import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { api } from "../api";

export default function Editor() {
  const { id } = useParams();
  const [project, setProject] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(true);
  const [refineText, setRefineText] = useState({});
  const [commentText, setCommentText] = useState({});
  const [exportLoading, setExportLoading] = useState(false);

  const loadProject = async () => {
    setLoading(true);
    try {
      const res = await api.get(`/projects/${id}`);
      setProject(res.data);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to load project");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProject();
  }, [id]);

  const refineSection = async (sectionId) => {
    const instruction = refineText[sectionId];
    if (!instruction) return;
    try {
      await api.post(`/projects/${id}/sections/${sectionId}/refine`, { instruction });
      await loadProject();
    } catch {
      alert("Refinement failed");
    }
  };

  const sendFeedback = async (sectionId, action) => {
    try {
      await api.post(`/projects/${id}/sections/${sectionId}/feedback`, {
        action,
        comment: commentText[sectionId] || null,
      });
      setCommentText((p) => ({ ...p, [sectionId]: "" }));
      await loadProject();
    } catch {
      alert("Feedback failed");
    }
  };

  const handleExport = async (fmt) => {
    setExportLoading(true);
    try {
      const res = await api.get(`/export/${id}`, {
        params: { format: fmt },
        responseType: "blob",
      });
      const blob = new Blob([res.data]);
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = fmt === "pptx" ? `project_${id}.pptx` : `project_${id}.docx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch {
      alert("Export failed");
    } finally {
      setExportLoading(false);
    }
  };

  if (loading) return <p className="muted page-centered">Loading document…</p>;
  if (error) return <p className="text-danger page-centered">{error}</p>;

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h2 className="page-title">
            {project.title} <span className="muted">({project.doc_type})</span>
          </h2>
          {project.topic && (
            <p className="page-subtitle"><strong>Topic:</strong> {project.topic}</p>
          )}
        </div>
        <div style={{ display: "flex", gap: 10 }}>
          <button className="btn btn-primary" onClick={() => handleExport("docx")} disabled={exportLoading}>Export DOCX</button>
          <button className="btn btn-primary" onClick={() => handleExport("pptx")} disabled={exportLoading}>Export PPTX</button>
        </div>
      </div>

      <div className="editor-layout">
        {/* LEFT SIDEBAR */}
        <aside className="editor-sidebar">
          {project.sections.map((s, i) => (
            <button
              key={s.id}
              className="sidebar-item"
              onClick={() =>
                document.getElementById(`section-${s.id}`)?.scrollIntoView({ behavior: "smooth" })
              }
            >
              {i + 1}. {s.title}
            </button>
          ))}
        </aside>

        {/* MAIN DOCUMENT */}
        <main className="editor-document">
          {project.sections.map((s, i) => (
            <div key={s.id} id={`section-${s.id}`} className="editor-section">
              <h3 className="editor-section-title">{i + 1}. {s.title}</h3>
              <pre className="editor-content">{s.content}</pre>

              {/* Feedback + refine UI */}
              <div className="interaction-panel">
                <p className="stat-line">
                  👍 {s.likes} &nbsp; | &nbsp; 👎 {s.dislikes}
                </p>

                <textarea
                  className="interaction-input"
                  placeholder="Suggest a refinement (e.g. formal tone / bullet points / shorten to 100 words)"
                  value={refineText[s.id] || ""}
                  onChange={(e) => setRefineText((p) => ({ ...p, [s.id]: e.target.value }))}
                />
                <button className="btn btn-primary btn-sm" onClick={() => refineSection(s.id)}>
                  Refine with AI
                </button>

                <input
                  className="interaction-input"
                  placeholder="Leave a comment"
                  value={commentText[s.id] || ""}
                  onChange={(e) => setCommentText((p) => ({ ...p, [s.id]: e.target.value }))}
                />
                <div>
                  <button className="btn btn-like" onClick={() => sendFeedback(s.id, "like")}>👍 Like</button>
                  <button className="btn btn-dislike" onClick={() => sendFeedback(s.id, "dislike")}>👎 Dislike</button>
                </div>
              </div>
            </div>
          ))}
        </main>
      </div>
    </div>
  );
}
