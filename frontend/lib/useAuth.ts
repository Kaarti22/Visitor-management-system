"use client";

import { useRouter } from "next/navigation";
import { useEffect } from "react";

export const useAuth = () => {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      router.replace("/employee/login");
    }
  }, []);
};
