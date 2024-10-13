import { memo } from "react";
import LogoIcon from "../../assets/images/logo.png";

export const Logo = memo(() => {
  return (
    <div>
      <img className=" h-10 w-10" src={LogoIcon} alt="logo" />
    </div>
  );
});
