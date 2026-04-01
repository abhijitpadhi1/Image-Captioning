export default function Loader() {
  return (
    <div className="flex flex-col items-center justify-center mt-10">
      <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-blue-500"></div>
      <p className="mt-4 text-gray-600">Generating caption...</p>
    </div>
  );
}