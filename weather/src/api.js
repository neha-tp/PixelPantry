import axios from "axios";

const API_BASE_URL = "http://localhost:5000/api"; // Flask backend URL

export const getWeather = async (location) => {
    return axios.get(`${API_BASE_URL}/weather/${location}`);
};

export const getAlerts = async (location) => {
    return axios.get(`${API_BASE_URL}/alert/${location}`);
};

export const getNGOs = async () => {
    return axios.get(`${API_BASE_URL}/Ngo`);
};

export const registerUser = async (userData) => {
    return axios.post(`${API_BASE_URL}/User`, userData);
};
