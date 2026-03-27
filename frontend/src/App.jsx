import { useState } from "react";
import Landing from "./components/Landing";
import Upload from "./components/Upload";

export default function App() {
  const [started, setStarted] = useState(false);

  return (
    <div className="min-h-screen bg-gray-100">
      {!started ? (
        <Landing onStart={() => setStarted(true)} />
      ) : (
        <Upload />
      )}
    </div>
  );
}