"use client";

import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { useAuth } from "@/lib/useAuth";
import { getEmployeeFromToken } from "@/lib/token";
import api from "@/lib/axios";
import { toast } from "sonner";

interface Approval {
  id: number;
  visitor_id: number;
  employee_id: number;
  status: string;
  requested_at: string;
  decision_at: string | null;
  visitor?: any;
}

export default function ApprovePage() {
  useAuth();
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [loading, setLoading] = useState(false);
  const employee = getEmployeeFromToken();

  const fetchApprovals = async () => {
    if (!employee?.id) return;
    try {
      const res = await api.get(`/approvals/${employee.id}`);
      setApprovals(res.data);
    } catch {
      console.error("Error fetching approvals");
    }
  };

  const handleAction = async (id: number, status: "APPROVED" | "REJECTED") => {
    setLoading(true);
    try {
      await api.post(`/approvals/${id}/action`, { status });
      toast.success(`Approval ID ${id} approved`);
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
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Pending Approvals</h1>
      {approvals.length === 0 && <p>No pending approvals</p>}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {approvals.map((appr) => (
          <Card key={appr.id} className="p-4">
            <CardContent className="space-y-2">
              <p>
                <strong>Visitor ID:</strong> {appr.visitor_id}
              </p>
              <p>
                <strong>Approval ID:</strong> {appr.id}
              </p>
              <p>
                <strong>Requested:</strong>{" "}
                {new Date(appr.requested_at).toLocaleString()}
              </p>
              <div className="flex gap-2">
                <Button
                  onClick={() => handleAction(appr.id, "APPROVED")}
                  variant="outline"
                  className="cursor-pointer"
                  disabled={loading}
                >
                  Approve
                </Button>
                <Button
                  onClick={() => handleAction(appr.id, "REJECTED")}
                  variant="destructive"
                  className="cursor-pointer"
                  disabled={loading}
                >
                  Reject
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}
