import React, { useState } from "react";

export default function Chat() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]); // {role: 'user'|'ai', text: string, sources?: []}
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
    setSources([]);

    // Add user message to chat history
    setMessages((prev) => [...prev, { role: "user", text: question }]);
    const userQuestion = question;
    setQuestion("");

    try {
      const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: userQuestion }),
      });

      if (!res.ok) {
        throw new Error(`Server error: ${res.status}`);
      }

      const data = await res.json();
      console.log("Backend response:", data);

      setMessages((prev) => [
        ...prev,
        { role: "ai", text: data.data.answer, sources: data.data.sources }
      ]);
      setSources(data.data.sources);
    } catch (err) {
      setError("Failed to get response from server.");
      setMessages((prev) => [
        ...prev,
        { role: "ai", text: "[Error: Failed to get response from server.]" }
      ]);
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
          placeholder="How can I help you today?"
          disabled={loading}
          className="flex-1 p-3 bg-gray-800 border-b border-gray-700 text-gray-100 focus:outline-none"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="bg-blue-600 hover:bg-blue-500 transition-colors duration-300 px-6 py-3 text-white disabled:opacity-50"
        >
          Send
        </button>
      </div>

      {error && (
        <p className="text-red-500 mb-4 mt-2 animate-pulse">{error}</p>
      )}

      <div className="w-full max-w-3xl flex flex-col gap-2 mb-4">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`px-4 py-2 max-w-[80%] ${
                msg.role === "user"
                  ? "bg-blue-600 text-white self-end"
                  : "bg-gray-800 text-gray-100 self-start"
              } animate-fadeIn`}
            >
              {msg.text}
              {/* Show sources for AI message if present */}
              {/* {msg.role === "ai" && msg.sources && msg.sources.length > 0 && (
                <div className="mt-2">
                  <h2 className="font-semibold mb-1 text-blue-300">Sources:</h2>
                  <ul className="list-disc list-inside space-y-1">
                    {msg.sources.map((src, sidx) => (
                      <li key={sidx}>
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
              )} */}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-gray-800 text-gray-400 px-4 py-2 max-w-[80%] animate-pulse">
              AI is typing...
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
