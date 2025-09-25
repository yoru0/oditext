// import React from "react";
import { useState, useEffect } from "react";
import { Trash2, AlertTriangle, X } from "lucide-react";

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
        if (!response.ok) throw new Error("Failed to fetch history");
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

  // delete item
  const deleteItem = async (id: number) => {
    if (!window.confirm("Are you sure you want to delete this entry?")) return;

    try {
      const response = await fetch(`http://localhost:8080/api/history/${id}`, {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Delete failed");
      setHistory((prev) => prev.filter((item) => item.id !== id));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to delete item");
    }
  };

  // delete all items
  const deleteAll = async () => {
    if (!window.confirm("Are you sure you want to delete ALL history?")) return;

    try {
      const response = await fetch("http://localhost:8080/api/history/all", {
        method: "DELETE",
      });

      if (!response.ok) throw new Error("Bulk delete failed");
      setHistory([]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to clear history");
    }
  };

  if (loading)
    return <div className="p-4 pl-7 text-gray-600">Loading history...</div>;
  if (error)
    return (
      <div className="bg-red-50 p-4 rounded-lg mb-4 flex items-center gap-2">
        <AlertTriangle className="w-6 h-6 text-red-600" />
        <span className="text-red-700">{error}</span>
      </div>
    );

  return (
    <div>
      <div className="flex justify-between items-center pl-9 pr-4 pt-2 pb-1">
        <h2 className="text-lg font-semibold">
          {history.length} item{history.length !== 1 ? "s" : ""} in history
        </h2>
        <button
          onClick={deleteAll}
          className="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 flex items-center gap-3"
        >
          <Trash2 className="w-5 h-5" />
          Clear All
        </button>
      </div>

      <div className="h-[calc(85vh-10rem)] overflow-y-auto p-4 pt-1">
        <div className="space-y-4">
          {history.map((item) => (
            <div
              key={item.id}
              className="bg-gray-100 p-5 rounded-lg shadow relative group"
            >
              <button
                onClick={() => deleteItem(item.id)}
                className="absolute top-0 right-0 p-6.5"
              >
                <X className="w-5 h-5 text-gray-900 hover:text-gray-600" />
              </button>

              <div className="flex justify-between items-start mb-2 mr-12">
                <span className="text-sm text-gray-500 pt-1.5">
                  {item.timestamp}
                </span>
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
      </div>
    </div>
  );
}
