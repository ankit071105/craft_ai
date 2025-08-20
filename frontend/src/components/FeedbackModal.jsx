import React, { useState } from "react";

export default function FeedbackModal({ open, onClose, onSubmit }){
  const [rating, setRating] = useState(5);
  const [comment, setComment] = useState("");
  if(!open) return null;
  return (
    <div className="fixed inset-0 bg-black/40 grid place-items-center z-50">
      <div className="w-[95%] max-w-md bg-white rounded-2xl p-4 space-y-3">
        <div className="text-lg font-semibold">Help improve recommendations</div>
        <div className="flex items-center gap-2">
          <label className="text-sm">Your rating:</label>
          <select className="border rounded px-2 py-1" value={rating} onChange={e=>setRating(+e.target.value)}>
            {[1,2,3,4,5].map(n=><option key={n} value={n}>{n}</option>)}
          </select>
        </div>
        <textarea className="w-full border rounded p-2" rows="3" placeholder="What did you like or not like?"
          value={comment} onChange={e=>setComment(e.target.value)} />
        <div className="flex gap-2 justify-end">
          <button onClick={onClose} className="px-3 py-1 rounded-lg border">Cancel</button>
          <button onClick={()=>onSubmit({rating, comment})} className="px-3 py-1 rounded-lg bg-black text-white">Submit</button>
        </div>
      </div>
    </div>
  );
}
