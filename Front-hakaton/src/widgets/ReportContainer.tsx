import React from "react";
import { Card } from "../shared/ui/Card";

interface IDefects {
  Lock: string;
  UnknownDefect: string;
  MissingScrew: string;
  KeysProblems: string;
  Chipped: string;
  BrokenPixel: string;
  Scratch: string;
  NoDefect: string;
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
        title="Замок"
        value={defectsData.Lock}
        onChange={(e) => onDefectChange("Lock", e.target.value)}
      />
      <Card
        title="Неизвестный дефект"
        value={defectsData.UnknownDefect}
        onChange={(e) => onDefectChange("UnknownDefect", e.target.value)}
      />
      <Card
        title="Отсутствует шуруп"
        value={defectsData.MissingScrew}
        onChange={(e) => onDefectChange("MissingScrew", e.target.value)}
      />
      <Card
        title="Проблемы с клавишами"
        value={defectsData.KeysProblems}
        onChange={(e) => onDefectChange("KeysProblems", e.target.value)}
      />
      <Card
        title="Сколы"
        value={defectsData.Chipped}
        onChange={(e) => onDefectChange("Chipped", e.target.value)}
      />
      <Card
        title="Битые пиксели"
        value={defectsData.BrokenPixel}
        onChange={(e) => onDefectChange("BrokenPixel", e.target.value)}
      />
      <Card
        title="Царапины"
        value={defectsData.Scratch}
        onChange={(e) => onDefectChange("Scratch", e.target.value)}
      />
      <Card
        title="Нет деффекта"
        value={defectsData.NoDefect}
        onChange={(e) => onDefectChange("NoDefect", e.target.value)}
      />
    </div>
  );
};
