"use client";

import { useRouter } from "next/navigation";
import { Button } from "./ui/button";
import { toast } from "sonner";

const LogoutButton = () => {
  const router = useRouter();

  const handleLogout = () => {
    localStorage.removeItem("token");
    router.replace("/employee/login");
    toast.success("Logged out", {
      description: "You've been safely logged out.",
    });
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
