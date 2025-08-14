import { Link, NavLink } from 'react-router-dom'

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `px-3 py-2 rounded-xl ${isActive ? 'bg-gray-900 text-white' : 'text-gray-700 hover:bg-gray-200'}`

  return (
    <nav className="bg-white shadow-sm">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold">AI Shopping Assistant</Link>
        <div className="flex items-center gap-2">
          <NavLink to="/" className={linkClass} end>Home</NavLink>
          <NavLink to="/chat" className={linkClass}>Chat</NavLink>
          <NavLink to="/products" className={linkClass}>Products</NavLink>
        </div>
      </div>
    </nav>
  )
}
