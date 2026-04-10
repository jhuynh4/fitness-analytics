import Link from "next/link";

export default function HomePage() {
  return (
    <main className="min-h-screen flex items-center justify-center p-6">
      <div className="text-center space-y-4">
        <h1 className="text-3xl font-semibold">Fitness Analytics Platform</h1>
        <p className="text-sm text-gray-600">
          Track runs, nutrition, and weight with analytics dashboards.
        </p>
        <Link
          href="/login"
          className="inline-block rounded-lg border px-4 py-2 font-medium"
        >
          Go to Login
        </Link>
      </div>
    </main>
  );
}