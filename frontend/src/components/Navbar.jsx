import { Link, NavLink } from 'react-router-dom'

export default function Navbar() {
  const linkClass = ({ isActive }) =>
    `px-1 py-2 ${isActive ? 'text-gray-900 border-b-2 border-gray-900' : 'text-gray-700 hover:text-gray-900'}`

  return (
    <nav className="bg-white">
      <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <Link to="/" className="text-xl font-bold">AI Shopping Assistant</Link>
        <div className="flex items-center gap-6">
          <NavLink to="/" className={linkClass} end>Home</NavLink>
          <NavLink to="/chat" className={linkClass}>Chat</NavLink>
          <NavLink to="/search" className={linkClass}>Search</NavLink>
        </div>
      </div>
    </nav>
  )
}
