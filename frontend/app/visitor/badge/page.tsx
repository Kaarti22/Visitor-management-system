"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "sonner";
import { motion } from "framer-motion";

const BadgePage = () => {
  const searchParams = useSearchParams();
  const visitorId = searchParams.get("id");
  const [visitor, setVisitor] = useState<any>(null);

  useEffect(() => {
    const fetchVisitor = async () => {
      if (!visitorId) return;
      try {
        const res = await axios.get(
          `${process.env.NEXT_PUBLIC_API_BASE_URL}/visitors/${visitorId}`
        );
        setVisitor(res.data);
      } catch {
        toast.error("Visitor not found");
      }
    };
    fetchVisitor();
  }, [visitorId]);

  if (!visitorId)
    return <p className="p-4">Visitor ID is missing in the URL.</p>;
  if (!visitor) return <p className="p-4">Loading visitor badge...</p>;

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-white dark:from-gray-900 dark:to-gray-800 flex items-center justify-center px-4">
      <motion.div
        className="bg-white dark:bg-gray-900 border rounded-xl shadow-xl p-8 w-full max-w-md text-center space-y-4"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <h1 className="text-3xl font-bold text-gray-800 dark:text-white">
          Visitor Badge
        </h1>

        {visitor.badge_url ? (
          <img
            src={visitor.badge_url}
            alt="QR Badge"
            className="w-40 h-40 mx-auto border rounded bg-white p-2"
          />
        ) : (
          <p className="text-red-500 font-medium">
            Badge not available yet. Please wait for approval.
          </p>
        )}

        <div className="text-left space-y-1 text-gray-700 dark:text-gray-200">
          <p>
            <strong>Name:</strong> {visitor.full_name}
          </p>
          <p>
            <strong>Company:</strong> {visitor.company || "N/A"}
          </p>
          <p>
            <strong>Host:</strong> {visitor.host_employee_name}
          </p>
          <p>
            <strong>Department:</strong> {visitor.host_department}
          </p>
        </div>

        <p className="text-sm text-gray-500 dark:text-gray-400 mt-4">
          Please show this badge at the security gate.
        </p>
      </motion.div>
    </main>
  );
};

export default BadgePage;
