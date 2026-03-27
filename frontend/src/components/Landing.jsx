export default function Landing({ onStart }) {
  return (
    <div className="flex flex-col items-center justify-center h-screen bg-gradient-to-r from-blue-500 to-indigo-600 text-white">
      <h1 className="text-5xl font-bold mb-6">Image Captioning AI</h1>
      <p className="mb-6 text-lg">Upload an image and see AI describe it</p>

      <button
        onClick={onStart}
        className="px-6 py-3 bg-white text-blue-600 rounded-lg font-semibold hover:bg-gray-200"
      >
        Get Started
      </button>
    </div>
  );
}