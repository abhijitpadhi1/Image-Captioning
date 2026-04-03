export default function AttentionView({ image, attention, caption }) {
  if (!attention) return null;

  // Split caption into tokens matching attention map frames
  const tokens = caption ? caption.trim().split(/\s+/) : [];

  return (
    <div
      className="animate-slide-up"
      style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
    >
      {/* Header explanation */}
      <div
        className="glass"
        style={{
          borderRadius: "var(--radius-xl)",
          padding: "1rem 1.25rem",
          fontSize: "0.85rem",
          color: "var(--text-secondary)",
          lineHeight: 1.6,
          textAlign: "center",
        }}
      >
        Each frame shows which part of the image the model was attending to when
        generating each word.
      </div>

      {/* Attention grid */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))",
          gap: "1rem",
        }}
      >
        {attention.map((alpha, i) => {
          const grid = alpha.flat();
          const word = tokens[i] || `#${i + 1}`;
          const cols = Math.round(Math.sqrt(grid.length)) || 7;

          return (
            <div key={i} className="animate-slide-up attention-frame glass" style={{ animationDelay: `${i * 0.04}s` }}>
              {/* Word label */}
              <div
                style={{
                  padding: "6px 12px",
                  display: "flex",
                  alignItems: "center",
                  gap: "6px",
                  borderBottom: "1px solid var(--border)",
                }}
              >
                <span
                  style={{
                    fontSize: "0.7rem",
                    color: "var(--text-muted)",
                    textTransform: "uppercase",
                    letterSpacing: "0.06em",
                    fontWeight: 600,
                  }}
                >
                  #{i + 1}
                </span>
                <span
                  style={{
                    fontSize: "0.85rem",
                    fontWeight: 700,
                    color: "var(--purple-400)",
                  }}
                >
                  {word}
                </span>
              </div>

              {/* Image + heatmap */}
              <div style={{ position: "relative" }}>
                <img
                  src={image}
                  alt={`attention-${i}`}
                  style={{ width: "100%", display: "block" }}
                />

                {/* Heatmap overlay — HSL warm-to-cool mapping */}
                <div
                  style={{
                    position: "absolute",
                    top: 0,
                    left: 0,
                    width: "100%",
                    height: "100%",
                    opacity: 0.55,
                    display: "grid",
                    gridTemplateColumns: `repeat(${cols}, 1fr)`,
                  }}
                >
                  {grid.map((v, idx) => {
                    // Map 0→1 to hue 240 (blue/cool) → 0 (red/warm)
                    const hue = Math.round((1 - v) * 240);
                    const sat = 80;
                    const lit = 50;
                    return (
                      <div
                        key={idx}
                        style={{
                          backgroundColor: `hsla(${hue}, ${sat}%, ${lit}%, ${v})`,
                        }}
                      />
                    );
                  })}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}