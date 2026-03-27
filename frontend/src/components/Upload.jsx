import { useState } from "react";
import { predict, visualize } from "../api";
import Tabs from "./Tabs";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [imageURL, setImageURL] = useState(null);
  const [caption, setCaption] = useState("");
  const [attention, setAttention] = useState(null);
  const [loaded, setLoaded] = useState(false);

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
  };

  return (
    <div className="p-6">
      {!loaded ? (
        <div className="flex flex-col items-center">
          <input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <button
            onClick={handleUpload}
            className="mt-4 px-6 py-2 bg-blue-500 text-white rounded"
          >
            Upload & Predict
          </button>
        </div>
      ) : (
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