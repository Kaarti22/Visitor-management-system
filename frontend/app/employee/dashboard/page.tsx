"use client";

import api from "@/lib/axios";
import { getEmployeeFromToken } from "@/lib/token";
import { useAuth } from "@/lib/useAuth";
import { useEffect, useState } from "react";
import { toast } from "sonner";
import { motion } from "framer-motion";
import Link from "next/link";
import { Button } from "@/components/ui/button";

interface Approval {
  id: number;
  status: "APPROVED" | "PENDING" | "REJECTED";
  requested_at: string;
  decision_at: string | null;
}

interface PreApproval {
  id: number;
  valid_from: string;
  valid_to: string;
}

const Dashboard = () => {
  useAuth();
  const employee = getEmployeeFromToken();
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [preapprovals, setPreapprovals] = useState<PreApproval[]>([]);

  const today = new Date().toISOString().slice(0, 10);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [apprRes, preRes] = await Promise.all([
          api.get(`/approvals/${employee?.id}`),
          api.get(`/preapprovals/${employee?.id}`),
        ]);
        setApprovals(apprRes.data);
        setPreapprovals(preRes.data);
      } catch (err) {
        toast.error("Error fetching dashboard data");
      }
    };

    fetchData();
    console.log(approvals);
    console.log(preapprovals);
  }, [employee?.id]);

  const approvedCount = approvals.filter((a) => a.status === 'APPROVED').length;
  const todayApproved = approvals.filter(
    (a) => a.decision_at?.slice(0, 10) === today && a.status === 'APPROVED'
  ).length;

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-white dark:from-gray-900 dark:to-gray-800 p-8">
      <motion.h1
        className="text-3xl font-bold mb-8 text-gray-800 dark:text-white"
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
      >
        Welcome back, {employee?.sub.split("@")[0]}
      </motion.h1>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {[
          {
            title: "Approved Visitors",
            count: approvedCount,
            color: "bg-green-100 dark:bg-green-800",
          },
          {
            title: "Pre-Approvals Scheduled",
            count: preapprovals.length,
            color: "bg-blue-100 dark:bg-blue-800",
          },
          {
            title: "Visitors Today",
            count: todayApproved,
            color: "bg-purple-100 dark:bg-purple-800",
          },
        ].map((stat, i) => (
          <motion.div
            key={i}
            className={`rounded-xl p-6 shadow-lg text-center ${stat.color}`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 * i, duration: 0.6 }}
          >
            <h2 className="text-lg font-medium text-gray-700 dark:text-white mb-2">
              {stat.title}
            </h2>
            <p className="text-4xl font-bold text-gray-900 dark:text-white">
              {stat.count}
            </p>
          </motion.div>
        ))}
      </div>

      <div className="flex flex-wrap gap-4">
        <Link href="/employee/approve">
          <Button size="lg" className="cursor-pointer">
            Approve Visitors
          </Button>
        </Link>
        <Link href="/employee/preapprove">
          <Button variant="outline" size="lg" className="cursor-pointer">
            Schedule Pre-Approval
          </Button>
        </Link>
      </div>
    </main>
  );
};

export default Dashboard;
