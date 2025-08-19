import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

export default function ProductDetails() {
  const { productId } = useParams();
  const [product, setProduct] = useState(null);
  const [recommendations, setRecommendations] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (productId) {
      // Fetch Product Details
      fetch(`http://127.0.0.1:8000/products/${productId}`)
        .then((res) => res.json())
        .then((data) => setProduct(data))
        .catch((err) => setError(err.message));

      // Fetch Recommendations
      fetch(`http://127.0.0.1:8000/recommendations/${productId}?top_k=4`)
        .then((res) => res.json())
        .then((data) => setRecommendations(data))
        .catch((err) => setError(err.message));
    }
  }, [productId]);

  if (error) return <p className="text-red-500">{error}</p>;
  if (!product) return <p>Loading...</p>;

  return (
    <div className="p-6 bg-gray-900 text-white min-h-screen">
      {/* Product Details */}
      <div className="flex gap-6 items-start">
        <img
          src={product.image}
          alt={product.product_name}
          className="w-48 h-48 object-cover rounded"
        />
        <div>
          <h1 className="text-3xl font-bold">{product.product_name}</h1>
          <p className="text-gray-300 mt-2 max-w-3xl">{product.about_product}</p>
          <p className="text-green-400 mt-3 text-xl font-semibold">₹ {product.price}</p>
        </div>
      </div>

      {/* Recommendations Section */}
      <div className="mt-8">
        <h2 className="text-2xl font-bold mb-2">🔥 Recommended for You</h2>
        <ul className="divide-y divide-gray-800">
          {recommendations.map((rec) => (
            <li key={rec.product_id} className="py-4">
              <Link to={`/product/${rec.product_id}`} className="flex gap-4 items-center">
                <img
                  src={rec.image}
                  alt={rec.product_name}
                  className="w-20 h-20 object-cover rounded"
                />
                <div>
                  <h3 className="text-lg font-semibold">{rec.product_name}</h3>
                  <p className="text-green-400">₹ {rec.price}</p>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
