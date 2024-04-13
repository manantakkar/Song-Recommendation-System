import SearchInput from "../../../../components/input/SearchInput";
import Input from "../../../../components/input";
import { FiPlusCircle } from "react-icons/fi";
import { LuMinusCircle } from "react-icons/lu";
import { useContext } from "react";
import { recommendationsContext } from "../..";

export default function RecommendationForm() {
  const { handelSubmit, n_songs, setN_songs, setSongs, songs } = useContext(
    recommendationsContext
  );
  return (
    <form
      onSubmit={handelSubmit}
      className="flex flex-col gap-5 py-10 px-5 shadow-[rgba(14,30,37,0.12)_0px_2px_4px_0px,_rgba(14,30,37,0.32)_0px_2px_16px_0px]"
    >
      <div className="grid gap-2">
        <label htmlFor="song">Song</label>
        {songs.map((value, idx) => {
          return (
            <div key={idx} className="flex items-center w-full gap-3">
              <SearchInput
                id={`search-${idx}`}
                key={idx}
                value={value}
                onSelect={(song) => {
                  songs[idx] = song;
                  setSongs([...songs]);
                }}
              />
              {idx == 0 && (
                <FiPlusCircle
                  data-tooltip-id="search-tooltip"
                  data-tooltip-content="Enter multiple songs"
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
            value={songs[0].artist}
            onChange={(e) => {
              songs[0].artist = e.target.value;
              setSongs([...songs]);
            }}
            id="artist"
            label="Artist"
            placeholder="Enter artist name (optional)"
          />

          <div className="grid grid-cols-2 gap-4 max-w-xl">
            <Input
              id="year"
              value={songs[0].year}
              label="Release Year"
              placeholder="Enter release year (optional)"
              type="text"
              pattern="[0-9]{4}"
              onChange={(e) => {
                songs[0].year = e.target.value;
                setSongs([...songs]);
              }}
            />
            <Input
              label="No. of Recommendations"
              id="n_song"
              placeholder="Enter no. of recommendations (optional)"
              type="number"
              pattern="^[-.]"
              value={n_songs}
              onChange={(e) => {
                let val = e.target.value.replace(/[-.]/, "");
                e.target.value = val;
                setN_songs(val);
              }}
            />
          </div>
        </>
      )}
      <div className="py-5">
        <button className="py-4 px-5 text-white bg-primary border-none outline-none w-fit rounded-lg hover:bg-blue-800 font-semibold">
          Get Recommendations
        </button>
      </div>
    </form>
  );
}
