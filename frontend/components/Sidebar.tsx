"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";

const navItems = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Runs", href: "/runs" },
  { label: "Nutrition", href: "/nutrition" },
  { label: "Weight", href: "/weight" },
  { label: "Settings", href: "/settings" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();

  function handleLogout() {
    localStorage.removeItem("token");
    router.push("/login");
  }

  return (
    <aside className="w-64 min-h-screen border-r bg-white p-4">
      <div className="mb-8">
        <h1 className="text-2xl font-bold">Fitness Analytics</h1>
        <p className="text-sm text-gray-500 mt-1">Track and analyze progress</p>
      </div>

      <nav className="space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`block rounded-lg px-4 py-2 transition ${
                isActive
                  ? "bg-black text-white"
                  : "text-gray-700 hover:bg-gray-100"
              }`}
            >
              {item.label}
            </Link>
          );
        })}
      </nav>

      <button
        onClick={handleLogout}
        className="mt-8 w-full rounded-lg border px-4 py-2 text-left hover:bg-gray-100 transition"
      >
        Log out
      </button>
    </aside>
  );
}