import { Logo } from "../shared/ui/Logo";

export const Header = () => (
  <header className=" bg-gray-200 h-[60px] w-full flex flex-row items-center">
    <div className="pl-6">
      <Logo />
    </div>
  </header>
);
