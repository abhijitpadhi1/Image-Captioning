export default function AttentionView({ image, attention }) {
  if (!attention) return null;

  return (
    <div className="flex flex-col items-center">
      {attention.map((alpha, i) => {
        const grid = alpha.flat();

        return (
          <div key={i} className="mb-4 relative">
            <img src={image} className="rounded-lg" />

            {/* Heatmap overlay */}
            <div className="absolute top-0 left-0 w-full h-full opacity-40 grid grid-cols-7">
              {grid.map((v, idx) => (
                <div
                  key={idx}
                  style={{
                    backgroundColor: `rgba(255,0,0,${v})`,
                  }}
                />
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
}