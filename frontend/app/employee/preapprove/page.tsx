"use client";

import { useAuth } from "@/lib/useAuth";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import api from "@/lib/axios";
import { useState } from "react";
import { getEmployeeFromToken } from "@/lib/token";

const employee = getEmployeeFromToken();
const employeeId = employee?.id;

const PreApprovePage = () => {
  useAuth();

  const [visitorId, setVisitorId] = useState("");
  const [validFrom, setValidFrom] = useState("");
  const [validTo, setValidTo] = useState("");
  const [maxPerDay, setMaxPerDay] = useState(5);
  const [message, setMessage] = useState("");

  const handleSubmit = async (ev: any) => {
    ev.preventDefault();
    try {
      await api.post(
        `/preapprovals/`,
        {
          visitor_id: Number(visitorId),
          employee_id: employeeId,
          valid_from: validFrom,
          valid_to: validTo,
          max_visits_per_day: maxPerDay,
        }
      );
      setMessage("Pre-approval scheduled successfully");
    } catch (err: any) {
      setMessage(
        err.response?.data?.detail || "Failed to schedule pre-approval"
      );
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold">Pre-Approve a Visitor</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <Label htmlFor="visitor_id">Visitor ID</Label>
          <Input
            id="visitor_id"
            value={visitorId}
            onChange={(e) => setVisitorId(e.target.value)}
            required
          />
        </div>
        <div>
          <Label htmlFor="valid_from">Valid From (UTC)</Label>
          <Input
            type="datetime-local"
            id="valid_from"
            value={validFrom}
            onChange={(e) => setValidFrom(e.target.value)}
            required
          />
        </div>
        <div>
          <Label htmlFor="valid_to">Valid To (UTC)</Label>
          <Input
            type="datetime-local"
            id="valid_to"
            value={validTo}
            onChange={(e) => setValidTo(e.target.value)}
            required
          />
        </div>
        <div>
          <Label htmlFor="max_per_day">Max Visitors Per Day</Label>
          <Input
            type="number"
            id="max_per_day"
            value={maxPerDay}
            onChange={(e) => setMaxPerDay(Number(e.target.value))}
          />
        </div>
        <Button type="submit" className="cursor-pointer">
          Schedule Pre-Approval
        </Button>
      </form>

      {message && <p className="mt-4 text-green-600 font-medium">{message}</p>}
    </div>
  );
};

export default PreApprovePage;
