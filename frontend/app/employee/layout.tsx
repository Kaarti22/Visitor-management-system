"use client";

import EmployeeHeader from "@/components/employee-header";

const EmployeeLayout = ({ children }: { children: React.ReactNode }) => {
  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 text-gray-800 dark:text-white">
      <EmployeeHeader />
      <main>{children}</main>
    </div>
  );
};

export default EmployeeLayout;
