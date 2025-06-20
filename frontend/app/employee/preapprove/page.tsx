"use client";

import { useState } from "react";
import { useAuth } from "@/lib/useAuth";
import { toast } from "sonner";
import api from "@/lib/axios";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import { motion } from "framer-motion";
import { DateTimePicker } from "@/components/datetime-picker";
import { getEmployeeFromToken } from "@/lib/token";

const PreApprovePage = () => {
  useAuth();
  const employee = getEmployeeFromToken();

  const [visitorId, setVisitorId] = useState("");
  const [validFrom, setValidFrom] = useState<Date | undefined>();
  const [validTo, setValidTo] = useState<Date | undefined>();
  const [maxPerDay, setMaxPerDay] = useState(5);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validFrom || !validTo) {
      toast.error("Please select valid date & time");
      return;
    }

    setLoading(true);
    try {
      await api.post("/preapprovals/", {
        visitor_id: Number(visitorId),
        employee_id: employee?.id,
        valid_from: validFrom.toISOString(),
        valid_to: validTo.toISOString(),
        max_visits_per_day: maxPerDay,
      });
      toast.success("Pre-approval scheduled successfully");
      setVisitorId("");
      setValidFrom(undefined);
      setValidTo(undefined);
      setMaxPerDay(5);
    } catch (err: any) {
      toast.error(
        err.response?.data?.detail || "Failed to schedule pre-approval"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-white dark:bg-gray-900 px-4 py-10">
      <motion.div
        className="max-w-4xl mx-auto bg-gray-50 dark:bg-gray-800 shadow rounded-xl p-6 space-y-6"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-center text-gray-900 dark:text-white">
          Pre-Approve a Visitor
        </h1>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="visitorId">Visitor ID</Label>
              <Input
                id="visitorId"
                type="number"
                value={visitorId}
                onChange={(e) => setVisitorId(e.target.value)}
                required
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="maxPerDay">Max Visits Per Day</Label>
              <Input
                id="maxPerDay"
                type="number"
                min={1}
                value={maxPerDay}
                onChange={(e) => setMaxPerDay(Number(e.target.value))}
              />
            </div>
          </div>

          <div className="grid sm:grid-cols-2 gap-4">
            <DateTimePicker
              label="Valid From"
              value={validFrom}
              onChange={setValidFrom}
            />
            <DateTimePicker
              label="Valid To"
              value={validTo}
              onChange={setValidTo}
            />
          </div>

          <div className="pt-4">
            <Button type="submit" className="w-full cursor-pointer" disabled={loading}>
              {loading ? "Scheduling..." : "Schedule Pre-Approval"}
            </Button>
          </div>
        </form>
      </motion.div>
    </main>
  );
};

export default PreApprovePage;
