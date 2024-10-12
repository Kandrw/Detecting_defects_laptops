import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { MainPage } from "./App.tsx";
import "./index.css";
import { Header } from "./widgets/Header.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <Header />
    <MainPage />
  </StrictMode>
);
