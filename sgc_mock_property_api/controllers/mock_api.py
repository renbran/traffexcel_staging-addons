# -*- coding: utf-8 -*-
"""
SGC Mock Property Portal API
==============================
Mimics Property Finder / Bayut / Dubai Rest API style endpoints for
integration testing.  No DB dependency -- all data is in-memory.

Usage after installing the module:
  curl http://your-odoo:8069/api/v1/property-portal/properties
  curl http://your-odoo:8069/api/v1/property-portal/properties/42
  curl http://your-odoo:8069/api/v1/property-portal/properties/search?q=dubai+marina&type=apartment
  curl http://your-odoo:8069/api/v1/property-portal/locations?q=marina
  curl http://your-odoo:8069/api/v1/property-portal/agents
  curl http://your-odoo:8069/api/v1/property-portal/stats
  curl -X POST http://your-odoo:8069/api/v1/property-portal/inquiry \
    -H "Content-Type: application/json" \
    -d '{"name":"Test","email":"t@t.com","phone":"+971501234567","property_id":1,"message":"Interested"}'
"""
import logging
import random
import time
from datetime import datetime, timedelta
from functools import lru_cache

from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mock data: realistic UAE property listings
# ---------------------------------------------------------------------------

COMMUNITIES = [
    # (name, city, lat, lng, type)
    ("Dubai Marina", "Dubai", 25.0805, 55.1403, "community"),
    ("Palm Jumeirah", "Dubai", 25.1124, 55.1390, "community"),
    ("Downtown Dubai", "Dubai", 25.1962, 55.2744, "community"),
    ("Arabian Ranches", "Dubai", 25.0500, 55.2700, "community"),
    ("Emirates Hills", "Dubai", 25.0652, 55.1557, "community"),
    ("Jumeirah Lakes Towers (JLT)", "Dubai", 25.0677, 55.1403, "community"),
    ("Business Bay", "Dubai", 25.1850, 55.2600, "community"),
    ("Dubai Hills Estate", "Dubai", 25.1200, 55.2300, "community"),
    ("Al Barsha", "Dubai", 25.1113, 55.1960, "community"),
    ("Jumeirah Beach Residence (JBR)", "Dubai", 25.0800, 55.1360, "community"),
    ("Al Furjan", "Dubai", 25.0300, 55.1500, "community"),
    ("Dubai Silicon Oasis", "Dubai", 25.1300, 55.3800, "community"),
    ("Mohammed Bin Rashid City", "Dubai", 25.1700, 55.3200, "community"),
    ("Jumeirah Village Circle (JVC)", "Dubai", 25.0800, 55.2100, "community"),
    ("Al Raha Beach", "Abu Dhabi", 24.4637, 54.4850, "community"),
    ("Saadiyat Island", "Abu Dhabi", 24.5347, 54.4400, "community"),
    ("Yas Island", "Abu Dhabi", 24.4900, 54.5800, "community"),
    ("Al Reem Island", "Abu Dhabi", 24.4930, 54.4070, "community"),
    ("Corniche Area", "Abu Dhabi", 24.4667, 54.3667, "community"),
    ("Al Bandar", "Abu Dhabi", 24.5200, 54.4200, "community"),
    ("Al Maryah Island", "Abu Dhabi", 24.4969, 54.3896, "community"),
    ("Al Zahia", "Sharjah", 25.3700, 55.4200, "community"),
    ("Al Majaz", "Sharjah", 25.3200, 55.3800, "community"),
    ("Aljada", "Sharjah", 25.3300, 55.4400, "community"),
    ("Mirdif", "Dubai", 25.2300, 55.4200, "area"),
    ("Al Nahda", "Dubai", 25.2800, 55.3600, "area"),
    ("Deira", "Dubai", 25.2800, 55.3100, "area"),
    ("Bur Dubai", "Dubai", 25.2530, 55.3070, "area"),
    ("Al Qusais", "Dubai", 25.2800, 55.3600, "area"),
    ("Al Reef", "Abu Dhabi", 24.4400, 54.5900, "community"),
]

PROPERTY_TYPES = [
    "Apartment", "Villa", "Townhouse", "Penthouse", "Studio",
    "Duplex", "Office", "Shop", "Warehouse", "Land",
    "Full Floor", "Bulk Units", "Hotel Apartment",
]

FURNISHING = ["Unfurnished", "Semi-Furnished", "Fully Furnished"]

AMENITIES = [
    "Swimming Pool", "Gym", "Covered Parking", "Security",
    "Maid's Room", "Balcony", "Central AC", "Built-in Wardrobes",
    "Private Garden", "Jacuzzi", "Shared Pool", "Concierge",
    "Children's Play Area", "BBQ Area", "Steam Room", "Sauna",
    "Maid Service", "Laundry Room", "Study Room", "Storage Room",
    "Business Center", "Spa", "Tennis Court", "Paddle Tennis",
    "Smart Home System", "Central Heating", "Double Glazing",
]

AGENTS = [
    {"id": 1, "name": "Sarah Ahmed", "company": "Gulf Sotheby's Realty",
     "phone": "+971501234567", "email": "sarah@gulf-sir.com",
     "photo": "https://randomuser.me/api/portraits/women/44.jpg",
     "listings_count": 48, "since": 2018},
    {"id": 2, "name": "Mohammed Al Hashimi", "company": "Betterhomes LLC",
     "phone": "+971502345678", "email": "m.alhashimi@betterhomes.ae",
     "photo": "https://randomuser.me/api/portraits/men/32.jpg",
     "listings_count": 73, "since": 2015},
    {"id": 3, "name": "James Wilson", "company": "Emaar Properties",
     "phone": "+971503456789", "email": "jwilson@emaar.ae",
     "photo": "https://randomuser.me/api/portraits/men/62.jpg",
     "listings_count": 112, "since": 2012},
    {"id": 4, "name": "Fatima Rashed", "company": "Keller Williams UAE",
     "phone": "+971504567890", "email": "fatima@kw-uae.com",
     "photo": "https://randomuser.me/api/portraits/women/68.jpg",
     "listings_count": 35, "since": 2020},
    {"id": 5, "name": "Karim Nasser", "company": "Provident Estate",
     "phone": "+971505678901", "email": "karim@provident.ae",
     "photo": "https://randomuser.me/api/portraits/men/75.jpg",
     "listings_count": 56, "since": 2017},
    {"id": 6, "name": "Layla Hassan", "company": "Allsopp & Allsopp",
     "phone": "+971506789012", "email": "lhassan@allsopp.ae",
     "photo": "https://randomuser.me/api/portraits/women/26.jpg",
     "listings_count": 41, "since": 2019},
    {"id": 7, "name": "Ahmed El Sayed", "company": "Espace Real Estate",
     "phone": "+971507890123", "email": "ahmed@espace.ae",
     "photo": "https://randomuser.me/api/portraits/men/55.jpg",
     "listings_count": 89, "since": 2014},
    {"id": 8, "name": "Noora Al Maktoum", "company": "Dubai Properties",
     "phone": "+971508901234", "email": "noora@dubai-properties.ae",
     "photo": "https://randomuser.me/api/portraits/women/50.jpg",
     "listings_count": 27, "since": 2021},
]

FEATURED_TITLES = [
    "Stunning Marina View Apartment with Premium Finishes",
    "Luxurious Palm Jumeirah Villa with Private Beach Access",
    "Modern Downtown Dubai Penthouse with Burj Khalifa View",
    "Spacious Family Villa in Arabian Ranches with Pool",
    "Executive Office in Business Bay with Panoramic Skyline",
    "Elegant JBR Beachfront Apartment - Walk to the Shore",
    "Contemporary Townhouse in Dubai Hills Estate",
    "High-End Duplex in Emirates Hills - Gated Community",
    "Chic Studio in JLT - Ideal for Young Professionals",
    "Premium Villa on Saadiyat Island - Abu Dhabi Cultural Hub",
]

PRICE_DESCRIPTIONS = [
    "Price includes VAT | Handover Q4 2026",
    "Flexible payment plan available | 60% DLD waived",
    "Full ownership | No commission",
    "RERA registered | BSO compliant",
    "Ready to move | Title deed available",
]

# ---------------------------------------------------------------------------
# Property generator
# ---------------------------------------------------------------------------


def _generate_properties(count=150):
    """Generate *count* realistic property records."""
    props = []
    now = datetime.utcnow()

    for i in range(1, count + 1):
        community = random.choice(COMMUNITIES)
        prop_type = random.choice(PROPERTY_TYPES)
        furnishing = random.choice(FURNISHING)
        agent = random.choice(AGENTS)

        if prop_type in ("Villa", "Townhouse", "Duplex", "Land"):
            beds = random.randint(3, 7)
            baths = random.randint(beds, beds + 2)
            area = random.randint(2500, 15000)
        elif prop_type in ("Full Floor", "Bulk Units", "Warehouse", "Office"):
            beds = None
            baths = random.randint(1, 4)
            area = random.randint(800, 25000)
        elif prop_type == "Penthouse":
            beds = random.randint(2, 5)
            baths = random.randint(beds, beds + 2)
            area = random.randint(2000, 8000)
        elif prop_type == "Studio":
            beds = None
            baths = 1
            area = random.randint(350, 700)
        else:
            beds = random.randint(1, 3)
            baths = beds
            area = random.randint(500, 2500)

        purchase_price = _generate_price(prop_type, "buy", area)
        annual_rent = _generate_price(prop_type, "rent", area)
        is_rental = random.random() < 0.4
        is_furnished = furnishing != "Unfurnished"

        completion_status = random.choices(
            ["Ready", "Ready", "Ready", "Off-Plan", "Off-Plan", "Under Construction"],
            weights=[40, 30, 10, 10, 5, 5],
        )[0]

        created_days_ago = random.randint(0, 90)
        permalink = (
            f"{community[0].lower().replace(' ', '-').replace('(', '').replace(')', '')}"
            f"-{prop_type.lower().replace(' ', '-')}-{i}"
        )

        ref = f"PROP-{now.year}-{i:04d}"

        photos = [
            f"https://picsum.photos/seed/{i}{j}/800/600"
            for j in range(random.randint(3, 8))
        ]

        prop = {
            "id": i,
            "reference": ref,
            "permalink": permalink,
            "title": random.choice(FEATURED_TITLES),
            "description": _generate_description(prop_type, community[0], beds, area),
            "type": prop_type,
            "purpose": "rent" if is_rental else "buy",
            "price": annual_rent if is_rental else purchase_price,
            "price_label": "Annual" if is_rental else "Sale",
            "price_per_sqft": round((annual_rent if is_rental else purchase_price) / max(area, 1), 2),
            "currency": "AED",
            "bedrooms": beds,
            "bathrooms": baths,
            "area_sqft": area,
            "area_sqmt": round(area / 10.764, 2),
            "community": community[0],
            "city": community[1],
            "latitude": community[2] + random.uniform(-0.005, 0.005),
            "longitude": community[3] + random.uniform(-0.005, 0.005),
            "furnished": is_furnished,
            "furnishing": furnishing,
            "completion": completion_status,
            "ownership": random.choice(["Freehold", "Freehold", "Leasehold"]),
            "view": random.choice(["City", "Sea", "Marina", "Pool", "Park", "Community", "None"]),
            "parking": random.randint(0, 3),
            "floor_level": random.randint(1, 50) if prop_type in ("Apartment", "Penthouse", "Studio", "Duplex") else None,
            "total_floors": random.randint(5, 60),
            "amenities": random.sample(AMENITIES, random.randint(3, 10)),
            "photos": photos,
            "photo_count": len(photos),
            "agent": agent,
            "listed_date": (now - timedelta(days=created_days_ago)).isoformat() + "Z",
            "updated_date": (now - timedelta(days=random.randint(0, created_days_ago))).isoformat() + "Z",
            "price_description": random.choice(PRICE_DESCRIPTIONS),
            "permit_number": f"RERA-{random.randint(10000, 99999)}",
            "featured": random.random() < 0.15,
            "status": random.choices(
                ["Active", "Active", "Active", "Under Offer", "Sold"],
                weights=[60, 20, 10, 7, 3],
            )[0],
        }
        props.append(prop)

    return props


def _generate_price(prop_type, purpose, area):
    """Realistic UAE pricing."""
    base_rates = {
        "Apartment": {"buy": (1200, 2500), "rent": (80, 200)},
        "Villa": {"buy": (1500, 3500), "rent": (90, 250)},
        "Townhouse": {"buy": (1100, 2200), "rent": (70, 160)},
        "Penthouse": {"buy": (2500, 6000), "rent": (150, 400)},
        "Studio": {"buy": (1400, 2800), "rent": (90, 190)},
        "Duplex": {"buy": (1800, 4000), "rent": (100, 280)},
        "Office": {"buy": (900, 1800), "rent": (60, 140)},
        "Shop": {"buy": (800, 2000), "rent": (100, 250)},
        "Warehouse": {"buy": (400, 900), "rent": (30, 70)},
        "Land": {"buy": (200, 800), "rent": (5, 20)},
        "Full Floor": {"buy": (1500, 3000), "rent": (100, 200)},
        "Bulk Units": {"buy": (800, 1500), "rent": (50, 100)},
        "Hotel Apartment": {"buy": (1300, 2200), "rent": (100, 180)},
    }
    rates = base_rates.get(prop_type, base_rates["Apartment"])
    per_sqft = random.uniform(rates[purpose][0], rates[purpose][1])
    raw = area * per_sqft
    # Round to nearest thousand / ten-thousand
    if purpose == "rent":
        return round(raw / 1000) * 1000
    return round(raw / 10000) * 10000


def _generate_description(prop_type, community, beds, area):
    """Generate a realistic property description."""
    templates = [
        f"Exceptional {prop_type.lower()} in the heart of {community}. "
        f"This {'spacious ' if beds and beds >= 3 else 'cozy '} "
        f"{beds or ''}-bedroom home offers {area:,} sqft of thoughtfully designed living space. "
        f"Features include floor-to-ceiling windows, premium Italian cabinetry, "
        f"and a private balcony with panoramic views.",

        f"Rare opportunity in {community}! This stunning {prop_type.lower()} "
        f"boasts {area:,} sqft of living space with {'{} bedrooms'.format(beds) if beds else 'open-plan layout'}. "
        f"High-quality finishes throughout, including marble flooring, "
        f"designer kitchen, and spacious built-in wardrobes. "
        f"Building amenities include gym, pool, and 24-hour security.",

        f"Newly listed {prop_type.lower()} in sought-after {community}. "
        f"Perfect for families and professionals alike. "
        f"Open-plan living and dining area flows onto a generous balcony. "
        f"Kitchen is fully equipped with integrated appliances. "
        f"Close to schools, retail, and public transport.",
    ]
    return random.choice(templates)


PROPERTIES = _generate_properties(150)

# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _json_response(data=None, pagination=None, success=True, message=None, status=200):
    """Build a standard JSON envelope."""
    body = {
        "success": success,
        "data": data or {},
        "server_time": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if pagination:
        body["pagination"] = pagination
    if message:
        body["message"] = message
    return request.make_json_response(body, status=status)


def _paginate(items, page, per_page=20):
    """Slice *items* into page and return (slice, pagination_dict)."""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    return items[start:end], {
        "page": page,
        "per_page": per_page,
        "total": total,
        "total_pages": max(1, -(-total // per_page)),  # ceil division
    }


def _parse_int(val, default=None):
    try:
        return int(val)
    except (TypeError, ValueError):
        return default


# ---------------------------------------------------------------------------
# Controller
# ---------------------------------------------------------------------------


class MockPropertyPortal(http.Controller):
    """Mock Bayut / Property Finder style REST API."""

    # ---- listings ---------------------------------------------------------

    @http.route(
        "/api/v1/property-portal/properties",
        type="http", auth="public", methods=["GET"], csrf=False,
        cors="*",
    )
    def property_list(self, **params):
        """Paginated property listing with search, filter, and sort."""
        page = max(1, _parse_int(params.get("page"), 1))
        per_page = min(100, max(1, _parse_int(params.get("per_page"), 20)))
        purpose = params.get("purpose")  # buy | rent
        prop_type = params.get("type")
        community = params.get("community")
        city = params.get("city")
        min_price = _parse_int(params.get("min_price"))
        max_price = _parse_int(params.get("max_price"))
        min_beds = _parse_int(params.get("min_beds"))
        max_beds = _parse_int(params.get("max_beds"))
        furnishing = params.get("furnishing")
        agent_id = _parse_int(params.get("agent_id"))
        featured = params.get("featured")
        status = params.get("status")
        sort_by = params.get("sort_by", "listed_date")
        sort_order = params.get("sort_order", "desc")
        q = params.get("q", "").lower().strip()

        filtered = list(PROPERTIES)

        # Search
        if q:
            filtered = [
                p for p in filtered
                if q in p["title"].lower()
                or q in p["community"].lower()
                or q in p["city"].lower()
                or q in p["type"].lower()
                or q in p["description"].lower()
                or q in p["reference"].lower()
            ]

        # Filters
        if purpose:
            filtered = [p for p in filtered if p["purpose"] == purpose]
        if prop_type:
            types = [t.strip() for t in prop_type.split(",")]
            filtered = [p for p in filtered if p["type"].lower() in [t.lower() for t in types]]
        if community:
            filtered = [p for p in filtered if p["community"].lower() == community.lower()]
        if city:
            filtered = [p for p in filtered if p["city"].lower() == city.lower()]
        if min_price is not None:
            filtered = [p for p in filtered if p["price"] >= min_price]
        if max_price is not None:
            filtered = [p for p in filtered if p["price"] <= max_price]
        if min_beds is not None:
            filtered = [p for p in filtered if (p["bedrooms"] or 0) >= min_beds]
        if max_beds is not None:
            filtered = [p for p in filtered if (p["bedrooms"] or 99) <= max_beds]
        if furnishing:
            filtered = [p for p in filtered if p["furnishing"].lower() == furnishing.lower()]
        if agent_id:
            filtered = [p for p in filtered if p["agent"]["id"] == agent_id]
        if featured:
            filtered = [p for p in filtered if p["featured"]]
        if status:
            filtered = [p for p in filtered if p["status"].lower() == status.lower()]

        # Sort
        reverse = sort_order != "asc"
        if sort_by == "price":
            filtered.sort(key=lambda p: p["price"], reverse=reverse)
        elif sort_by == "area":
            filtered.sort(key=lambda p: p["area_sqft"], reverse=reverse)
        elif sort_by == "bedrooms":
            filtered.sort(key=lambda p: p["bedrooms"] or 0, reverse=reverse)
        else:
            filtered.sort(key=lambda p: p["listed_date"], reverse=reverse)

        page_items, pagination = _paginate(filtered, page, per_page)

        return _json_response(
            data={"properties": page_items, "filters_applied": {
                "q": q or None, "purpose": purpose, "type": prop_type,
                "community": community, "city": city,
                "min_price": min_price, "max_price": max_price,
                "min_beds": min_beds, "max_beds": max_beds,
                "furnishing": furnishing, "sort_by": sort_by, "sort_order": sort_order,
            }},
            pagination=pagination,
        )

    # ---- single property --------------------------------------------------

    @http.route(
        "/api/v1/property-portal/properties/<int:property_id>",
        type="http", auth="public", methods=["GET"], csrf=False,
        cors="*",
    )
    def property_detail(self, property_id, **params):
        """Detailed view of a single property."""
        prop = next((p for p in PROPERTIES if p["id"] == property_id), None)
        if not prop:
            return _json_response(success=False, message="Property not found", status=404)
        # Enrich with some simulated related info
        enriched = dict(prop)
        enriched["nearby_places"] = _get_nearby_places(prop["latitude"], prop["longitude"])
        enriched["price_history"] = _get_price_history(prop)
        enriched["similar_properties"] = _find_similar(prop, 6)
        return _json_response(data=prop)

    # ---- search -----------------------------------------------------------

    @http.route(
        "/api/v1/property-portal/properties/search",
        type="http", auth="public", methods=["GET"], csrf=False,
        cors="*",
    )
    def property_search(self, **params):
        """Unified search endpoint — delegates to property_list."""
        return self.property_list(**params)

    # ---- locations / autocomplete -----------------------------------------

    @http.route(
        "/api/v1/property-portal/locations",
        type="http", auth="public", methods=["GET"], csrf=False,
        cors="*",
    )
    def location_autocomplete(self, **params):
        """Search communities / areas."""
        q = params.get("q", "").lower().strip()
        results = []
        for comm in COMMUNITIES:
            if not q or q in comm[0].lower() or q in comm[1].lower():
                results.append({
                    "name": comm[0],
                    "city": comm[1],
                    "latitude": comm[2],
                    "longitude": comm[3],
                    "type": comm[4],
                    "listing_count": random.randint(5, 200),
                })
        return _json_response(data={"locations": results[:20]})

    # ---- agents -----------------------------------------------------------

    @http.route(
        "/api/v1/property-portal/agents",
        type="http", auth="public", methods=["GET"], csrf=False,
        cors="*",
    )
    def agent_list(self, **params):
        """Agent directory."""
        page = max(1, _parse_int(params.get("page"), 1))
        per_page = min(50, max(1, _parse_int(params.get("per_page"), 20)))
        q = params.get("q", "").lower().strip()

        filtered = list(AGENTS)
        if q:
            filtered = [
                a for a in filtered
                if q in a["name"].lower() or q in a["company"].lower()
            ]

        page_items, pagination = _paginate(filtered, page, per_page)
        return _json_response(data={"agents": page_items}, pagination=pagination)

    # ---- stats ------------------------------------------------------------

    @http.route(
        "/api/v1/property-portal/stats",
        type="http", auth="public", methods=["GET"], csrf=False,
        cors="*",
    )
    def market_stats(self, **params):
        """Aggregate market statistics."""
        city = params.get("city", "Dubai")
        city_props = [p for p in PROPERTIES if p["city"].lower() == city.lower()]

        avg_price = round(sum(p["price"] for p in city_props) / max(len(city_props), 1))
        avg_rental = round(
            sum(p["price"] for p in city_props if p["purpose"] == "rent")
            / max(sum(1 for p in city_props if p["purpose"] == "rent"), 1)
        )
        avg_sale = round(
            sum(p["price"] for p in city_props if p["purpose"] == "buy")
            / max(sum(1 for p in city_props if p["purpose"] == "buy"), 1)
        )

        type_counts = {}
        for p in city_props:
            type_counts[p["type"]] = type_counts.get(p["type"], 0) + 1

        return _json_response(data={
            "city": city,
            "total_listings": len(city_props),
            "avg_price": avg_price,
            "avg_rental_price": avg_rental,
            "avg_sale_price": avg_sale,
            "price_trend": [
                {
                    "month": f"2026-{m:02d}",
                    "avg_price": round(avg_price * (1 + random.uniform(-0.03, 0.03))),
                    "transaction_count": random.randint(200, 800),
                }
                for m in range(1, 7)
            ],
            "listings_by_type": type_counts,
            "top_communities": sorted(
                [
                    {"name": c[0], "count": sum(1 for p in city_props if p["community"] == c[0])}
                    for c in COMMUNITIES if c[1].lower() == city.lower()
                ],
                key=lambda x: x["count"], reverse=True,
            )[:10],
        })

    # ---- inquiry / lead ---------------------------------------------------

    @http.route(
        "/api/v1/property-portal/inquiry",
        type="http", auth="public", methods=["POST"], csrf=False,
        cors="*",
    )
    def submit_inquiry(self, **params):
        """Submit a lead / inquiry for a property."""
        try:
            data = request.get_json_data()
        except Exception:
            data = params

        name = data.get("name") or data.get("full_name")
        email = data.get("email")
        phone = data.get("phone") or data.get("mobile")
        property_id = _parse_int(data.get("property_id"))
        message = data.get("message") or data.get("notes", "")

        if not name or not email:
            return _json_response(
                success=False, message="Name and email are required", status=400,
            )

        _logger.info(
            "MOCK INQUIRY: name=%s email=%s phone=%s property_id=%s msg=%s",
            name, email, phone, property_id, message,
        )

        return _json_response(
            data={
                "inquiry_id": random.randint(10000, 99999),
                "status": "received",
                "message": f"Thank you {name}! Your inquiry has been received. "
                           f"Our agent will contact you within 24 hours.",
                "created_at": datetime.utcnow().isoformat() + "Z",
            },
            status=201,
        )

    # ---- health -----------------------------------------------------------

    @http.route(
        "/api/v1/property-portal/health",
        type="http", auth="public", methods=["GET"], csrf=False,
        cors="*",
    )
    def health_check(self, **params):
        return _json_response(data={
            "status": "ok",
            "version": "1.0.0",
            "mock": True,
            "total_properties": len(PROPERTIES),
            "total_agents": len(AGENTS),
            "total_communities": len(COMMUNITIES),
        })

    # ---- internal helpers -------------------------------------------------

    def _get_nearby_places(self, lat, lng):
        places = []
        categories = [
            ("School", 500), ("Supermarket", 300), ("Restaurant", 200),
            ("Metro Station", 800), ("Hospital", 1000), ("Park", 400),
            ("Shopping Mall", 600), ("Mosque", 300),
        ]
        for name, dist_m in categories:
            places.append({
                "name": f"{name}",
                "type": name,
                "distance_meters": dist_m + random.randint(-100, 100),
                "walking_minutes": max(1, dist_m // 80 + random.randint(-2, 2)),
            })
        return sorted(places, key=lambda x: x["distance_meters"])

    def _get_price_history(self, prop):
        now = datetime.utcnow()
        return [
            {
                "date": (now - timedelta(days=d)).isoformat() + "Z",
                "price": round(prop["price"] * (1 + random.uniform(-0.05, 0.02))),
                "event": e,
            }
            for d, e in [
                (180, "Listed"),
                (120, "Price Reduced"),
                (60, "Price Reduced"),
                (14, "Latest"),
            ]
        ]

    def _find_similar(self, prop, limit=6):
        similar = [
            p for p in PROPERTIES
            if p["id"] != prop["id"]
            and p["type"] == prop["type"]
            and p["community"] == prop["community"]
        ]
        if len(similar) < limit:
            similar = [
                p for p in PROPERTIES
                if p["id"] != prop["id"]
                and p["type"] == prop["type"]
            ][:limit * 2]
        return [{
            "id": p["id"],
            "title": p["title"],
            "type": p["type"],
            "price": p["price"],
            "bedrooms": p["bedrooms"],
            "bathrooms": p["bathrooms"],
            "area_sqft": p["area_sqft"],
            "community": p["community"],
            "photo": p["photos"][0] if p["photos"] else None,
        } for p in similar[:limit]]


# Export for external consumers
def get_all_properties():
    return list(PROPERTIES)


def get_property(property_id):
    return next((p for p in PROPERTIES if p["id"] == property_id), None)
