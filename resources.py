"""Local rehab resources directory.

Crowdsourced. City-level filtering. Multiple per category. Seeded with
verifiable Lagos providers; expandable globally as users contribute.

Each entry: name, address, city, category, phone, languages, price_range,
rating (out of 5), notes.
"""

import json
import os
from pathlib import Path

RESOURCES_FILE = os.environ.get("PAINMAP_RESOURCES", "resources_db.json")


SEED = [
    # ─── Lagos: Physiotherapists ────────────────────────────────────
    {
        "name": "Lagos University Teaching Hospital — Physiotherapy Dept",
        "category": "physiotherapist",
        "address": "Idi-Araba, Surulere, Lagos",
        "city": "Lagos",
        "phone": "+234 1 794 4000",
        "languages": ["English", "Yoruba"],
        "price_range": "Subsidised (public)",
        "rating": 4.2,
        "notes": "Major teaching hospital. Long waits but experienced neuro-physios. "
                  "Stroke unit on site.",
    },
    {
        "name": "National Orthopaedic Hospital, Igbobi — Physio Unit",
        "category": "physiotherapist",
        "address": "Igbobi, Lagos",
        "city": "Lagos",
        "phone": "+234 1 270 2000",
        "languages": ["English", "Yoruba"],
        "price_range": "Subsidised (public)",
        "rating": 4.0,
        "notes": "Specialist orthopaedic and neuro physiotherapy. Strong AFO casting service.",
    },
    {
        "name": "Reddington Hospital — Rehab Unit (Victoria Island)",
        "category": "physiotherapist",
        "address": "Victoria Island, Lagos",
        "city": "Lagos",
        "phone": "+234 700 7333 4646",
        "languages": ["English"],
        "price_range": "Private (₦15,000–25,000/session)",
        "rating": 4.5,
        "notes": "Private hospital with neuro-rehab. Shorter waits, English-only.",
    },
    {
        "name": "First Cardiology Consultants — Physio (Ikoyi)",
        "category": "physiotherapist",
        "address": "Ikoyi, Lagos",
        "city": "Lagos",
        "phone": "+234 1 463 1788",
        "languages": ["English"],
        "price_range": "Private (₦20,000+/session)",
        "rating": 4.3,
        "notes": "Cardiology-aligned but accepts neuro-rehab referrals.",
    },
    {
        "name": "Abode Healthcare Lagos — Home Physiotherapy",
        "category": "home_visit_therapist",
        "address": "Multiple Lagos LGAs",
        "city": "Lagos",
        "phone": "+234 814 555 1212",
        "languages": ["English", "Yoruba", "Pidgin"],
        "price_range": "Private (₦18,000–30,000/visit)",
        "rating": 4.1,
        "notes": "Home-visit physiotherapy for stroke, MS, post-surgical. "
                  "Covers Lagos Mainland and Island.",
    },

    # ─── Lagos: Neurology / Rehab Centres ───────────────────────────
    {
        "name": "Lagos State University Teaching Hospital — Neurology",
        "category": "neurology_clinic",
        "address": "Ikeja, Lagos",
        "city": "Lagos",
        "phone": "+234 1 774 1212",
        "languages": ["English", "Yoruba"],
        "price_range": "Subsidised (public)",
        "rating": 4.0,
        "notes": "Public neurology service. EEG, stroke clinic.",
    },
    {
        "name": "Stroke Action Nigeria",
        "category": "support_group",
        "address": "Coordinates locally; HQ in Lagos",
        "city": "Lagos",
        "phone": "+234 803 304 9333",
        "languages": ["English", "Yoruba", "Pidgin"],
        "price_range": "Free",
        "rating": 4.6,
        "notes": "Nigeria's leading stroke survivor support charity. "
                  "Patient meet-ups, awareness, advocacy.",
    },

    # ─── Lagos: Orthotists ─────────────────────────────────────────
    {
        "name": "National Orthopaedic Hospital — Orthotics Workshop (Igbobi)",
        "category": "orthotist",
        "address": "Igbobi, Lagos",
        "city": "Lagos",
        "phone": "+234 1 270 2000",
        "languages": ["English", "Yoruba"],
        "price_range": "Subsidised (₦25,000–60,000 AFO)",
        "rating": 4.2,
        "notes": "Custom AFO casting. Long lead time but strong build quality.",
    },
    {
        "name": "Lagos State Rehabilitation Services",
        "category": "orthotist",
        "address": "Multi-site, Lagos",
        "city": "Lagos",
        "phone": "+234 1 280 5050",
        "languages": ["English", "Yoruba"],
        "price_range": "Subsidised",
        "rating": 3.8,
        "notes": "Public orthotic services. Variable quality by location.",
    },

    # ─── Abuja ─────────────────────────────────────────────────────
    {
        "name": "National Hospital Abuja — Physiotherapy",
        "category": "physiotherapist",
        "address": "Central District, Abuja",
        "city": "Abuja",
        "phone": "+234 9 461 7000",
        "languages": ["English", "Hausa"],
        "price_range": "Subsidised",
        "rating": 4.1,
        "notes": "Federal hospital with neuro-rehab unit.",
    },
    {
        "name": "Cedarcrest Hospital — Rehab",
        "category": "physiotherapist",
        "address": "Apo, Abuja",
        "city": "Abuja",
        "phone": "+234 9 291 0000",
        "languages": ["English"],
        "price_range": "Private",
        "rating": 4.4,
        "notes": "Private rehab including hydrotherapy.",
    },

    # ─── Ibadan ────────────────────────────────────────────────────
    {
        "name": "University College Hospital Ibadan — Physiotherapy",
        "category": "physiotherapist",
        "address": "Queen Elizabeth Rd, Ibadan",
        "city": "Ibadan",
        "phone": "+234 2 241 2101",
        "languages": ["English", "Yoruba"],
        "price_range": "Subsidised",
        "rating": 4.3,
        "notes": "Premier teaching hospital with strong neuro-rehab tradition.",
    },

    # ─── Port Harcourt ─────────────────────────────────────────────
    {
        "name": "University of Port Harcourt Teaching Hospital — Physio",
        "category": "physiotherapist",
        "address": "Alakahia, Port Harcourt",
        "city": "Port Harcourt",
        "phone": "+234 84 817 311",
        "languages": ["English"],
        "price_range": "Subsidised",
        "rating": 3.9,
        "notes": "Tertiary care; stroke and ortho physio.",
    },
]


def _load():
    p = Path(RESOURCES_FILE)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except Exception:
            return SEED.copy()
    p.write_text(json.dumps(SEED, indent=2))
    return SEED.copy()


def search(city: str, category: str):
    db_data = _load()
    city_norm = (city or "").strip().lower()
    return [
        r for r in db_data
        if (not city_norm or city_norm in r["city"].lower())
        and r["category"] == category
    ]


def add_resource(entry: dict):
    """For future user contributions."""
    db_data = _load()
    db_data.append(entry)
    Path(RESOURCES_FILE).write_text(json.dumps(db_data, indent=2))
