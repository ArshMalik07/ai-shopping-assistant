import React, { useState } from "react";

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const sendMessage = async () => {
    if (!question.trim()) {
      setError("Please enter a question.");
      return;
    }
    setError("");
    setLoading(true);
    setResponse("");
    setSources([]);

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: question }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      console.log("Backend response:", data);

      setResponse(data.data.answer);
      setSources(data.data.sources);
    } catch (err) {
      setError("Failed to get response from server.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 flex flex-col items-center p-6">
      <h1 className="text-4xl font-bold mb-6 animate-pulse text-blue-400">
        AI Shopping Assistant
      </h1>

      <div className="flex gap-2 w-full max-w-3xl mb-4">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask me anything..."
          disabled={loading}
          className="flex-1 p-3 rounded-lg bg-gray-800 border border-gray-700 text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-all duration-300"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 transition-colors duration-300 px-6 py-3 rounded-lg shadow-md text-white disabled:opacity-50"
        >
          Send
        </button>
      </div>

      {loading && (
        <p className="text-gray-400 animate-pulse mt-2">Loading...</p>
      )}

      {error && (
        <p className="text-red-500 mb-4 mt-2 animate-pulse">{error}</p>
      )}

      {response && (
        <div className="bg-gray-800 p-4 rounded-lg shadow-lg mb-4 w-full max-w-3xl animate-fadeIn">
          <h2 className="font-semibold mb-2 text-blue-300">AI Response:</h2>
          <p>{response}</p>
        </div>
      )}

      {sources.length > 0 && (
        <div className="bg-gray-800 p-4 rounded-lg shadow-lg w-full max-w-3xl animate-fadeIn">
          <h2 className="font-semibold mb-2 text-blue-300">Sources:</h2>
          <ul className="list-disc list-inside space-y-1">
            {sources.map((src, idx) => (
              <li key={idx}>
                <a
                  href={src.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 hover:underline transition-colors duration-200"
                >
                  {src.title || src.url}
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}
