import { useState } from "react";
import Landing from "./components/Landing";
import Upload from "./components/Upload";

export default function App() {
  const [started, setStarted] = useState(false);

  return (
    <div
      style={{
        transition: "opacity 0.4s ease",
      }}
    >
      {!started ? (
        <Landing onStart={() => setStarted(true)} />
      ) : (
        <div className="animate-fade-in">
          <Upload />
        </div>
      )}
    </div>
  );
}