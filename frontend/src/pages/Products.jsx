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
      <ul className="divide-y divide-gray-800">
        {products.map((product) => (
          <li key={product.id} className="py-4 flex items-center gap-4">
            <img src={product.image} alt={product.name} className="w-20 h-20 object-cover rounded" />
            <a href={product.link} className="flex-1">
              <h2 className="font-semibold text-lg">{product.name}</h2>
              <p className="text-blue-400 font-bold">{product.price}</p>
            </a>
          </li>
        ))}
      </ul>
    </div>
  );
}
