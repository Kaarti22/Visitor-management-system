"use client";

import { useRouter } from "next/navigation";
import { Button } from "./ui/button";

const LogoutButton = () => {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.replace("/employee/login");
  };

  return (
    <Button
      variant={"destructive"}
      className="cursor-pointer"
      onClick={handleLogout}
    >
      Logout
    </Button>
  );
};

export default LogoutButton;
