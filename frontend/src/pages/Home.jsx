import { useEffect, useState } from 'react'

export default function Home() {
  const [message, setMessage] = useState('...')
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch('http://127.0.0.1:8000/')
      .then((res) => {
        if (!res.ok) throw new Error('Network response was not ok')
        return res.json()
      })
      .then((data) => setMessage(data.message ?? JSON.stringify(data)))
      .catch((err) => setError(err.message))
  }, [])

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-semibold">Welcome 👋</h1>
      <p className="text-gray-700">
        This is a starter React + Vite + Tailwind app wired to your FastAPI backend.
      </p>
      <div className="p-4 rounded-2xl bg-white shadow-sm">
        <h2 className="text-lg font-medium mb-2">Backend check</h2>
        {error ? (
          <p className="text-red-600">Error: {error}</p>
        ) : (
          <p className="text-green-700">Backend says: <span className="font-mono">{message}</span></p>
        )}
      </div>
    </section>
  )
}
