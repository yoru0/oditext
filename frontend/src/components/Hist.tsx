// import React from "react";
import { useState, useEffect } from "react";
// import { useNavigate } from "react-router-dom";

interface HistoryItem {
  id: number;
  text: string;
  prediction: string;
  label: string;
  confidence: number;
  timestamp: string;
}

export default function Hist() {
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await fetch("http://localhost:8080/api/history");
        if (!response.ok) {
          throw new Error("Failed to fetch history");
        }
        const data: HistoryItem[] = await response.json();
        setHistory(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Unknown error occurred");
      } finally {
        setLoading(false);
      }
    };
    fetchHistory();
  }, []);

  if (loading)
    return <div className="p-4 text-gray-600">Loading history...</div>;
  if (error) return <div className="p-4 text-red-500">Error: {error}</div>;

  return (
    <div className="h-[calc(90vh-10rem)] overflow-y-auto space-y-4 p-4">
      {history.map((item) => (
        <div key={item.id} className="bg-gray-100 p-4 rounded-lg shadow">
          <div className="flex justify-between items-start mb-2">
            <span className="text-sm text-gray-500">{item.timestamp}</span>
            <span
              className={`px-2 py-1 rounded ${
                Number(item.prediction) === 0
                  ? "bg-green-100 text-green-800"
                  : "bg-red-100 text-red-800"
              }`}
            >
              {item.label} ({item.confidence.toFixed(2)})
            </span>
          </div>
          <p className="text-gray-800">{item.text}</p>
        </div>
      ))}
    </div>
  );
}
