import { useState, useRef } from "react";
import { predict, visualize } from "../api";
import Tabs from "./Tabs";
import Loading from "./Loading";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [imageURL, setImageURL] = useState(null);
  const [caption, setCaption] = useState("");
  const [attention, setAttention] = useState(null);
  const [loaded, setLoaded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [dragging, setDragging] = useState(false);
  const inputRef = useRef(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    const url = URL.createObjectURL(file);
    setImageURL(url);

    try {
      const [pred, vis] = await Promise.all([predict(file), visualize(file)]);
      setCaption(pred.caption);
      setAttention(vis.attention_maps);
      setLoaded(true);
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setFile(null);
    setImageURL(null);
    setCaption("");
    setAttention(null);
    setLoaded(false);
    setLoading(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);
    const dropped = e.dataTransfer.files[0];
    if (dropped) setFile(dropped);
  };

  // ── Loaded view ─────────────────────────────────────────────
  if (loaded) return <Tabs image={imageURL} caption={caption} attention={attention} onReset={reset} />;

  // ── Loading view ─────────────────────────────────────────────
  if (loading) return (
    <div style={{ minHeight: "100vh", background: "var(--bg-base)", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <Loading />
    </div>
  );

  // ── Upload view ──────────────────────────────────────────────
  return (
    <div
      className="animate-fade-in"
      style={{
        minHeight: "100vh",
        background:
          "radial-gradient(ellipse 100% 60% at 50% 0%, rgba(139,92,246,0.14) 0%, transparent 55%), var(--bg-base)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
      }}
    >
      {/* Header */}
      <h2
        className="gradient-text animate-slide-up"
        style={{
          fontSize: "2.2rem",
          fontWeight: 800,
          marginBottom: "0.5rem",
          textAlign: "center",
          letterSpacing: "-0.02em",
        }}
      >
        Upload an Image
      </h2>
      <p
        className="animate-slide-up-1"
        style={{
          color: "var(--text-secondary)",
          marginBottom: "2rem",
          fontSize: "0.95rem",
          textAlign: "center",
        }}
      >
        Supports JPG, PNG, WEBP · Max 10 MB
      </p>

      {/* Drop zone card */}
      <div
        className={`glass drop-zone animate-slide-up-2 ${dragging ? "dragging" : ""}`}
        style={{
          width: "100%",
          maxWidth: 520,
          padding: "3rem 2rem",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: "1.25rem",
          minHeight: 260,
        }}
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
        onDragLeave={() => setDragging(false)}
        onDrop={handleDrop}
      >
        <input
          ref={inputRef}
          type="file"
          accept="image/*"
          style={{ display: "none" }}
          onChange={(e) => setFile(e.target.files[0])}
        />

        {file ? (
          /* Preview */
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "1rem" }}>
            <img
              src={URL.createObjectURL(file)}
              alt="Preview"
              style={{
                width: 180,
                height: 180,
                objectFit: "cover",
                borderRadius: "1rem",
                border: "1px solid var(--border-glow)",
                boxShadow: "0 0 30px rgba(139,92,246,0.3)",
              }}
            />
            <p style={{ color: "var(--text-secondary)", fontSize: "0.85rem" }}>
              {file.name}
            </p>
            <button
              onClick={(e) => { e.stopPropagation(); setFile(null); }}
              style={{
                background: "rgba(255,255,255,0.06)",
                border: "1px solid var(--border)",
                borderRadius: "9999px",
                color: "var(--text-secondary)",
                padding: "4px 14px",
                fontSize: "0.78rem",
                cursor: "pointer",
              }}
            >
              Remove
            </button>
          </div>
        ) : (
          /* Empty state */
          <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: "0.75rem" }}>
            <div
              style={{
                width: 72,
                height: 72,
                borderRadius: "1.25rem",
                background: "linear-gradient(135deg, rgba(139,92,246,0.2), rgba(59,130,246,0.2))",
                border: "1px solid rgba(139,92,246,0.3)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontSize: "1.8rem",
              }}
            >
              🖼️
            </div>
            <p style={{ color: "var(--text-primary)", fontWeight: 600, fontSize: "1rem" }}>
              Drop your image here
            </p>
            <p style={{ color: "var(--text-muted)", fontSize: "0.85rem" }}>
              or click to browse files
            </p>
          </div>
        )}
      </div>

      {/* Analyze button */}
      <button
        onClick={handleUpload}
        disabled={!file}
        className="gradient-btn animate-slide-up-3"
        style={{
          marginTop: "1.75rem",
          padding: "15px 48px",
          borderRadius: "9999px",
          color: "#fff",
          fontWeight: 700,
          fontSize: "1rem",
          border: "none",
          cursor: file ? "pointer" : "not-allowed",
          opacity: file ? 1 : 0.4,
          letterSpacing: "0.01em",
        }}
      >
        <span>Analyze Image ✦</span>
      </button>
    </div>
  );
}