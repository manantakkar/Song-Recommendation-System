import { createContext, useState } from "react";

import { Tooltip } from "react-tooltip";
import "react-tooltip/dist/react-tooltip.css";

export const recommendationsContext = createContext({
  handelSubmit: () => {},
  n_songs: "",
  setN_songs: () => {},
  songs: [],
  setSongs: () => {},
});

import Navbar from "../../components/navbar";
import { axiosInstance } from "../../utils";
import Loading from "./components/loading";
import Recommendations from "./components/recommendations";

import { Outlet } from "react-router-dom";

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [recommendations, setRecommendations] = useState([]);
  const [songs, setSongs] = useState([
    {
      name: "",
      artist: "",
      image_link: "",
      year: "",
    },
  ]);

  const [n_songs, setN_songs] = useState("");

  const handelSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    try {
      let data;
      if (songs.length == 1) {
        const song = songs[0];
        data = {
          songs: [song.name],
          artist: song.artist,
          year: song.year,
          n_songs: Number(n_songs) || 5,
        };
      } else if (songs.length > 1) {
        data = {
          songs: songs.map((song) => song.name),
        };
      }
      const response = await axiosInstance.post("recommend-song/", data);
      setRecommendations(response.data.songs);
    } catch (e) {
      console.log(e);
    } finally {
      setIsLoading(false);
    }
  };


  return (
    <recommendationsContext.Provider
      value={{
        handelSubmit,
        n_songs,
        setN_songs,
        setSongs,
        songs,
      }}
    >
      <div className="overflow-hidden h-screen">
        <Navbar />
        <div className="w-full flex flex-col items-center h-4/5">
          <div
            className={`w-fit grid gap-10 max-w-screen-2xl px-5 py-10 h-full transition-all duration-300 ${
              recommendations.length > 0 ? "grid-cols-2" : ""
            }`}
          >
            <Outlet />
            <Recommendations songs={recommendations} />
          </div>
        </div>
        <Tooltip id="search-tooltip" />
        {isLoading && <Loading />}
      </div>
    </recommendationsContext.Provider>
  );
}
