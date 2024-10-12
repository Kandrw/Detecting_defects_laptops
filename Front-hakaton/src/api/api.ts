import axios from "axios";

export const instance = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const api = {
  async postUpload() {
    const response = await instance.post("/upload/");
    return response;
  },
  async postReport(serialNumber: string, defects: object) {
    const response = await instance.post(
      "/submit-report/",
      {
        serialNumber,
        defects,
      },
      {
        responseType: "blob",
      }
    );
    return response;
  },
};
