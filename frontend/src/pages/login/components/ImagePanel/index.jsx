// import skyscrapers from "@/assets/skyscrapers-sunset-sm.jpg";
export default function ImagePanel() {
  return (
    <div className="relative flex-1">
      <div
        style={{ backgroundImage: `url()` }}
        className="h-screen w-full bg-cover bg-bottom"
      />
      <div className="absolute inset-0 bg-primary bg-opacity-75">
        {/* //TODO add heading here */}
      </div>
    </div>
  );
}
