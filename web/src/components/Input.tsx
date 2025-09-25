import { useState } from "react";

export default function Input() {
  const [text, setText] = useState("");
  const [result, setResult] = useState<{ label: string; confidence: number; prediction: number } | null>(null);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleClassify = async () => {
    if (!text.trim()) return;
    setLoading(true);
    setErrorMsg(null);
    setResult(null);

    try {
      const res = await fetch("http://localhost:8080/api/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text })
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error ?? "Server error");
      }

      setResult({
        label: data.label,
        confidence: data.confidence,
        prediction: data.prediction
      });
    } catch (err: any) {
      setErrorMsg(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="w-full max-w-2xl mx-auto mt-12 p-6 bg-gray-100 rounded-xl shadow-md border border-gray-200">
      <h2 className="text-2xl font-semibold text-gray-800 mb-4 pl-3">
        Mental Health Text Classifier
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
          disabled={loading}
          className="px-7 py-3 text-sm font-medium text-white bg-gray-800 rounded-lg hover:bg-gray-700 transition-colors disabled:opacity-50"
        >
          {loading ? "Classifying…" : "Classify"}
        </button>
      </div>

      {errorMsg && (
        <p className="mt-4 text-red-600 text-center">{errorMsg}</p>
      )}

      {result && !errorMsg && (
        <p
          className={`mt-6 text-lg text-center font-medium ${
            result.prediction === 1 ? "text-red-600" : "text-green-600"
          }`}
        >
          Prediction: {result.label} <br />
          <span className="text-gray-700 text-base">
            (Confidence: {result.confidence}%)
          </span>
        </p>
      )}
    </div>
  );
}
