import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import Header from "../components/Header.jsx";
import api from "../api.js";

export default function ProductPage(){
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [user, setUser] = useState(null);

  useEffect(()=>{
    const u = localStorage.getItem("user"); if(u) setUser(JSON.parse(u));
    async function load(){
      const { data } = await api.get(`/products/${id}`);
      setProduct(data);
    }
    load();
  }, [id]);

  async function log(kind){
    if(!user) return;
    await api.post("/interactions", { user_id: user.id, product_id: product.id, kind });
  }

  async function addToCart(){ await log("cart"); }
  async function purchase(){ await log("purchase"); }

  if(!product) return <div className="p-4">Loading...</div>;

  return (
    <div>
      <Header />
      <main className="max-w-5xl mx-auto px-4 py-6">
        <div className="grid md:grid-cols-2 gap-6">
          <img src={product.image_url} alt={product.name} className="rounded-2xl w-full h-80 object-cover border" />
          <div className="space-y-3">
            <h1 className="text-2xl font-semibold">{product.name}</h1>
            <div className="text-slate-500">{product.description}</div>
            <div className="text-xl font-semibold">₹{product.price}</div>
            <div className="flex gap-2">
              <button onClick={addToCart} className="px-4 py-2 rounded-xl border">Add to cart</button>
              <button onClick={purchase} className="px-4 py-2 rounded-xl bg-black text-white">Buy now</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
