from typing import Optional, List, Tuple
from sqlalchemy.orm import Session
from .. import models
from .utils import haversine_km, safe_geo_score, min_max_scale, mmr_rerank

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class RecommenderEngine:
    def __init__(self, db: Session):
        self.db = db
        self._tfidf = None
        self._emb = None
        self._prods = None

    def _build(self):
        prods = self.db.query(models.Product).all()
        texts = []
        for p in prods:
            t = " ".join([p.name or "", p.description or "", (p.tags or "").replace(",", " "), p.category or ""]).strip()
            texts.append(t)
        if not texts:
            self._tfidf = None; self._emb=None; self._prods=prods; return
        self._tfidf = TfidfVectorizer(max_features=5000)
        X = self._tfidf.fit_transform(texts).toarray()
        norms = np.linalg.norm(X, axis=1, keepdims=True) + 1e-8
        self._emb = X / norms
        self._prods = prods

    def _user_vec(self, user: Optional[models.User]):
        if user is None or self._tfidf is None: return None
        weights = {"view":0.5, "click":0.7, "wishlist":1.0, "cart":1.2, "purchase":1.5}
        inter = self.db.query(models.Interaction).filter(models.Interaction.user_id==user.id).all()
        if not inter: return None
        ids = [it.product_id for it in inter]
        mp = {p.id:p for p in self.db.query(models.Product).filter(models.Product.id.in_(ids)).all()}
        docs, wts = [], []
        for it in inter:
            p = mp.get(it.product_id); 
            if not p: continue
            t = " ".join([p.name or "", p.description or "", (p.tags or "").replace(",", " "), p.category or ""]).strip()
            docs.append(t); wts.append(weights.get(it.kind, 0.5))
        if not docs: return None
        X = self._tfidf.transform(docs).toarray()
        prof = (X * np.array(wts).reshape(-1,1)).sum(axis=0)
        n = np.linalg.norm(prof)+1e-8
        return prof/n

    def recommend(self, user_id: Optional[int], lat: Optional[float], lon: Optional[float], k:int=20):
        self._build()
        prods = self._prods
        if not prods: return []
        pops = [len(p.interactions) for p in prods]
        pmin, pmax = (min(pops) if pops else 0), (max(pops) if pops else 1)
        user = self.db.get(models.User, user_id) if user_id else None
        if user and (lat is None or lon is None):
            lat = lat if lat is not None else user.lat
            lon = lon if lon is not None else user.lon
        uvec = self._user_vec(user)
        scored = []
        for i,p in enumerate(prods):
            dist = None; g = 0.0
            if lat is not None and lon is not None and p.lat is not None and p.lon is not None:
                dist = haversine_km(lat, lon, p.lat, p.lon); g = safe_geo_score(dist)
            pop = min_max_scale(len(p.interactions), pmin, pmax) if pmax>0 else 0.0
            c = 0.0
            if uvec is not None and self._emb is not None:
                c = float(np.dot(self._emb[i], uvec))
            score = 0.5*g + 0.3*pop + 0.2*c
            emb = self._emb[i] if self._emb is not None else None
            scored.append((i, score, emb, dist))
        reranked = mmr_rerank([(i,s,e) for (i,s,e,_) in scored], lambda_div=0.75, top_k=min(k, len(scored)))
        out = []
        for (i,s,_e) in reranked:
            p = prods[i]
            dist = next((d for (ii,_ss,_ee,d) in scored if ii==i), None)
            out.append((p, float(s), dist))
        return out
