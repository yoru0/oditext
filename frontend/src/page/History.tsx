// import React from "react";
import Navbar from "../components/Navbar";
import Hist from "../components/Hist";

export default function HistoryPage() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Navbar />
      <main className="flex-1 m-5 p-4 sm:p-6 md:p-8 lg:p-10 xl:p-12 bg-gray-100 rounded-2xl shadow-xl border border-gray-200">
        <div>
          <h1 className="text-3xl font-bold text-gray-800 mb-6 text-center">
            Text History
          </h1>
          <div className="bg-gray-500 h-0.5 ml-4 mr-4"></div>
          <Hist />
        </div>
      </main>
    </div>
  );
}
