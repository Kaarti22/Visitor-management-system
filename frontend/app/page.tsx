"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { Input } from "@/components/ui/input";

export default function HomePage() {
  const [badgeId, setBadgeId] = useState("");
  const [showBadgeInput, setShowBadgeInput] = useState(false);
  const router = useRouter();

  const handleBadgeSubmit = () => {
    if (badgeId) {
      router.push(`/visitor/badge?id=${badgeId}`);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 text-gray-800 dark:text-white">
      <section className="flex flex-col items-center justify-center text-center py-24 px-6">
        <motion.h1
          className="text-5xl md:text-6xl font-bold mb-4"
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          VisitorEase 🚪
        </motion.h1>
        <motion.p
          className="text-lg md:text-xl max-w-2xl mb-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.3, duration: 0.8 }}
        >
          A modern Visitor Management System for offices — secure, paperless,
          and effortless.
        </motion.p>
        <motion.div
          className="flex gap-4 flex-wrap justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6, duration: 0.8 }}
        >
          <Button
            size="lg"
            className="cursor-pointer"
            onClick={() => router.push("/employee/login")}
          >
            Employee Login
          </Button>
          <Button
            variant="outline"
            size="lg"
            className="cursor-pointer"
            onClick={() => setShowBadgeInput(true)}
          >
            View Visitor Badge
          </Button>
          {showBadgeInput && (
            <div className="mt-2 flex flex-col items-center gap-2">
              <Input
                type="number"
                placeholder="Enter your Visitor ID"
                value={badgeId}
                onChange={(e) => setBadgeId(e.target.value)}
                className="w-64"
              />
              <Button
                className="cursor-pointer"
                onClick={handleBadgeSubmit}
                disabled={!badgeId}
              >
                View Badge
              </Button>
            </div>
          )}
          <Button
            variant="ghost"
            size="lg"
            className="cursor-pointer"
            onClick={() => router.push("/visitor/register")}
          >
            Register as Visitor
          </Button>
        </motion.div>
      </section>

      <section className="bg-white dark:bg-gray-900 py-20 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <h2 className="text-3xl font-semibold mb-6">Why VisitorEase?</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mt-10">
            {[
              {
                title: "Instant Visitor Check-in",
                desc: "Register visitors in seconds with photo upload and approval routing.",
              },
              {
                title: "Pre-Approvals by Employees",
                desc: "Allow hosts to pre-approve expected visitors securely.",
              },
              {
                title: "QR Badge Generation",
                desc: "Generate and view digital QR badges — no printing required.",
              },
            ].map((item, idx) => (
              <motion.div
                key={idx}
                className="bg-blue-100 dark:bg-gray-800 rounded-xl p-6 shadow-md"
                whileHover={{ scale: 1.03 }}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.2, duration: 0.6 }}
              >
                <h3 className="text-xl font-semibold mb-2">{item.title}</h3>
                <p className="text-gray-700 dark:text-gray-300">{item.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      <section className="py-20 px-6 bg-gradient-to-br from-blue-100 to-indigo-200 dark:from-gray-800 dark:to-gray-700">
        <div className="max-w-4xl mx-auto text-center">
          <h2 className="text-3xl font-bold mb-4">About This Project</h2>
          <p className="text-lg text-gray-700 dark:text-gray-300">
            This Visitor Management System was built as part of an engineering
            project to improve entry security and digitize the visitor
            registration process. It combines modern frontend technologies
            (Next.js, ShadCN UI), a secure Python backend (FastAPI), and cloud
            tools (NeonDB, Cloudinary).
          </p>
        </div>
      </section>

      <footer className="text-center py-6 text-sm text-gray-500 dark:text-gray-400 border-t border-gray-300 dark:border-gray-700">
        Built with ❤️ by Mondi Venkata Kartikeya · FastAPI · Next.js · Tailwind
        · PostgreSQL · Cloudinary
      </footer>
    </main>
  );
}
