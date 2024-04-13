import axios from "axios";

export const BASE_URL = import.meta.env.VITE_SERVER_URL;

export const axiosInstance = axios.create({
  baseURL: BASE_URL,
});
