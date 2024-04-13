import { Link, useLocation } from "react-router-dom";

export default function Navbar() {
  const { pathname } = useLocation();
  return (
    <div className="flex w-full justify-center">
      <div className="flex justify-between items-center gap-5 max-w-[1600px] w-full px-5 min-[1600px]:px-0 py-5">
        <h1 className="whitespace-nowrap font-bold text-3xl font-Oxanium">
          <span className="text-primary">Melo</span>
          <span className="text-pristine_oceanic">Map</span>
        </h1>
        <div className="flex w-full max-w-xs justify-around">
          {pathname === "/" ? (
            <Link className="text-lg font-semibold cursor-pointer" to="/url">
              Recommendation By Url
            </Link>
          ) : (
            <Link className="text-lg font-semibold cursor-pointer" to="/">
              Recommendation By Songs
            </Link>
          )}
        </div>
      </div>
    </div>
  );
}
