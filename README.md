# AI Shopping Assistant

A full‑stack application that lets users search products semantically, chat with an AI assistant, and get relevant recommendations. Built with FastAPI, LangChain, Google Gemini, FAISS, and a Vite + React frontend.

## Features

- Smart search with semantic retrieval, typo tolerance (fuzzy), and filters (category, price)
- Query suggestions when no exact results
- "Related to your search" query‑based recommendations
- Product‑based recommendations
- AI chat with cited sources
- Cart and wishlist APIs (backend)
- Clean list‑style UI (no grid/cards)

## Tech Stack

- Backend: FastAPI, LangChain, GoogleGenerativeAI, FAISS, rapidfuzz
- Frontend: React (Vite), Tailwind CSS
- Data: `backend/data/products.json`, FAISS index in `backend/vectorstore/`

## Prerequisites

- Python 3.11+ recommended
- Node.js 18+
- A Google Gemini API key

## Setup

1) Clone and install Python deps

```bash
# In repo root
python -m venv venv
# Windows PowerShell
./venv/Scripts/Activate.ps1
pip install -r requirements.txt
```

2) Configure environment

Create a `.env` in repo root or backend with:

```
GEMINI_API_KEY=YOUR_KEY
```

3) Install frontend deps

```bash
cd frontend
npm install
```

## Running

- Backend (from repo root):

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

- Frontend (in `frontend/`):

```bash
npm run dev
```

Open the app at the dev server URL (typically http://localhost:5173).

## Data & Index

- Products are stored in `backend/data/products.json` and loaded at startup into memory (`products_cache`).
- A FAISS index (embeddings for semantic search) lives in `backend/vectorstore/` (`index.faiss`, `index.pkl`).
- The retriever is created in `backend/retriever.py` using `GoogleGenerativeAIEmbeddings(model="models/embedding-001")` and returns a LangChain retriever interface.
- If you need to rebuild the vectorstore, use the provided ingestion scripts (e.g., `backend/rebuild_vectorstore.py` if present) to embed documents and write the FAISS index.

## Backend Overview

File: `backend/main.py`

- App setup
  - CORS enabled for local frontend
  - Logging + global error handler
  - Startup loads: FAISS retriever + `products_cache`

- Models
  - `ChatRequest`: `{ query: str }`

- Helpers
  - `success_response(message, data)` and `error_response(message)` unify responses

- Endpoints
  - `GET /`: health
  - `POST /chat`: uses `ask_ai(query)` from `backend/chat_chain.py`; returns `{ data: { answer, sources } }`
  - `GET /products`: all products from cache
  - `GET /products/{product_id}`: one product by id
  - `POST /search?query=...&top_k=5&category=&min_price=&max_price=`
    - Semantic recall via retriever
    - Exact/substring check on `product_name`
    - Fuzzy expansion via `rapidfuzz` over `product_name + about_product`
    - Optional filters (category/price)
    - Suggestions if no results
    - Returns `{ products, suggestions }`
  - `GET /recommendations/{product_id}?top_k=5`: product‑based recs (exclude self)
  - `GET /recommendations/by-query?query=...&top_k=6`: query‑based recs
  - Cart/Wishlist:
    - `POST /cart/add`, `/cart/remove`, `/cart/update`, `GET /cart/{user_id}`, `POST /cart/clear`
    - `POST /wishlist/add`, `/wishlist/remove`, `GET /wishlist/{user_id}`, `POST /wishlist/move-to-cart`

File: `backend/chat_chain.py`

- Loads `GEMINI_API_KEY` from `.env`
- Constructs Gemini chat LLM: `ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)`
- Builds a `RetrievalQA` chain with the global retriever
- `ask_ai(query)` runs the chain and returns `{ result, source_documents }`

File: `backend/retriever.py`

- Builds embeddings with `GoogleGenerativeAIEmbeddings(model="models/embedding-001")`
- Loads FAISS vectorstore from `backend/vectorstore/` (dangerous deserialization allowed for FAISS pickle)
- Returns `as_retriever(search_kwargs={"k": k})`

## Frontend Overview

Key files in `frontend/src/`:

- `App.jsx`: routes and layout; imports `Navbar` and pages
- `components/Navbar.jsx`: minimal link list
- `pages/Home.jsx`: hero, search input, status, features (list)
- `pages/Search.jsx`:
  - Live suggestions from `/products` list
  - Submits search to `/search` with filters (category, min/max price)
  - Shows suggestions if no results
  - Shows query‑based recs from `/recommendations/by-query`
  - Shows product‑based recs for first result via `/recommendations/{product_id}`
  - All product displays are list items with dividers (no grid/cards)
- `pages/Chat.jsx`: simple chat with history; messages rendered as lightweight bubbles
- `pages/Products.jsx`: static example list (list items, no cards)
- `pages/productDetails.jsx`: product details + recommended list

## Typical Flow

1) User opens app → `GET /` verifies backend is running (shown on Home).
2) User types in Search → frontend calls:
   - `POST /search?query=...&category=&min_price=&max_price=` → `{ products, suggestions }`
   - `GET /recommendations/by-query?query=...` → related items
   - If there are results, also `GET /recommendations/{firstProductId}` → product‑based recs
3) User chats in Chat page → `POST /chat` → Gemini answers with cited sources.

## Environment & Security Notes

- Ensure `GEMINI_API_KEY` is kept private; do not commit `.env`.
- `allow_dangerous_deserialization=True` is required by FAISS load; only load trusted indices.

## Troubleshooting

- Missing FAISS index: rebuild the vectorstore (find or implement `rebuild_vectorstore.py`).
- 401/403 from Gemini: verify `GEMINI_API_KEY` and billing access.
- CORS errors: confirm FastAPI CORS settings and frontend origin.
- Typos not matching: fuzzy threshold is ~70; tune in `main.py` if needed.

## Scripts & Commands

```bash
# Run backend
echo GEMINI_API_KEY=... > .env
uvicorn backend.main:app --reload

# Run frontend
cd frontend
npm install
npm run dev
```

## License

MIT (add your preferred license text). 