"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import SummaryCard from "@/components/SummaryCard";
import TrendChart from "@/components/TrendChart";
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

type TrendsResponse = {
  run_miles_by_date: { date: string; miles: number }[];
  nutrition_by_date: { date: string; calories: number; protein_g: number }[];
  weight_by_date: { date: string; weight_lbs: number }[];
};

export default function DashboardPage() {
  const router = useRouter();
  const [summary, setSummary] = useState<SummaryResponse | null>(null);
  const [trends, setTrends] = useState<TrendsResponse | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    async function loadDashboard() {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          router.push("/login");
          return;
        }

        const [summaryData, trendsData] = await Promise.all([
          apiFetch<SummaryResponse>("/analytics/summary"),
          apiFetch<TrendsResponse>("/analytics/trends"),
        ]);

        setSummary(summaryData);
        setTrends(trendsData);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load dashboard");
      }
    }

    loadDashboard();
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
            <SummaryCard title="Total Miles" value={`${summary.total_miles} mi`} />
            <SummaryCard
              title="Avg Calories (7d)"
              value={`${summary.avg_calories_7d} kcal`}
            />
            <SummaryCard
              title="Latest Weight"
              value={summary.latest_weight !== null ? `${summary.latest_weight} lbs` : "N/A"}
            />
            <SummaryCard
              title="Runs Last 7 Days"
              value={summary.runs_last_7_days}
            />
            <SummaryCard
              title="Miles Last 7 Days"
              value={`${summary.miles_last_7_days} mi`}
            />
            <SummaryCard
              title="Avg Protein (7d)"
              value={`${summary.avg_protein_7d} g`}
            />
            <SummaryCard
              title="Avg Weight (7d)"
              value={`${summary.avg_weight_7d} lbs`}
            />
          </div>
        )}

        {!trends ? null : (
          <div className="grid gap-6 lg:grid-cols-1">
            <TrendChart
              title="Run Miles by Date"
              data={trends.run_miles_by_date}
              dataKey="miles"
            />
            <TrendChart
              title="Calories by Date"
              data={trends.nutrition_by_date}
              dataKey="calories"
            />
            <TrendChart
              title="Weight by Date"
              data={trends.weight_by_date}
              dataKey="weight_lbs"
            />
          </div>
        )}
      </div>
    </main>
  );
}