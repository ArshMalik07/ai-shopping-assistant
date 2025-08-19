import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import Home from './pages/Home.jsx'
import Chat from './pages/Chat.jsx'
import Products from './pages/Products.jsx'
import ProductDetails from './pages/productDetails.jsx'
import Search from "./pages/Search.jsx";




export default function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900">
      <Navbar />
      <main className="max-w-6xl mx-auto p-6">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chat" element={<Chat />} />
          <Route path="/products" element={<Products />} />
           <Route path="/product/:productId" element={<ProductDetails />} />
           <Route path="/search" element={<Search />} />

        </Routes>
      </main>
    </div>
  )
}
