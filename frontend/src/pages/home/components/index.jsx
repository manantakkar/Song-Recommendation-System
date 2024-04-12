import { useState } from "react";
import Input from "../../../components/input";
import { FiPlusCircle } from "react-icons/fi";
import { LuMinusCircle } from "react-icons/lu";
import axios from "axios";

export default function Home() {
  const [songs, setSongs] = useState([""]);
  const [artist, setArtist] = useState("");
  const [year, setYear] = useState("");
  const [nSongs, setNSongs] = useState("");

  const handelSubmit = async (e) => {
    e.preventDefault();
    const res = await axios.post(
      "http://localhost:8000/recommend/recommend-song/",
      {
        songs,
        artist,
        year,
        n_songs: Number(nSongs),
      }
    );
    console.log(res.data);
  };

  return (
    <div className="bg-black h-screen w-full flex flex-col items-center">
      <h1 className="capitalize text-white text-4xl font-bold py-10">
        song recommendation app
      </h1>
      <div className="w-full grid grid-cols-2 max-w-screen-2xl px-5">
        <form
          onSubmit={handelSubmit}
          className="text-white flex flex-col gap-5"
        >
          <div className="grid gap-2">
            <label htmlFor="song">Song</label>
            {songs.map((value, idx) => {
              return (
                <div key={idx} className="flex items-center w-full gap-3">
                  <input
                    value={value}
                    className="outline-none rounded py-2 px-4 border-none bg-gray-500 w-full text-white "
                    placeholder="Enter song name"
                    onChange={(e) => {
                      songs[idx] = e.target.value;
                      setSongs([...songs]);
                    }}
                  />
                  {idx == 0 && (
                    <FiPlusCircle
                      className="size-6 cursor-pointer"
                      onClick={() => {
                        if (songs.length < 5) {
                          setSongs([...songs, ""]);
                        }
                      }}
                    />
                  )}
                  {idx !== 0 && (
                    <LuMinusCircle
                      className="size-6 cursor-pointer"
                      onClick={() => {
                        setSongs(songs.filter((_, i) => i != idx));
                      }}
                    />
                  )}
                </div>
              );
            })}
          </div>
          {songs.length === 1 && (
            <>
              <Input
                value={artist}
                onChange={(e) => {
                  setArtist(e.target.value);
                }}
                id="artist"
                label="Artist"
                placeholder="Enter artist name (optional)"
              />

              <div className="grid grid-cols-2 gap-4">
                <Input
                  id="year"
                  value={year}
                  label="Release Year"
                  placeholder="Enter release year (optional)"
                  type="text"
                  pattern="[0-9]{4}"
                  onChange={(e) => {
                    setYear(e.target.value);
                  }}
                />
                <Input
                  label="No. of Recommendations"
                  id="n_song"
                  placeholder="Enter no. of recommendations (optional)"
                  type="number"
                  value={nSongs}
                  onChange={(e) => {
                    setNSongs(e.target.value);
                  }}
                />
              </div>
            </>
          )}
          <div className="py-5">
            <button className="py-4 px-5 bg-blue-700 border-none outline-none w-fit rounded-lg hover:bg-blue-800 font-semibold">
              Get Recommendations
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
