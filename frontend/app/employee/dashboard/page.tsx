"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface Approval {
  id: number;
  visitor_id: number;
  employee_id: number;
  status: string;
  requested_at: string;
  decision_at: string | null;
  visitor?: any;
}

const EMPLOYEE_ID = 1;

const ApprovalDashboard = () => {
  const [approvals, setApprovals] = useState<Approval[]>([]);
  const [loading, setLoading] = useState(false);

  const fetchApprovals = async () => {
    try {
      const res = await axios.get(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/approvals/${EMPLOYEE_ID}`
      );
      setApprovals(res.data);
    } catch (err) {
      console.error("Error fetching approvals");
    }
  };

  const handleAction = async (id: number, status: "APPROVED" | "REJECTED") => {
    try {
      await axios.post(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/approvals/${id}/action`,
        { status }
      );
      await fetchApprovals();
    } catch (err) {
      alert("Failed to update approval status");
    }
  };

  useEffect(() => {
    fetchApprovals();
  }, []);

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Pending Visitor Approvals</h1>
      {approvals.length === 0 && (
        <p className="text-muted">No pending approvals</p>
      )}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {approvals.map((appr) => (
          <Card key={appr.id} className="p-4">
            <CardContent className="space-y-2">
              <p>
                <strong>Visitor ID: </strong>
                {appr.visitor_id}
              </p>
              <p>
                <strong>Approval ID: </strong>
                {appr.id}
              </p>
              <p>
                <strong>Requested at: </strong>
                {new Date(appr.requested_at).toLocaleString()}
              </p>
              <div className="flex gap-2">
                <Button
                  variant={"outline"}
                  onClick={() => handleAction(appr.id, "APPROVED")}
                  className="cursor-pointer"
                >
                  Approve
                </Button>
                <Button
                  variant={"destructive"}
                  onClick={() => handleAction(appr.id, "REJECTED")}
                  className="cursor-pointer"
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
};

export default ApprovalDashboard;
