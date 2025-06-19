"use client";

import { useAuth } from "@/lib/useAuth";

export default function EmployeeDashboard() {
  useAuth();

  return (
    <div className="max-w-xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Welcome to your Dashboard</h1>
      <ul className="list-disc pl-4 space-y-2">
        <li>
          <a href="/employee/approve" className="text-blue-600 underline">
            View & Approve Visitors
          </a>
        </li>
        <li>
          <a href="/employee/preapprove" className="text-blue-600 underline">
            Schedule a Pre-Approval
          </a>
        </li>
      </ul>
    </div>
  );
}
