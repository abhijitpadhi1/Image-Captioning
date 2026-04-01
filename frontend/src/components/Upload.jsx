import { useState } from "react";
import { predict, visualize } from "../api";
import Tabs from "./Tabs";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [imageURL, setImageURL] = useState(null);
  const [caption, setCaption] = useState("");
  const [attention, setAttention] = useState(null);
  const [loaded, setLoaded] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return;

    const url = URL.createObjectURL(file);
    setImageURL(url);

    const pred = await predict(file);
    const vis = await visualize(file);

    setCaption(pred.caption);
    setAttention(vis.attention_maps);
    setLoaded(true);
  };

  const reset = () => {
    setFile(null);
    setImageURL(null);
    setCaption("");
    setAttention(null);
    setLoaded(false);
    setLoading(false);
  };

  return (
    <div className="p-6">
      {!loaded && !loading && (
        <div className="flex flex-col items-center">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button
            onClick={handleUpload}
            disabled={loading}
            className={`mt-4 px-6 py-2 rounded ${
              loading ? "bg-gray-400" : "bg-blue-500 text-white"
            }`}
          >
            {loading ? "Processing..." : "Upload & Predict"}
          </button>
        </div>
      )}

      {loading && (
        <div className="flex flex-col items-center mt-10">
          <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500"></div>
          <p className="mt-4 text-gray-600">Analyzing image...</p>
        </div>
      )}

      {loaded && !loading && (
        <Tabs
          image={imageURL}
          caption={caption}
          attention={attention}
          onReset={reset}
        />
      )}
    </div>
  );
}