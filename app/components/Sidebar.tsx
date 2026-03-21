"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { label: "Home", href: "/", icon: "⚽" },
  { label: "Match List", href: "/matches", icon: "📋" },
  { label: "Winners List", href: "/winners", icon: "🏆" },
];

export default function Sidebar() {
  const pathname = usePathname();

  return (
    <aside
      style={{ backgroundColor: "#2C3E6B" }}
      className="fixed top-0 left-0 h-screen w-64 flex flex-col z-50"
    >
      {/* Branding */}
      <div
        className="px-6 py-8"
        style={{ borderBottom: "1px solid rgba(74,111,165,0.4)" }}
      >
        <h1
          className="text-xl font-bold leading-tight tracking-wide"
          style={{ color: "#FFFFFF" }}
        >
          Unofficial Football
          <br />
          Club World
          <br />
          Championship
        </h1>
        <div
          className="mt-3 h-0.5 w-12 rounded-full"
          style={{ backgroundColor: "#F0C34E" }}
        />
      </div>

      {/* Navigation */}
      <nav className="flex-1 flex flex-col gap-1 px-3 py-6">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              className="flex items-center gap-3 px-4 py-3 rounded-lg text-base font-medium transition-all duration-200 no-underline"
              style={{
                color: isActive ? "#FFFFFF" : "rgba(255,255,255,0.8)",
                backgroundColor: isActive
                  ? "#1A2A4A"
                  : "transparent",
                boxShadow: isActive
                  ? "0 4px 6px rgba(0,0,0,0.2)"
                  : "none",
              }}
              onMouseEnter={(e) => {
                if (!isActive) {
                  e.currentTarget.style.backgroundColor =
                    "rgba(74,111,165,0.3)";
                  e.currentTarget.style.color = "#FFFFFF";
                }
              }}
              onMouseLeave={(e) => {
                if (!isActive) {
                  e.currentTarget.style.backgroundColor = "transparent";
                  e.currentTarget.style.color = "rgba(255,255,255,0.8)";
                }
              }}
            >
              <span className="text-lg">{item.icon}</span>
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div
        className="px-6 py-4"
        style={{ borderTop: "1px solid rgba(74,111,165,0.4)" }}
      >
        <p
          className="text-xs text-center"
          style={{ color: "rgba(255,255,255,0.5)" }}
        >
          UFCC © 2025/26
        </p>
      </div>
    </aside>
  );
}
