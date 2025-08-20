import React, { useEffect, useState } from "react";
import { MapContainer, TileLayer, Marker, useMapEvents } from "react-leaflet";
import L from "leaflet";

const markerIcon = new L.Icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25,41], iconAnchor: [12,41]
});

function ClickHandler({ setPos }){
  useMapEvents({
    click(e){ setPos([e.latlng.lat, e.latlng.lng]); }
  });
  return null;
}

export default function LocationPrompt({ onSubmit }) {
  const [pos, setPos] = useState([20.5937, 78.9629]); // India approx
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!navigator.geolocation) return;
    navigator.geolocation.getCurrentPosition(
      (p) => setPos([p.coords.latitude, p.coords.longitude]),
      () => {}
    );
  }, []);

  return (
    <div className="space-y-3">
      <p className="text-slate-700">Share your location to get local recommendations. Move the pin to adjust.</p>
      <div className="rounded-2xl overflow-hidden shadow">
        <MapContainer center={pos} zoom={12} scrollWheelZoom={true}>
          <TileLayer
            attribution='&copy; OpenStreetMap contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />
          <Marker position={pos} icon={markerIcon} />
          <ClickHandler setPos={setPos} />
        </MapContainer>
      </div>
      <div className="flex gap-2">
        <button
          onClick={() => onSubmit({ lat: pos[0], lon: pos[1] })}
          className="px-4 py-2 rounded-xl bg-black text-white"
        >
          Use this location
        </button>
      </div>
    </div>
  );
}
