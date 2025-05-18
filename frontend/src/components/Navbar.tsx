// import React from 'react';
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-white shadow-md fixed top-0 left-0 w-full z-10">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Company Name */}
          <div className="text-xl font-bold text-blue-600">Hewwo</div>

          {/* Navigation Links */}
          <div className="space-x-6">
            <Link
              to="/home"
              className="text-gray-700 hover:text-blue-500 font-medium"
            >
              Home
            </Link>
            <Link
              to="/history"
              className="text-gray-700 hover:text-blue-500 font-medium"
            >
              History
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
