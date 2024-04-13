import React, { useContext, useState } from "react";
import { axiosInstance } from "../../../../utils";
import { recommendationsContext } from "../..";
import Input from "../../../../components/input";
import Loading from "../loading";

export default function RecommendationByUrl() {
  const [n_songs, setN_songs] = useState("");
  const [url, setUrl] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const { setSongs } = useContext(recommendationsContext);

  const handelSubmit = async (e) => {
    try {
      e.preventDefault();
      setIsLoading(true);
      const res = await axiosInstance.post("recommend-playlist/", {
        URL: url,
        n_songs: Number(n_songs) || 5   ,
      });
      setSongs(res.data);
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <form
      onSubmit={handelSubmit}
      className="flex flex-col justify-center min-w-[520px] gap-5 py-10 px-5 shadow-[rgba(14,30,37,0.12)_0px_2px_4px_0px,_rgba(14,30,37,0.32)_0px_2px_16px_0px]"
    >
      <div className="grid gap-4">
        <Input
          value={url}
          onChange={(e) => {
            setUrl(e.target.value);
          }}
          id="url"
          label="Spotify playlist Url"
          placeholder="Enter playlist url"
          required
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

      <div className="py-5">
        <button className="py-4 px-5 text-white bg-primary border-none outline-none w-fit rounded-lg hover:bg-blue-800 font-semibold">
          Get Recommendations
        </button>
      </div>
      {isLoading && <Loading />}
    </form>
  );
}
