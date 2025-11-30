import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../api";

export default function ConfigureProject() {
  const [title, setTitle] = useState("");
  const [topic, setTopic] = useState("");
  const [docType, setDocType] = useState("docx");
  const [sections, setSections] = useState([{ title: "", order: 0 }]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const updateSection = (index, field, value) => {
    setSections((prev) =>
      prev.map((s, i) => (i === index ? { ...s, [field]: value } : s))
    );
  };

  const addSection = () => {
    setSections((prev) => [...prev, { title: "", order: prev.length }]);
  };

  const removeSection = (index) => {
    setSections((prev) =>
      prev
        .filter((_, i) => i !== index)
        .map((s, i) => ({ ...s, order: i }))
    );
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const outline = sections.map((s, i) => ({
        title: s.title || `Section ${i + 1}`,
        order: i,
      }));

      const res = await api.post("/projects", {
        title,
        topic,
        doc_type: docType,
        outline,
      });

      const projectId = res.data.id;
      await api.post(`/projects/${projectId}/generate`);
      navigate(`/projects/${projectId}/edit`);
    } catch (err) {
      console.error(err);
      setError(err.response?.data?.detail || "Failed to create project");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page page-centered">
      <div className="page-card wide">
        <h1 className="title-xl">Create New Document</h1>
        <p className="subtitle">
          Describe your topic and let the AI generate a polished document.
        </p>

        {error && <p className="text-danger" style={{ marginBottom: 16 }}>{error}</p>}

        <form className="modern-form" onSubmit={handleCreate}>
          <div className="form-row">
            <label>Document Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="e.g. Psychological Impact of Social Media"
              required
            />
          </div>

          <div className="form-row">
            <label>Main Topic / Prompt</label>
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              placeholder="e.g. Effects of social media on mental health in teenagers"
              required
            />
          </div>

          <div className="form-row small">
            <label>Document Type</label>
            <select value={docType} onChange={(e) => setDocType(e.target.value)}>
              <option value="docx">Word (.docx)</option>
              <option value="pptx">PowerPoint (.pptx)</option>
            </select>
          </div>

          <div className="section-block">
            <label>{docType === "docx" ? "Sections" : "Slides"}</label>

            {sections.map((s, idx) => (
              <div key={idx} className="section-line">
                <input
                  value={s.title}
                  onChange={(e) => updateSection(idx, "title", e.target.value)}
                  placeholder={
                    docType === "docx"
                      ? `Section ${idx + 1} title`
                      : `Slide ${idx + 1} title`
                  }
                  required
                />

                {sections.length > 1 && (
                  <button
                    type="button"
                    className="remove-btn"
                    onClick={() => removeSection(idx)}
                  >
                    ✕
                  </button>
                )}
              </div>
            ))}

            <button
              type="button"
              className="btn-light"
              onClick={addSection}
              style={{ marginTop: 8 }}
            >
              + Add {docType === "docx" ? "Section" : "Slide"}
            </button>
          </div>

          <button
            type="submit"
            className="btn-primary-xl"
            disabled={loading}
            style={{ marginTop: 20 }}
          >
            {loading ? "Generating..." : "Create & Generate with AI"}
          </button>
        </form>
      </div>
    </div>
  );
}
