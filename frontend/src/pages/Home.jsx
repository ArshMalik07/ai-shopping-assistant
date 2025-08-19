import { useEffect, useState } from "react";
import { ShoppingCart, Bot, Search, Heart, Zap } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function Home() {
  const [message, setMessage] = useState("...");
  const [error, setError] = useState(null);
  const [searchQuery, setSearchQuery] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    fetch("http://127.0.0.1:8000/")
      .then((res) => {
        if (!res.ok) throw new Error("Network response was not ok");
        return res.json();
      })
      .then((data) => setMessage(data.message ?? JSON.stringify(data)))
      .catch((err) => setError(err.message));
  }, []);

  const handleSearch = () => {
    if (searchQuery.trim()) {
      navigate(`/search?query=${encodeURIComponent(searchQuery)}`);
    }
  };

  const features = [
    {
      icon: <Bot className="w-8 h-8 text-indigo-400" />,
      title: "AI-Powered Chat",
      description: "Ask anything about products and get accurate answers using AI.",
    },
    {
      icon: <Search className="w-8 h-8 text-pink-400" />,
      title: "Smart Search",
      description: "Find products instantly with semantic & vector-based search.",
    },
    {
      icon: <Zap className="w-8 h-8 text-green-400" />,
      title: "Recommendations",
      description: "Get AI-powered product recommendations tailored for you.",
    },
  ];

  return (
    <section className="min-h-screen bg-gradient-to-br from-gray-900 via-black to-gray-900 text-white p-8 space-y-12">
      {/* Hero Section */}
      <div className="relative p-2">
        <h1 className="text-5xl font-extrabold">
          AI Shopping Assistant
        </h1>
        <p className="mt-2 text-lg text-gray-300 max-w-3xl">
          Your personal AI-powered shopping partner — Search, Chat, and Shop
          smarter with seamless recommendations and intelligent product
          insights.
        </p>

        {/* Search Box */}
        <div className="flex flex-wrap gap-3 mt-6">
          <input
            type="text"
            placeholder="Search for a product..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="flex-1 p-3 bg-gray-800 border-b border-gray-700 text-white focus:outline-none focus:border-indigo-500"
          />
          <button
            onClick={handleSearch}
            className="px-6 py-3 bg-indigo-600 text-white font-semibold hover:opacity-90 transition"
          >
            Search
          </button>
        </div>

        {/* CTA Buttons */}
        <div className="flex flex-wrap gap-4 mt-6">
          <button
            onClick={() => navigate("/chat")}
            className="px-6 py-3 bg-blue-600 text-white font-semibold hover:opacity-90 transition"
          >
            Get Started →
          </button>
        </div>
      </div>

      {/* Backend Status */}
      <div className="py-4 border-t border-b border-gray-800">
        <h2 className="text-2xl font-bold mb-1">Backend Status</h2>
        <p className={error ? "text-red-400" : "text-green-400"}>
          {error ? ` Error: ${error}` : ` Backend says: ${message}`}
        </p>
      </div>

      {/* Features */}
      <div>
        <h2 className="text-3xl font-bold mb-4 text-indigo-400"> Key Features</h2>
        <ul className="divide-y divide-gray-800">
          {features.map((feature, index) => (
            <li key={index} className="py-4 flex gap-4 items-start">
              <div className="mt-1">{feature.icon}</div>
              <div>
                <h3 className="text-xl font-semibold mb-1">{feature.title}</h3>
                <p className="text-gray-400 text-sm">{feature.description}</p>
              </div>
            </li>
          ))}
        </ul>
      </div>

      {/* How Recommendations Work */}
      <div className="py-4 border-t border-b border-gray-800">
        <h2 className="text-2xl font-bold text-green-400 mb-1">💡 How AI Recommendations Work</h2>
        <p className="text-gray-300 text-sm">
          When you view a product, our AI analyzes its features, description, and category.
          Using semantic similarity search with vector embeddings, it finds the most relevant
          products that match your preferences and needs.
        </p>
      </div>

      {/* Footer */}
      <footer className="pt-10 text-center text-gray-500 text-sm">
        © {new Date().getFullYear()} AI Shopping Assistant. All rights reserved.
      </footer>
    </section>
  );
}
