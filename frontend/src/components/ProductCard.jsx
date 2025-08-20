import React, { useEffect } from "react";
import { Link } from "react-router-dom";

export default function ProductCard({ product, onView, onClick, onWishlist }) {
  useEffect(() => { onView?.(product.id); }, []);
  return (
    <div className="group rounded-2xl border bg-white overflow-hidden shadow-sm hover:shadow-md transition">
      <Link to={`/product/${product.id}`} onClick={() => onClick?.(product.id)}>
        <img src={product.image_url} alt={product.name} className="w-full h-44 object-cover" />
        <div className="p-3 space-y-1">
          <div className="font-medium">{product.name}</div>
          <div className="text-sm text-slate-500">₹{product.price}</div>
        </div>
      </Link>
      <div className="px-3 pb-3">
        <button onClick={() => onWishlist?.(product.id)} className="text-sm px-3 py-1 rounded-lg border">
          ❤️ Wishlist
        </button>
      </div>
    </div>
  );
}
