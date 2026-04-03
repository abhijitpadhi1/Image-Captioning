import { useState } from "react";
import CaptionView from "./CaptionView";
import AttentionView from "./AttentionView";

export default function Tabs({ image, caption, attention, onReset }) {
  const [tab, setTab] = useState("caption");

  return (
    <div
      className="animate-fade-in"
      style={{
        minHeight: "100vh",
        background:
          "radial-gradient(ellipse 100% 60% at 50% 0%, rgba(59,130,246,0.1) 0%, transparent 55%), var(--bg-base)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        padding: "2.5rem 1.5rem",
      }}
    >
      {/* Tab bar */}
      <div className="tab-bar animate-slide-up" style={{ marginBottom: "2rem" }}>
        <button
          className={`tab-pill ${tab === "caption" ? "active" : ""}`}
          onClick={() => setTab("caption")}
        >
          📝 Caption
        </button>
        <button
          className={`tab-pill ${tab === "attention" ? "active" : ""}`}
          onClick={() => setTab("attention")}
        >
          🔍 Attention
        </button>
      </div>

      {/* Content */}
      <div
        className="tab-content"
        key={tab}
        style={{ width: "100%", maxWidth: 680 }}
      >
        {tab === "caption" && (
          <CaptionView image={image} caption={caption} />
        )}
        {tab === "attention" && (
          <AttentionView image={image} attention={attention} caption={caption} />
        )}
      </div>

      {/* Reset */}
      <button
        onClick={onReset}
        className="glass glass-hover animate-slide-up-4"
        style={{
          marginTop: "2.5rem",
          padding: "12px 36px",
          borderRadius: "9999px",
          color: "var(--text-secondary)",
          fontWeight: 600,
          fontSize: "0.9rem",
          cursor: "pointer",
        }}
      >
        ← Try Another Image
      </button>
    </div>
  );
}