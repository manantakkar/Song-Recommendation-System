import React from "react";
import defaultImage from "../../../../assets/image.png";
/**
 * @typedef Song
 * @property {string} name
 * @property {string[]} artist
 * @property {string} year
 * @property {string} image_link
 * @property {string} spotify_link
 * @param {Object} props
 * @param {Song[]} props.songs
 */

export default function Recommendations({ songs }) {
  return (
    <div
      className={`w-full ${
        songs.length === 0 ? "opacity-0" : "opacity-100"
      } transition-all duration-300 bg-primary rounded-lg shadow-[rgba(14,30,37,0.12)_0px_2px_4px_0px,_rgba(14,30,37,0.32)_0px_2px_16px_0px]`}
    >
      <h2 className="text-white text-3xl text-center font-bold py-4">
        Recommended Songs
      </h2>
      <div className="w-full px-5 pt-5 grid gap-4 overflow-auto max-h-[70vh]">
        {songs.map((song, idx) => {
          return (
            <a
              href={song.spotify_link}
              target="_blank"
              key={idx}
              onClick={() => {
                setSearch(song.name);
                setSongSuggestion([]);
                if (onSelect) {
                  onSelect(song);
                }
              }}
              className="flex py-2 px-5 rounded-md items-center gap-3 w-full cursor-pointer border-b-[0.6px] border-[#4949492f] bg-white"
            >
              <img
                className="block size-10 rounded-full"
                src={song.image_link || defaultImage}
              />

              <div className="grid gap-1">
                <h5 className="text-lg font-medium leading-none">
                  {song.name}
                </h5>
                <p className="text-sm">{song.artist.join(", ")}</p>
              </div>
            </a>
          );
        })}
      </div>
    </div>
  );
}
