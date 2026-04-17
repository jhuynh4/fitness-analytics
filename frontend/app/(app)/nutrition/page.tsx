"use client";

export default function NutritionPage() {
  return (
    <div>
      <h1 className="text-3xl font-semibold mb-4">Nutrition</h1>
      <p className="text-gray-600 mb-6">
        Track your daily calories and protein intake.
      </p>

      <div className="rounded-2xl border p-6 shadow-sm bg-white">
        <p className="text-gray-500">
          Nutrition logs will go here (table or list later).
        </p>
      </div>
    </div>
  );
}