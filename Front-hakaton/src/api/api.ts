import axios from "axios";

export const instance = axios.create({
  baseURL: "http://localhost:8000/api",
});

export const api = {
  async postUpload(formData: FormData) {
    const response = await instance.post("/upload/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
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
  async postReportPDF(serialNumber: string, defects: object) {
    const response = await instance.post(
      "/submit-report-pdf/",
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
