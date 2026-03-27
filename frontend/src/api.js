import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

export const predict = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await API.post("/predict", formData);
  return res.data;
};

export const visualize = async (file) => {
  const formData = new FormData();
  formData.append("file", file);

  const res = await API.post("/visualize", formData);
  return res.data;
};