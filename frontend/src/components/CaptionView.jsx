import { useState } from "react";

export default function CaptionView({ image, caption }) {
  const [copied, setCopied] = useState(false);

  const copyCaption = () => {
    navigator.clipboard.writeText(caption);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div
      className="animate-slide-up"
      style={{ display: "flex", flexDirection: "column", gap: "1.5rem" }}
    >
      {/* Image */}
      <img
        src={image}
        alt="Uploaded"
        className="result-image"
        style={{ maxHeight: 380, objectFit: "contain" }}
      />

      {/* Caption card */}
      <div
        className="glass"
        style={{
          borderRadius: "var(--radius-xl)",
          padding: "1.75rem",
          position: "relative",
        }}
      >
        {/* Quote mark */}
        <span
          style={{
            position: "absolute",
            top: "12px",
            left: "20px",
            fontSize: "3.5rem",
            lineHeight: 1,
            color: "var(--purple-500)",
            opacity: 0.35,
            fontFamily: "Georgia, serif",
            userSelect: "none",
          }}
        >
          "
        </span>

        <p
          className="caption-text"
          style={{
            fontSize: "1.15rem",
            fontWeight: 600,
            lineHeight: 1.7,
            color: "var(--text-primary)",
            textAlign: "center",
            padding: "1rem 0.5rem 0",
          }}
        >
          {caption}
        </p>

        {/* Copy button */}
        <div style={{ display: "flex", justifyContent: "center", marginTop: "1.25rem" }}>
          <button
            onClick={copyCaption}
            className="glass glass-hover"
            style={{
              padding: "7px 20px",
              borderRadius: "9999px",
              fontSize: "0.8rem",
              fontWeight: 500,
              color: copied ? "var(--teal-400)" : "var(--text-secondary)",
              cursor: "pointer",
              display: "flex",
              alignItems: "center",
              gap: "6px",
              transition: "color 0.2s ease",
            }}
          >
            {copied ? "✓ Copied!" : "⎘ Copy Caption"}
          </button>
        </div>
      </div>
    </div>
  );
}