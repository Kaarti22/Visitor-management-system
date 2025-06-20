"use client";

import { useState } from "react";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Button } from "@/components/ui/button";
import axios from "axios";
import { toast } from "sonner";
import { motion } from "framer-motion";
import Image from "next/image";

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
      await axios.post(
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
    <main className="min-h-screen bg-white dark:bg-gray-900 flex flex-col md:flex-row items-center justify-center">
      <motion.div
        className="hidden md:flex w-1/2 items-center justify-center"
        initial={{ opacity: 0, x: -40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
      >
        <Image
          src="/login.jpg"
          alt="Visitor Registration"
          width={500}
          height={400}
          className="rounded-lg"
        />
      </motion.div>

      <motion.div
        className="w-full md:w-1/2 p-8 md:p-12"
        initial={{ opacity: 0, x: 40 }}
        animate={{ opacity: 1, x: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="max-w-md mx-auto space-y-6">
          <h1 className="text-3xl font-bold text-center">
            Visitor Registration
          </h1>

          <form className="space-y-4" onSubmit={handleSubmit}>
            {[
              "full_name",
              "contact",
              "company",
              "purpose",
              "host_employee_name",
              "host_department",
            ].map((field) => (
              <div key={field} className="flex flex-col gap-1">
                <Label htmlFor={field} className="capitalize">
                  {field.replace(/_/g, " ")}
                </Label>
                <Input
                  id={field}
                  name={field}
                  value={(formData as any)[field]}
                  onChange={handleChange}
                  required={field !== "company"}
                />
              </div>
            ))}

            <div className="flex flex-col gap-1">
              <Label htmlFor="photo">Visitor Photo</Label>
              <Input
                type="file"
                accept="image/*"
                className="cursor-pointer"
                onChange={handleImage}
                required
              />
              {photoPreview && (
                <img
                  src={photoPreview}
                  alt="preview"
                  className="w-32 h-32 mt-2 rounded border"
                />
              )}
            </div>

            <Button
              type="submit"
              className="w-full cursor-pointer"
              disabled={loading}
            >
              {loading ? "Registering..." : "Submit"}
            </Button>
          </form>
        </div>
      </motion.div>
    </main>
  );
};

export default RegisterPage;
