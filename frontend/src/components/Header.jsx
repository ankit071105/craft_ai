import React from "react";
import { Link } from "react-router-dom";

export default function Header() {
  return (
    <header className="sticky top-0 z-10 bg-white/80 backdrop-blur border-b">
      <div className="max-w-6xl mx-auto px-4 py-3 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold">CraftOracle</Link>
        <nav className="text-sm text-slate-600">Hyper‑local crafts marketplace</nav>
      </div>
    </header>
  );
}
