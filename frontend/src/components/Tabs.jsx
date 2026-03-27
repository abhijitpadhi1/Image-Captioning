import { useState } from "react";
import CaptionView from "./CaptionView";
import AttentionView from "./AttentionView";

export default function Tabs({ image, caption, attention, onReset }) {
  const [tab, setTab] = useState("caption");

  return (
    <div className="flex flex-col items-center">

      {/* Toggle */}
      <div className="mb-4">
        <button
          onClick={() => setTab("caption")}
          className={`px-4 py-2 ${tab === "caption" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
        >
          Caption
        </button>

        <button
          onClick={() => setTab("attention")}
          className={`px-4 py-2 ${tab === "attention" ? "bg-blue-500 text-white" : "bg-gray-200"}`}
        >
          Attention
        </button>
      </div>

      {/* Content */}
      <div className="w-full max-w-2xl">
        {tab === "caption" && <CaptionView image={image} caption={caption} />}
        {tab === "attention" && <AttentionView image={image} attention={attention} />}
      </div>

      {/* Reset */}
      <button
        onClick={onReset}
        className="mt-6 px-6 py-2 bg-red-500 text-white rounded"
      >
        Reset
      </button>
    </div>
  );
}