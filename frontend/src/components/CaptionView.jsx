export default function CaptionView({ image, caption }) {
  return (
    <div className="text-center">
      <img src={image} className="rounded-lg shadow mb-4" />
      <p className="text-lg font-semibold">{caption}</p>
    </div>
  );
}