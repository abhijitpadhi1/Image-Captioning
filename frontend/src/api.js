import axios from "axios";

const API = axios.create({
  baseURL: "/api",
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