"""
backend/cart_wishlist.py

Simple, file-backed (JSON) cart & wishlist utilities + FastAPI helper endpoints.
- Uses a Lock to avoid concurrent writes corrupting the JSON files.
- Data layout:
  cart.json: { "<user_id>": [ {"product_id": "...", "quantity": 2}, ... ], ... }
  wishlist.json: { "<user_id>": [ "product_id1", "product_id2", ... ], ... }

Note: This is intentionally simple for a student project / prototype.
You can later replace JSON storage with a proper DB (Postgres/Mongo).
"""

import json
from pathlib import Path
from threading import Lock
from typing import List, Dict, Any

# File paths relative to this module
BASE = Path(__file__).parent
CART_FILE = BASE / "data" / "cart.json"
WISHLIST_FILE = BASE / "data" / "wishlist.json"

# Locks to prevent concurrent read/write corruption
_cart_lock = Lock()
_wishlist_lock = Lock()

# Helper: ensure data directory & files exist (called on import)
def _ensure_files():
    """
    Make sure the data folder and JSON files exist.
    If files don't exist, create them with empty JSON objects.
    """
    data_dir = BASE / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    if not CART_FILE.exists():
        CART_FILE.write_text(json.dumps({}, ensure_ascii=False), encoding="utf-8")
    if not WISHLIST_FILE.exists():
        WISHLIST_FILE.write_text(json.dumps({}, ensure_ascii=False), encoding="utf-8")

# Read-cart (thread-safe)
def _read_cart() -> Dict[str, List[Dict[str, Any]]]:
    """Return the whole cart JSON as dict (user_id -> list of items)."""
    with _cart_lock:
        with open(CART_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

# Write-cart (thread-safe)
def _write_cart(data: Dict[str, List[Dict[str, Any]]]) -> None:
    """Overwrite the cart JSON file atomically (under a lock)."""
    with _cart_lock:
        with open(CART_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# Read-wishlist (thread-safe)
def _read_wishlist() -> Dict[str, List[str]]:
    """Return the whole wishlist JSON as dict (user_id -> list of product_ids)."""
    with _wishlist_lock:
        with open(WISHLIST_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

# Write-wishlist (thread-safe)
def _write_wishlist(data: Dict[str, List[str]]) -> None:
    """Overwrite the wishlist JSON file atomically (under a lock)."""
    with _wishlist_lock:
        with open(WISHLIST_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

# Utility: add item to cart
def add_to_cart(user_id: str, product_id: str, quantity: int = 1) -> Dict[str, Any]:
    """
    Add product to user's cart with given quantity.
    If product exists, increment quantity.
    Returns the new cart for the user.
    """
    if quantity <= 0:
        raise ValueError("Quantity must be >= 1")

    carts = _read_cart()
    user_cart = carts.get(user_id, [])

    # Find existing item
    for item in user_cart:
        if item["product_id"] == product_id:
            item["quantity"] += quantity
            break
    else:
        # not found -> append new item
        user_cart.append({"product_id": product_id, "quantity": quantity})

    carts[user_id] = user_cart
    _write_cart(carts)
    return {"user_id": user_id, "cart": user_cart}

# Utility: remove item from cart (entirely)
def remove_from_cart(user_id: str, product_id: str) -> Dict[str, Any]:
    """
    Remove a product from the user's cart completely.
    Returns the updated cart.
    """
    carts = _read_cart()
    user_cart = carts.get(user_id, [])
    new_cart = [item for item in user_cart if item["product_id"] != product_id]
    carts[user_id] = new_cart
    _write_cart(carts)
    return {"user_id": user_id, "cart": new_cart}

# Utility: update quantity (set exact quantity; if 0 -> remove)
def update_cart_quantity(user_id: str, product_id: str, quantity: int) -> Dict[str, Any]:
    """
    Set exact quantity for a product in cart. If quantity == 0, remove product.
    """
    if quantity < 0:
        raise ValueError("Quantity must be >= 0")

    carts = _read_cart()
    user_cart = carts.get(user_id, [])
    found = False
    new_cart = []
    for item in user_cart:
        if item["product_id"] == product_id:
            found = True
            if quantity > 0:
                new_cart.append({"product_id": product_id, "quantity": quantity})
            # else skip -> remove
        else:
            new_cart.append(item)

    # if not found and quantity>0, add it
    if (not found) and quantity > 0:
        new_cart.append({"product_id": product_id, "quantity": quantity})

    carts[user_id] = new_cart
    _write_cart(carts)
    return {"user_id": user_id, "cart": new_cart}

# Utility: get user cart
def get_cart(user_id: str) -> Dict[str, Any]:
    """Return the cart content for given user_id (empty list if none)."""
    carts = _read_cart()
    return {"user_id": user_id, "cart": carts.get(user_id, [])}

# Utility: clear cart
def clear_cart(user_id: str) -> Dict[str, Any]:
    """Empty the user's cart."""
    carts = _read_cart()
    carts[user_id] = []
    _write_cart(carts)
    return {"user_id": user_id, "cart": []}

# ---------------- WISHLIST FUNCTIONS ----------------

def add_to_wishlist(user_id: str, product_id: str) -> Dict[str, Any]:
    """
    Add product_id to user's wishlist. No duplicates allowed.
    Returns updated wishlist for the user.
    """
    wishes = _read_wishlist()
    user_wish = wishes.get(user_id, [])
    if product_id not in user_wish:
        user_wish.append(product_id)
    wishes[user_id] = user_wish
    _write_wishlist(wishes)
    return {"user_id": user_id, "wishlist": user_wish}

def remove_from_wishlist(user_id: str, product_id: str) -> Dict[str, Any]:
    """
    Remove product_id from user's wishlist.
    """
    wishes = _read_wishlist()
    user_wish = wishes.get(user_id, [])
    user_wish = [pid for pid in user_wish if pid != product_id]
    wishes[user_id] = user_wish
    _write_wishlist(wishes)
    return {"user_id": user_id, "wishlist": user_wish}

def get_wishlist(user_id: str) -> Dict[str, Any]:
    """Return wishlist for the user."""
    wishes = _read_wishlist()
    return {"user_id": user_id, "wishlist": wishes.get(user_id, [])}

def move_wishlist_to_cart(user_id: str, product_id: str, quantity: int = 1) -> Dict[str, Any]:
    """
    Move an item from wishlist to cart:
      - remove from wishlist
      - add to cart with given quantity
    Returns both updated wishlist and cart.
    """
    # remove from wishlist
    remove_from_wishlist(user_id, product_id)
    # add to cart
    cart_state = add_to_cart(user_id, product_id, quantity)
    wish_state = get_wishlist(user_id)
    return {"user_id": user_id, "cart": cart_state["cart"], "wishlist": wish_state["wishlist"]}

# Ensure files exist when module is imported
_ensure_files()
