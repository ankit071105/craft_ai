from .database import Base, engine, SessionLocal
from . import models
import random

INDIAN_CITIES = [
    ("Delhi", 28.6139, 77.2090),
    ("Mumbai", 19.0760, 72.8777),
    ("Jaipur", 26.9124, 75.7873),
    ("Kolkata", 22.5726, 88.3639),
    ("Bengaluru", 12.9716, 77.5946),
    ("Chennai", 13.0827, 80.2707),
    ("Lucknow", 26.8467, 80.9462),
    ("Varanasi", 25.3176, 82.9739),
    ("Agra", 27.1767, 78.0081),
    ("Ahmedabad", 23.0225, 72.5714),
]

CRAFTS = [
    ("Blue Pottery Vase", "Handcrafted Jaipur blue pottery.", "home, pottery, blue, jaipur", "https://images.unsplash.com/photo-1544735716-392fe2489ffa?q=80&w=800"),
    ("Madhubani Painting", "Traditional Mithila art.", "art, painting, madhubani, bihar", "https://images.unsplash.com/photo-1520697222862-6b23c0b303ae?q=80&w=800"),
    ("Kalamkari Dupatta", "Hand-painted cotton dupatta.", "textile, kalamkari, andhra", "https://images.unsplash.com/photo-1610030469989-8e1431a5e3b5?q=80&w=800"),
    ("Channapatna Toy", "Eco-friendly lacquered wooden toy.", "toys, wood, channapatna", "https://images.unsplash.com/photo-1601758064138-8ea22a595a0d?q=80&w=800"),
    ("Banarasi Silk Scarf", "Fine silk with zari work.", "silk, banaras, textile", "https://images.unsplash.com/photo-1530023367847-a683933f4178?q=80&w=800"),
    ("Terracotta Planter", "Clay planter with rustic finish.", "terracotta, clay, garden", "https://images.unsplash.com/photo-1523419410397-64f81d6e9f6c?q=80&w=800"),
    ("Dokra Necklace", "Tribal brass necklace.", "jewelry, dokra, brass", "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?q=80&w=800"),
    ("Pashmina Shawl", "Soft pashmina wool shawl.", "shawl, kashmir, wool", "https://images.unsplash.com/photo-1512436991641-6745cdb1723f?q=80&w=800"),
    ("Warli Painting", "Tribal art village scenes.", "warli, tribal, painting", "https://images.unsplash.com/photo-1520697222862-6b23c0b303ae?q=80&w=800"),
    ("Bidriware Box", "Blackened alloy box with silver inlay.", "bidri, metal, decor", "https://images.unsplash.com/photo-1481437642641-2f0ae875f836?q=80&w=800"),
]

def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    sellers = []
    for i in range(5):
        city, lat, lon = random.choice(INDIAN_CITIES)
        s = models.Seller(name=f"Seller {i+1}", city=city, lat=lat, lon=lon)
        db.add(s); sellers.append(s)
    db.commit()
    for s in sellers: db.refresh(s)

    for i in range(40):
        item = random.choice(CRAFTS)
        city, lat, lon = random.choice(INDIAN_CITIES)
        seller = random.choice(sellers)
        p = models.Product(
            name=item[0], description=item[1], price=round(random.uniform(199, 4999), 2),
            category="crafts", tags=item[2], seller_id=seller.id, city=city,
            lat=lat + random.uniform(-0.15, 0.15), lon=lon + random.uniform(-0.15, 0.15),
            image_url=item[3]
        )
        db.add(p)
    db.commit()
    print("Seeded.")

if __name__ == "__main__":
    run()
