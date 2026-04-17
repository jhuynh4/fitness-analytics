"use client";

import { useRouter } from "next/navigation";

export default function SettingsPage() {
  const router = useRouter();

  function handleLogout() {
    localStorage.removeItem("token");
    router.push("/login");
  }

  return (
    <div>
      <h1 className="text-3xl font-semibold mb-4">Settings</h1>
      <p className="text-gray-600 mb-6">
        Manage your account and preferences.
      </p>

      <div className="space-y-4">
        {/* Account Card */}
        <div className="rounded-2xl border p-6 shadow-sm bg-white">
          <h2 className="text-lg font-semibold mb-2">Account</h2>
          <p className="text-gray-500 mb-4">
            Update your account settings or log out.
          </p>

          <button
            onClick={handleLogout}
            className="px-4 py-2 rounded-lg border hover:bg-gray-100 transition"
          >
            Log out
          </button>
        </div>

        {/* Future Settings Placeholder */}
        <div className="rounded-2xl border p-6 shadow-sm bg-white">
          <h2 className="text-lg font-semibold mb-2">Preferences</h2>
          <p className="text-gray-500">
            Future settings like units (lbs/kg), theme, etc.
          </p>
        </div>
      </div>
    </div>
  );
}