import React, { useEffect, useMemo, useState } from "react";
import Header from "../components/Header.jsx";
import LocationPrompt from "../components/LocationPrompt.jsx";
import ProductCard from "../components/ProductCard.jsx";
import FeedbackModal from "../components/FeedbackModal.jsx";
import api from "../api.js";

export default function App(){
  const [user, setUser] = useState(null);
  const [loc, setLoc] = useState(null);
  const [recs, setRecs] = useState([]);
  const [showFeedback, setShowFeedback] = useState(false);
  const [feedbackFor, setFeedbackFor] = useState(null);

  useEffect(()=>{
    const u = localStorage.getItem("user");
    if(u) setUser(JSON.parse(u));
  },[]);

  useEffect(()=>{
    if((user || loc) && recs.length===0){
      fetchRecs();
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user, loc]);

  async function createGuestAndFetch({lat, lon}){
    setLoc({lat, lon});
    const res = await api.post("/users/guest", null, { params: {lat, lon} });
    setUser(res.data); localStorage.setItem("user", JSON.stringify(res.data));
    await fetchRecs(res.data, {lat, lon});
  }

  async function fetchRecs(_user=user, _loc=loc){
    const params = {};
    if(_user) params.user_id = _user.id;
    if(_loc){ params.lat=_loc.lat; params.lon=_loc.lon; }
    const { data } = await api.get("/recommendations", { params });
    setRecs(data.map(r=>r.product));
  }

  async function log(kind, product_id){
    if(!user) return;
    await api.post("/interactions", { user_id: user.id, product_id, kind });
  }

  function onAskFeedback(product_id){
    setFeedbackFor(product_id); setShowFeedback(true);
  }

  async function submitFeedback({rating, comment}){
    if(!feedbackFor) return;
    await api.post("/feedback", { user_id: user?.id, product_id: feedbackFor, rating, comment });
    setShowFeedback(false); setFeedbackFor(null);
  }

  return (
    <div>
      <Header />
      <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">
        {!user && !loc && (
          <section className="bg-white rounded-2xl p-5 border shadow-sm">
            <h1 className="text-xl font-semibold mb-2">Get hyper‑local recommendations</h1>
            <LocationPrompt onSubmit={createGuestAndFetch} />
          </section>
        )}

        <section className="space-y-3">
          <div className="flex items-end justify-between">
            <h2 className="text-lg font-semibold">Recommended for you</h2>
            {user && <div className="text-sm text-slate-500">User #{user.id} {user.is_guest ? "(guest)" : ""}</div>}
          </div>

          {recs.length === 0 ? (
            <div className="text-slate-500">No products yet—try seeding the backend data or adjusting your location.</div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {recs.map(p => (
                <ProductCard key={p.id}
                  product={p}
                  onView={(id)=>log("view", id)}
                  onClick={(id)=>log("click", id)}
                  onWishlist={(id)=>{ log("wishlist", id); onAskFeedback(id); }}
                />
              ))}
            </div>
          )}
        </section>
      </main>

      <FeedbackModal open={showFeedback} onClose={()=>setShowFeedback(false)} onSubmit={submitFeedback} />
    </div>
  );
}
