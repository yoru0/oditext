import { Home, History } from "lucide-react";
import { NavLink, Link } from "react-router-dom";

const navItems = [
  { label: "Home", icon: Home, to: "/home" },
  { label: "History", icon: History, to: "/history" },
];

export default function Sidebar() {
  return (
    <aside className="w-64 ml-5 mt-5 mb-5 bg-gray-100 text-gray-800 rounded-2xl shadow-xl border border-gray-200 flex flex-col p-6">
      {/* Logo */}
      <div className="mb-10 pl-5 mt-3">
        <Link
          to="/home"
          className="relative inline-block text-3xl font-semibold tracking-wide text-gray-900 hover:text-black transition-colors duration-300 group"
        >
          Odi
          <span className="absolute left-0 -bottom-1 h-0.5 w-0 bg-gray-800 transition-all duration-300 group-hover:w-full"></span>
        </Link>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-3">
        {navItems.map(({ label, icon: Icon, to }) => (
          <NavLink
            key={label}
            to={to}
            className={({ isActive }) =>
              `flex items-center gap-4 px-5 py-3 rounded-lg transition-all duration-200
              ${
                isActive
                  ? "bg-gray-300 text-black font-semibold"
                  : "text-gray-700 hover:bg-gray-200"
              }`
            }
          >
            <Icon size={18} />
            <span>{label}</span>
          </NavLink>
        ))}
      </nav>

      {/* Toggle Button */}
      <div className="mt-auto flex justify-end">
        <button
          // onClick={toggleSidebar}
          className="text-sm text-gray-600 hover:text-black transition-colors"
        >
          {/* {isCollapsed ? ">>" : "<<"} */}
        </button>
      </div>
    </aside>
  );
}
