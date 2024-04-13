import axios from "axios";
import React, { useEffect, useState } from "react";
import { axiosInstance, speechRecognition } from "../../utils";
import debounce from "lodash.debounce";
import { IoMic, IoSearchOutline } from "react-icons/io5";
import defaultImage from "../../assets/image.png";
/**
 * @typedef song
 * @property {string} name
 * @property {string} artist
 * @property {string} year
 * @property {string} image_link
 * @param {Object} props
 * @param {(song:song)=>void} props.onSelect
 * @param {song} props.value
 * @param {string} props.id
 */

export default function SearchInput({ onSelect, value, id }) {
  const [search, setSearch] = useState(value.name);
  const [cancelToken, setCancelToken] = useState(null);
  const [songSuggestion, setSongSuggestion] = useState([]);

  const { start } = speechRecognition(
    (val) => {
      setSearch(val);
      if (val !== "Listening...") {
        searchSongs(val);
      }
    },
    (err) => {
      search("");
    }
  );
  useEffect(() => {
    return () => {
      if (cancelToken) {
        cancelToken.cancel("Operation canceled by cleanup");
      }
    };
  }, [cancelToken]);

  const searchSongs = async (search) => {
    if (search === "") {
      onSelect({
        artist: "",
        image_link: "",
        name: "",
        year: "",
      });
      setSongSuggestion([]);
      return;
    }
    try {
      const newCancelToken = axios.CancelToken.source();
      setCancelToken(newCancelToken);

      const response = await axiosInstance.get("search/", {
        params: {
          search,
        },
        cancelToken: newCancelToken.token,
      });

      setSongSuggestion(response.data.songs);
    } catch (error) {
      if (axios.isCancel(error)) {
        console.log("Request canceled:", error.message);
      } else {
        console.log(error);
      }
    }
  };

  const debouncedSearchSongs = debounce(searchSongs);

  const handleSearchChange = (e) => {
    e.target.setCustomValidity("");
    setSearch(e.target.value);
    debouncedSearchSongs(e.target.value, cancelToken);
  };
  return (
    <div className="w-full max-w-xl rounded-lg border border-gray-300 flex items-center px-5 relative">
      <label htmlFor={id}>
        <IoSearchOutline className="size-6" />
      </label>
      <input
        value={search}
        id={id}
        onChange={handleSearchChange}
        type="text"
        className="px-4 py-3  w-full border-none outline-none focus-within:bg-transparent active:bg-transparent"
        placeholder="Enter song name"
        required
        title="please enter a song name"
      />
      <IoMic onClick={start} className="size-6 cursor-pointer" />
      <div className="absolute rounded-lg px-5 left-0 w-full grid gap-3 top-[60px] max-h-96 overflow-y-auto bg-white z-10 shadow-[#00000059_0px_5px_15px]">
        {songSuggestion.map((song, idx) => {
          return (
            <div
              key={idx}
              onClick={() => {
                setSearch(song.name);
                setSongSuggestion([]);
                if (onSelect) {
                  onSelect(song);
                }
              }}
              className="flex py-2 items-center gap-3 w-full cursor-pointer border-b-[0.6px] border-[#4949492f]"
            >
              <img
                className="block size-10 rounded-full"
                src={song.image_link || defaultImage}
              />

              <div className="grid gap-1">
                <h5 className="text-lg font-medium leading-none">
                  {song.name}
                </h5>
                <p className="text-sm">{song.artist}</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
