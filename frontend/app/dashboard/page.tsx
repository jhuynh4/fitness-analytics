"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import SummaryCard from "@/components/SummaryCard";
import { apiFetch } from "@/lib/api";

type SummaryResponse = {
  total_runs: number;
  total_miles: number;
  runs_last_7_days: number;
  miles_last_7_days: number;
  avg_pace_seconds_per_mile: number;
  avg_calories_7d: number;
  avg_protein_7d: number;
  latest_weight: number | null;
  avg_weight_7d: number;
};

export default function DashboardPage() {
  const router = useRouter();
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadSummary() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          router.push("/login");
          return;
        }

        const data = await apiFetch<SummaryResponse>("/analytics/summary");
        setSummary(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load dashboard");
      }
    }

    loadSummary();
  }, [router]);

  function handleLogout() {
    localStorage.removeItem("token");
    router.push("/login");
  }

  return (
    <main className="min-h-screen p-6">
      <div className="max-w-6xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
          <h1 className="text-3xl font-semibold">Dashboard</h1>
          <button
            onClick={handleLogout}
            className="rounded-lg border px-4 py-2"
          >
            Log out
          </button>
        </div>

        {error ? (
          <div className="rounded-lg border border-red-300 p-4 text-red-600">
            {error}
          </div>
        ) : null}

        {!summary ? (
          <p>Loading...</p>
        ) : (
          <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <SummaryCard title="Total Runs" value={summary.total_runs} />
            <SummaryCard title="Total Miles" value={summary.total_miles} />
            <SummaryCard title="Avg Calories (7d)" value={summary.avg_calories_7d} />
            <SummaryCard
              title="Latest Weight"
              value={summary.latest_weight ?? "N/A"}
            />
            <SummaryCard
              title="Runs Last 7 Days"
              value={summary.runs_last_7_days}
            />
            <SummaryCard
              title="Miles Last 7 Days"
              value={summary.miles_last_7_days}
            />
            <SummaryCard
              title="Avg Protein (7d)"
              value={summary.avg_protein_7d}
            />
            <SummaryCard
              title="Avg Weight (7d)"
              value={summary.avg_weight_7d}
            />
          </div>
        )}
      </div>
    </main>
  );
}