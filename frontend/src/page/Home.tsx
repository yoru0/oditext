// import React from "react";
import Sidebar from "../components/Navbar";
import Input from "../components/Input";

export default function Homepage() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      <Sidebar />
      <main className="flex-1 m-5 p-4 sm:p-6 md:p-8 lg:p-10 xl:p-12 bg-gray-100 rounded-2xl shadow-xl border border-gray-200 flex items-center justify-center">
        <div className="w-full max-w-3xl -mt-15">
          <h1 className="text-3xl font-bold text-gray-800 mb-8 text-center">
            Welcome to Odi Text Classifier
          </h1>
          <Input />
        </div>
      </main>
    </div>
  );
}
