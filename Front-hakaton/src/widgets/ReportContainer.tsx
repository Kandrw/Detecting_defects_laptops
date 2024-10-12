import React from "react";
import { Card } from "../shared/ui/Card";

interface IDefects {
  Scratches: string;
  BrokenPixels: string;
  ProblemsWithButtons: string;
  Zamok: string;
  MissingScrew: string;
  Chips: string;
  ImgRes: string;
}

interface ResponseContainerProps {
  defectsData: IDefects;
  onDefectChange: (key: keyof IDefects, value: string) => void;
}

export const ReportContainer: React.FC<ResponseContainerProps> = ({
  defectsData,
  onDefectChange,
}) => {
  return (
    <div className="w-[30rem]">
      <Card
        title="Scratches"
        value={defectsData.Scratches}
        onChange={(e) => onDefectChange("Scratches", e.target.value)}
      />
      <Card
        title="BrokenPixels"
        value={defectsData.BrokenPixels}
        onChange={(e) => onDefectChange("BrokenPixels", e.target.value)}
      />
      <Card
        title="ProblemsWithButtons"
        value={defectsData.ProblemsWithButtons}
        onChange={(e) => onDefectChange("ProblemsWithButtons", e.target.value)}
      />
      <Card
        title="Zamok"
        value={defectsData.Zamok}
        onChange={(e) => onDefectChange("Zamok", e.target.value)}
      />
      <Card
        title="MissingScrew"
        value={defectsData.MissingScrew}
        onChange={(e) => onDefectChange("MissingScrew", e.target.value)}
      />
      <Card
        title="Chips"
        value={defectsData.Chips}
        onChange={(e) => onDefectChange("Chips", e.target.value)}
      />
      <div className="flex flex-col items-center">
        <h3 className="font-bold">Результат изображения:</h3>
        {defectsData.ImgRes ? (
          <img
            src={defectsData.ImgRes}
            alt="Результат"
            className="w-4/5 h-auto rounded-md"
          />
        ) : (
          <p className="text-gray-500">Изображение не доступно</p>
        )}
      </div>
    </div>
  );
};
