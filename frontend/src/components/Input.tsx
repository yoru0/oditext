import React, { useState } from "react";

export default function Input() {
  const [text,   setText]   = useState("");
  const [result, setResult] = useState<string | null>(null);
  const [error,  setError]  = useState<string | null>(null);
  const [busy,   setBusy]   = useState(false);

  const classify = async () => {
    if (!text.trim()) return;
    setBusy(true);  setError(null);  setResult(null);

    try {
      const res = await fetch("http://localhost:8080/api/predict", {
        method : "POST",
        headers: { "Content-Type": "application/json" },
        body   : JSON.stringify({ text })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Server error");

      setResult(data.prediction ?? "No prediction");
    } catch (err: any) {
      setError(err.message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-12 p-6 bg-gray-100 rounded-xl shadow-md border border-gray-200">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4 pl-3">
        Text Classifier
      </h2>

      <textarea
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Enter your text here..."
        className="w-full h-40 pl-5 pt-4 pr-5 pb-4 text-gray-800 bg-white border border-gray-300 rounded-lg resize-none focus:outline-none focus:ring-1 focus:ring-gray-200"
      />

      <div className="mt-4 flex justify-end">
        <button
          onClick={classify}
          disabled={busy}
          className="px-7 py-3 text-sm font-medium text-white bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors disabled:opacity-50"
        >
          {busy ? "Classifying…" : "Classify"}
        </button>
      </div>

      {error  && <p className="mt-4 text-red-600 text-center">{error}</p>}
      {result && !error && (
        <p className="mt-6 text-lg text-center">
          <span className="font-semibold">Prediction:</span> {result}
        </p>
      )}
    </div>
  );
}
