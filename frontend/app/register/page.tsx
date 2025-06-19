"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Label } from "@/components/ui/label";
import axios from "axios";
import { toast } from "sonner";

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    full_name: "",
    contact: "",
    company: "",
    purpose: "",
    host_employee_name: "",
    host_department: "",
    photo_base64: "",
  });

  const [photoPreview, setPhotoPreview] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (ev: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [ev.target.name]: ev.target.value });
  };

  const handleImage = (ev: React.ChangeEvent<HTMLInputElement>) => {
    const file = ev.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        const base64 = reader.result as string;
        setFormData({ ...formData, photo_base64: base64 });
        setPhotoPreview(base64);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSubmit = async (ev: React.FormEvent) => {
    ev.preventDefault();
    setLoading(true);
    try {
      const res = await axios.post(
        `${process.env.NEXT_PUBLIC_API_BASE_URL}/visitors/register`,
        formData
      );
      toast.success("Visitor registered successfully.");
    } catch (err: any) {
      toast.error(err.response?.data?.detail || "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto p-4 space-y-4">
      <h1 className="text-2xl font-bold">Visitor Registration</h1>
      <form className="space-y-4" onSubmit={handleSubmit}>
        {[
          "full_name",
          "contact",
          "company",
          "purpose",
          "host_employee_name",
          "host_department",
        ].map((field) => (
          <div key={field}>
            <Label htmlFor={field}>{field.replace(/_/g, " ")}</Label>
            <Input
              id={field}
              name={field}
              value={(formData as any)[field]}
              onChange={handleChange}
              required={field !== "company"}
            />
          </div>
        ))}
        <div>
          <Label htmlFor="photo">Visitor Photo</Label>
          <Input type="file" accept="image/*" onChange={handleImage} required />
          {photoPreview && (
            <img
              src={photoPreview}
              alt="preview"
              className="w-32 h-32 mt-2 rounded border"
            />
          )}
        </div>
        <Button type="submit" disabled={loading}>
          {loading ? "Registering..." : "Submit"}
        </Button>
      </form>
    </div>
  );
};

export default RegisterPage;
