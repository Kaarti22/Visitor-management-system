"use client";

import { useSearchParams } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";
import { toast } from "sonner";

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
      } catch (err) {
        toast.error("Visitor not found");
      }
    };
    fetchVisitor();
  }, [visitorId]);

  if (!visitorId)
    return <p className="p-4">Visitor ID is missing in the URL.</p>;
  if (!visitor) return <p className="p-4">Loading visitor badge...</p>;

  return (
    <div className="max-w-xl mx-auto p-4 text-center space-y-4">
      <h1 className="text-2xl font-bold">Visitor Badge</h1>
      <p>
        <strong>Name: </strong>
        {visitor.full_name}
      </p>
      <p>
        <strong>Company: </strong>
        {visitor.company || "N/A"}
      </p>
      {visitor.badge_url ? (
        <img
          src={visitor.badge_url}
          alt="QR Badge"
          className="w-40 mx-auto border p-2"
        />
      ) : (
        <p className="text-red-500">
          Badge not available yet. Please wait for approval.
        </p>
      )}
    </div>
  );
};

export default BadgePage;
