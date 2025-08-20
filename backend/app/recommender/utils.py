import math
from typing import Optional

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0088
    phi1 = math.radians(lat1); phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1); dl = math.radians(lon2 - lon1)
    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dl/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R*c

def safe_geo_score(d: Optional[float]) -> float:
    if d is None: return 0.0
    return math.exp(-d/50.0)

def min_max_scale(x, a, b):
    if b == a: return 0.0
    return (x-a)/(b-a)

def mmr_rerank(items, lambda_div=0.75, top_k=20):
    selected = []
    cand = items.copy()
    while cand and len(selected) < top_k:
        if not selected:
            best = max(cand, key=lambda t: t[1]); selected.append(best); cand.remove(best); continue
        def val(t):
            rel = t[1]
            max_sim = max((sum(a*b for a,b in zip(t[2], s[2])) for s in selected if t[2] is not None and s[2] is not None), default=0.0)
            return lambda_div*rel - (1-lambda_div)*max_sim
        best = max(cand, key=val); selected.append(best); cand.remove(best)
    return selected
