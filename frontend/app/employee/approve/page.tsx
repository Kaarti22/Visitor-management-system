"use client";

import { useEffect, useState } from "react";
import { CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/useAuth";
import { getEmployeeFromToken } from "@/lib/token";
import api from "@/lib/axios";
import { toast } from "sonner";
import { motion } from "framer-motion";

interface Approval {
  id: number;
  visitor_id: number;
  employee_id: number;
  status: string;
  requested_at: string;
  decision_at: string | null;
  visitor?: {
    full_name: string;
    company: string;
    purpose: string;
    photo_url?: string;
  };
}

export default function ApprovePage() {
  useAuth();
  const employee = getEmployeeFromToken();
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchApprovals = async () => {
    if (!employee?.id) return;
    try {
      const res = await api.get(`/approvals/${employee.id}?status=PENDING`);
      setApprovals(res.data);
    } catch {
      console.error("Error fetching approvals");
    }
  };

  const handleAction = async (id: number, status: "APPROVED" | "REJECTED") => {
    setLoading(true);
    try {
      await api.post(`/approvals/${id}/action`, { status });
      toast.success(`Visitor ${status.toLowerCase()}`);
      await fetchApprovals();
    } catch {
      toast.error("Failed to update approval");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchApprovals();
  }, []);

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-white dark:from-gray-900 dark:to-gray-800 px-4 py-8">
      <h1 className="text-3xl font-bold mb-8 text-center text-gray-800 dark:text-white">
        Pending Visitor Approvals
      </h1>

      {approvals.length === 0 && (
        <p className="text-center text-gray-500 dark:text-gray-400">
          No pending approvals
        </p>
      )}

      <div className="grid gap-6 sm:grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
        {approvals.map((appr, i) => (
          <motion.div
            key={appr.id}
            className="bg-white dark:bg-gray-900 rounded-xl shadow-lg p-6 border border-gray-200 dark:border-gray-700"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <CardContent className="space-y-2 text-sm text-gray-700 dark:text-gray-200">
              <p>
                <strong>Visitor:</strong> {appr.visitor?.full_name || "N/A"}
              </p>
              <p>
                <strong>Company:</strong> {appr.visitor?.company || "N/A"}
              </p>
              <p>
                <strong>Purpose:</strong> {appr.visitor?.purpose || "N/A"}
              </p>
              <p>
                <strong>Requested At:</strong>{" "}
                {new Date(appr.requested_at).toLocaleString()}
              </p>

              <div className="flex flex-col gap-3 pt-4">
                <Button
                  onClick={() => handleAction(appr.id, "APPROVED")}
                  disabled={loading}
                  className="w-full cursor-pointer"
                >
                  Approve
                </Button>
                <Button
                  onClick={() => handleAction(appr.id, "REJECTED")}
                  variant="destructive"
                  disabled={loading}
                  className="w-full cursor-pointer"
                >
                  Reject
                </Button>
              </div>
            </CardContent>
          </motion.div>
        ))}
      </div>
    </main>
  );
}
