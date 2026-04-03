export default function Loading() {
  const steps = [
    { label: "Uploading image", done: true },
    { label: "Running model inference", done: false },
    { label: "Generating attention maps", done: false },
  ];

  return (
    <div
      className="animate-fade-in"
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        minHeight: "60vh",
        gap: "2rem",
      }}
    >
      {/* Dual ring spinner */}
      <div style={{ position: "relative", width: 64, height: 64 }}>
        <div
          className="spinner-ring"
          style={{ position: "absolute", inset: 0 }}
        />
        <div
          className="spinner-ring-sm"
          style={{
            position: "absolute",
            inset: "10px",
          }}
        />
      </div>

      {/* Label */}
      <p
        style={{
          fontSize: "1.1rem",
          fontWeight: 600,
          color: "var(--text-primary)",
        }}
      >
        Analyzing your image…
      </p>

      {/* Step indicators */}
      <div
        style={{
          display: "flex",
          flexDirection: "column",
          gap: "0.6rem",
          alignItems: "flex-start",
        }}
      >
        {steps.map((s, i) => (
          <div
            key={i}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "0.6rem",
              color: s.done ? "var(--teal-400)" : "var(--text-muted)",
              fontSize: "0.85rem",
              fontWeight: 500,
              transition: "color 0.3s ease",
            }}
          >
            <span
              style={{
                width: 18,
                height: 18,
                borderRadius: "50%",
                display: "inline-flex",
                alignItems: "center",
                justifyContent: "center",
                background: s.done
                  ? "var(--teal-400)"
                  : "rgba(255,255,255,0.08)",
                fontSize: "0.65rem",
                color: "#fff",
                flexShrink: 0,
              }}
            >
              {s.done ? "✓" : i + 1}
            </span>
            {s.label}
          </div>
        ))}
      </div>
    </div>
  );
}