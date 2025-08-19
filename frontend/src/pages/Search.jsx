import { useState, useEffect } from "react";

export default function Search() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [suggestions, setSuggestions] = useState([]);
  const [allProductNames, setAllProductNames] = useState([]);
  const [category, setCategory] = useState("");
  const [minPrice, setMinPrice] = useState("");
  const [maxPrice, setMaxPrice] = useState("");
  const [allCategories, setAllCategories] = useState([]);
  const [queryRecommendations, setQueryRecommendations] = useState([]);

  useEffect(() => {
    // Fetch all product names and categories for suggestions/filters (once)
    fetch("http://127.0.0.1:8000/products")
      .then((res) => res.json())
      .then((data) => {
        if (data.data) {
          setAllProductNames(data.data.map((p) => p.product_name));
          // Extract unique categories
          const cats = Array.from(new Set(data.data.map((p) => p.category).filter(Boolean)));
          setAllCategories(cats);
        }
      });
  }, []);

  useEffect(() => {
    // Update suggestions as user types
    if (query.length > 0 && allProductNames.length > 0) {
      const q = query.toLowerCase();
      setSuggestions(
        allProductNames.filter((name) =>
          name.toLowerCase().includes(q)
        ).slice(0, 5)
      );
    } else {
      setSuggestions([]);
    }
  }, [query, allProductNames]);

  const handleSearch = async (q = query) => {
    if (!q.trim()) return;
    setLoading(true);
    setError("");
    let url = `http://127.0.0.1:8000/search?query=${encodeURIComponent(q)}&top_k=5`;
    if (category) url += `&category=${encodeURIComponent(category)}`;
    if (minPrice) url += `&min_price=${minPrice}`;
    if (maxPrice) url += `&max_price=${maxPrice}`;

    try {
      // 1️⃣ Search products
      const res = await fetch(url, { method: "POST" });
      const data = await res.json();
      console.log("Backend response:", data);

      setResults(data.products || []); // ✅ fix: data.products use karo
      if ((!data.products || data.products.length === 0) && data.suggestions && data.suggestions.length > 0) {
        setError("");
      } else if (!data.products || data.products.length === 0) {
        setError("No products found.");
      }
      setBackendSuggestions(data.suggestions || []);

      // 2️⃣ Query-based recommendations (related to the search query)
      try {
        const qRecRes = await fetch(`http://127.0.0.1:8000/recommendations/by-query?query=${encodeURIComponent(q)}&top_k=6`);
        const qRecData = await qRecRes.json();
        setQueryRecommendations(qRecData.data || qRecData.products || []);
      } catch (e) {
        // ignore silently
      }

      // 3️⃣ Fetch product-based recommendations for first product (if exists)
      if (data.products && data.products.length > 0) {
        const firstProductId = data.products[0].product_id;
        const recRes = await fetch(
          `http://127.0.0.1:8000/recommendations/${firstProductId}?top_k=4`
        );
        const recData = await recRes.json();
        setRecommendations(recData.products || recData.data || []);
      } else {
        setRecommendations([]);
      }
    } catch (err) {
      setError("Failed to fetch search results.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  // Helper to highlight query in product name
  const highlight = (text, q) => {
    if (!q) return text;
    const idx = text.toLowerCase().indexOf(q.toLowerCase());
    if (idx === -1) return text;
    return (
      <>
        {text.slice(0, idx)}
        <span className="bg-yellow-300 text-black rounded px-1">{text.slice(idx, idx + q.length)}</span>
        {text.slice(idx + q.length)}
      </>
    );
  };

  // Add state for backend suggestions
  const [backendSuggestions, setBackendSuggestions] = useState([]);
 
  // Decide placement for query-based recommendations
  const showQueryRecommendationsAbove = query && queryRecommendations.length > 0 && results.length < 3;
 
  // Helper renderer for query-based recommendations
  const renderQueryRecommendations = () => (
    <div className="mt-10">
      <h2 className="text-xl font-semibold mb-1">🔗 Related to your search</h2>
      {showQueryRecommendationsAbove && results.length > 0 && (
        <p className="text-gray-400 mb-2 text-sm">Showing because we found few exact matches.</p>
      )}
      <ul className="divide-y divide-gray-800">
        {queryRecommendations.map((product) => (
          <li key={product.product_id} className="py-4 flex gap-4 items-start">
            <img
              src={product.img_link}
              alt={product.product_name}
              className="w-20 h-20 object-cover rounded"
            />
            <div>
              <h3 className="text-lg font-semibold">{product.product_name}</h3>
              <p className="text-gray-400 text-sm line-clamp-3">{product.about_product}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );

  return (
    <section className="min-h-screen bg-gray-900 text-white p-8">
      <h1 className="text-3xl font-bold mb-6">Smart Search</h1>

      {/* Search Bar */}
      <div className="flex gap-2 mb-6 relative">
        <input
          type="text"
          placeholder="Search for a product..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter") handleSearch();
          }}
          className="flex-1 p-3 rounded-lg bg-gray-800 border border-gray-700 text-white"
        />
        <button
          onClick={() => handleSearch()}
          className="px-6 py-3 bg-indigo-600 hover:bg-indigo-700 rounded-lg font-semibold"
        >
          Search
        </button>
        {/* Suggestions dropdown */}
        {suggestions.length > 0 && (
          <ul className="absolute left-0 top-full mt-1 w-full bg-gray-800 border border-gray-700 rounded-lg z-10">
            {suggestions.map((s, i) => (
              <li
                key={i}
                className="px-4 py-2 hover:bg-indigo-600 cursor-pointer"
                onClick={() => {
                  setQuery(s);
                  setSuggestions([]);
                  handleSearch(s);
                }}
              >
                {highlight(s, query)}
              </li>
            ))}
          </ul>
        )}
      </div>
      {/* Error message */}
      {error && <p className="text-red-400 mb-2">{error}</p>}

 
      {/* Query-based Recommendations (above) */}
      {showQueryRecommendationsAbove && renderQueryRecommendations()}
 
      {/* Search Results */}
      {loading ? (
        <p className="text-gray-400">Searching...</p>
      ) : results.length > 0 ? (
        <div className="mb-10">
          <h2 className="text-xl font-semibold mb-3">Search Results</h2>
          <ul className="divide-y divide-gray-800">
            {results.map((product) => (
              <li key={product.product_id} className="py-4 flex gap-4 items-start">
                <img
                  src={product.img_link}
                  alt={product.product_name}
                  className="w-20 h-20 object-cover rounded"
                />
                <div>
                  <h3 className="text-lg font-semibold">{highlight(product.product_name, query)}</h3>
                  <p className="text-gray-400 text-sm line-clamp-3">{product.about_product}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      ) : (
        query && <p className="text-gray-400">No products found.</p>
      )}
 
      {/* Backend Suggestions if no results */}
      {backendSuggestions.length > 0 && results.length === 0 && (
        <div className="mb-6">
          <h3 className="text-lg text-yellow-300 font-semibold mb-2">Did you mean:</h3>
          <ul className="flex gap-2 flex-wrap">
            {backendSuggestions.map((s, i) => (
              <li key={i}>
                <button
                  className="bg-gray-700 hover:bg-indigo-600 text-white px-3 py-1 rounded"
                  onClick={() => { setQuery(s); handleSearch(s); }}
                >
                  {s}
                </button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {/* Query-based Recommendations (below) */}
      {!showQueryRecommendationsAbove && query && queryRecommendations.length > 0 && renderQueryRecommendations()}

      {/* Recommendations */}
      {recommendations.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-3"> AI Recommendations</h2>
          <ul className="divide-y divide-gray-800">
            {recommendations.map((product) => (
              <li key={product.product_id} className="py-4 flex gap-4 items-start">
                <img
                  src={product.img_link}
                  alt={product.product_name}
                  className="w-20 h-20 object-cover rounded"
                />
                <div>
                  <h3 className="text-lg font-semibold">{product.product_name}</h3>
                  <p className="text-gray-400 text-sm line-clamp-3">{product.about_product}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
