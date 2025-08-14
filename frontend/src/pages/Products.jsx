import React from "react";

const products = [
  {
    id: 1,
    name: "Wireless Headphones",
    price: "$99",
    image:
      "https://images.unsplash.com/photo-1511367461989-f85a21fda167?auto=format&fit=crop&w=400&q=80",
    link: "#",
  },
  {
    id: 2,
    name: "Smart Watch",
    price: "$199",
    image:
      "https://images.unsplash.com/photo-1603791440384-56cd371ee9a7?auto=format&fit=crop&w=400&q=80",
    link: "#",
  },
  {
    id: 3,
    name: "Portable Speaker",
    price: "$49",
    image:
      "https://images.unsplash.com/photo-1585386959984-a415522d43b2?auto=format&fit=crop&w=400&q=80",
    link: "#",
  },
];

export default function Products() {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 p-6">
      <h1 className="text-3xl font-bold mb-6 text-blue-400 text-center">
        Products
      </h1>
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {products.map((product) => (
          <a
            key={product.id}
            href={product.link}
            className="bg-gray-800 rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300"
          >
            <img
              src={product.image}
              alt={product.name}
              className="w-full h-48 object-cover"
            />
            <div className="p-4">
              <h2 className="font-semibold text-lg mb-2">{product.name}</h2>
              <p className="text-blue-400 font-bold">{product.price}</p>
            </div>
          </a>
        ))}
      </div>
    </div>
  );
}
