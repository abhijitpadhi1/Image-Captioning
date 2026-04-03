export default function Landing({ onStart }) {
  return (
    <div
      style={{
        minHeight: "100vh",
        background:
          "radial-gradient(ellipse 120% 80% at 50% -10%, rgba(139,92,246,0.28) 0%, transparent 60%), radial-gradient(ellipse 80% 60% at 80% 80%, rgba(59,130,246,0.2) 0%, transparent 55%), var(--bg-base)",
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "2rem",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Decorative orbs */}
      <div
        className="orb"
        style={{
          width: 500,
          height: 500,
          background: "rgba(139,92,246,0.12)",
          top: "-150px",
          left: "-120px",
          animationDuration: "10s",
        }}
      />
      <div
        className="orb"
        style={{
          width: 400,
          height: 400,
          background: "rgba(59,130,246,0.1)",
          bottom: "-100px",
          right: "-100px",
          animationDuration: "13s",
          animationDelay: "2s",
        }}
      />

      {/* Badge */}
      <div
        className="glass animate-slide-up"
        style={{
          borderRadius: "9999px",
          padding: "6px 18px",
          marginBottom: "1.5rem",
          fontSize: "0.78rem",
          fontWeight: 600,
          letterSpacing: "0.08em",
          textTransform: "uppercase",
          color: "var(--purple-400)",
          border: "1px solid rgba(139,92,246,0.3)",
        }}
      >
        ✦ Powered by Deep Learning
      </div>

      {/* Title */}
      <h1
        className="gradient-text animate-slide-up-1"
        style={{
          fontSize: "clamp(2.8rem, 7vw, 5rem)",
          fontWeight: 900,
          lineHeight: 1.08,
          textAlign: "center",
          marginBottom: "1.25rem",
          letterSpacing: "-0.02em",
        }}
      >
        Image Captioning
        <br />
        <span style={{ color: "var(--text-primary)", WebkitTextFillColor: "var(--text-primary)" }}>
          with AI
        </span>
      </h1>

      {/* Subtitle */}
      <p
        className="animate-slide-up-2"
        style={{
          color: "var(--text-secondary)",
          fontSize: "1.125rem",
          textAlign: "center",
          maxWidth: 480,
          lineHeight: 1.7,
          marginBottom: "2.5rem",
        }}
      >
        Upload any image and watch the AI generate a natural-language description
        — complete with visual attention maps.
      </p>

      {/* Feature chips */}
      <div
        className="animate-slide-up-2"
        style={{
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "0.6rem",
          marginBottom: "2.75rem",
        }}
      >
        {["🎯 Attention Heatmaps", "🧠 LSTM Decoder", "⚡ Instant Results"].map(
          (f) => (
            <span
              key={f}
              className="glass"
              style={{
                padding: "6px 16px",
                borderRadius: "9999px",
                fontSize: "0.82rem",
                fontWeight: 500,
                color: "var(--text-secondary)",
              }}
            >
              {f}
            </span>
          )
        )}
      </div>

      {/* CTA */}
      <button
        onClick={onStart}
        className="gradient-btn animate-slide-up-3"
        style={{
          padding: "16px 44px",
          borderRadius: "9999px",
          color: "#fff",
          fontWeight: 700,
          fontSize: "1.05rem",
          border: "none",
          cursor: "pointer",
          letterSpacing: "0.01em",
        }}
      >
        <span>Get Started →</span>
      </button>

      {/* Bottom hint */}
      <p
        className="animate-slide-up-4"
        style={{
          marginTop: "2rem",
          color: "var(--text-muted)",
          fontSize: "0.8rem",
        }}
      >
        No account needed · Free to use
      </p>
    </div>
  );
}