"use client";

import LogoutButton from "./logout-button";
import { getEmployeeFromToken } from "@/lib/token";
import { useEffect, useState } from "react";
import Link from "next/link";

const EmployeeHeader = () => {
  const [employeeName, setEmployeeName] = useState("");

  useEffect(() => {
    const employee = getEmployeeFromToken();
    if (employee) {
      const name = employee.sub?.split("@")[0];
      setEmployeeName(name);
    }
  }, []);

  return (
    <header className="w-full px-6 py-4 bg-white dark:bg-gray-900 border-b border-gray-200 dark:border-gray-700 flex justify-between items-center">
      <Link href="/employee/dashboard">
        <h1 className="text-xl font-bold text-gray-800 dark:text-white">
          VisitorEase Admin
        </h1>
      </Link>

      <div className="flex items-center gap-4">
        <p className="text-sm text-gray-600 dark:text-gray-300">
          Hello, <span className="font-medium">{employeeName}</span> 👋
        </p>
        <LogoutButton />
      </div>
    </header>
  );
};

export default EmployeeHeader;
