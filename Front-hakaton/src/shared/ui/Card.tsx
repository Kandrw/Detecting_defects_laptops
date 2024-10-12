// card.tsx
import clsx from "clsx";
import { FC } from "react";

interface CardProps {
  title: string; // Title will be a string (label)
  value: string; // The value for the input
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void; // Function to handle input change
  className?: string;
}

export const Card: FC<CardProps> = ({ title, value, onChange, className }) => (
  <div className={clsx("", className)}>
    <h1 className="border-0 indent-0 font-medium">{title}</h1>
    <input
      type="text"
      value={value}
      onChange={onChange}
      className="w-full p-2 mb-2 border rounded-md"
    />
  </div>
);
