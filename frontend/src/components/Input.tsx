import React, { useState } from "react";

export default function Input() {
  const [text, setText] = useState("");

  const handleClassify = () => {
    // TODO: Handle classification logic here
    console.log("Classifying:", text);
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-12 p-6 bg-gray-100 rounded-xl shadow-md border border-gray-200">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4 pl-3">
        Text Classifier
      </h2>

      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter your text here..."
        className="w-full h-40 pl-5 pt-4 pr-5 pb-4 text-gray-800 bg-white border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-1 focus:ring-gray-200"
      />

      <div className="mt-4 flex justify-end">
        <button
          onClick={handleClassify}
          className="px-7 py-3 text-sm font-medium text-white bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors"
        >
          Classify
        </button>
      </div>
    </div>
  );
}
