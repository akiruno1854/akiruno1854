from __future__ import annotations

from typing import Any


def normalize_nearby_search_response(payload: dict[str, Any]) -> list[dict[str, Any]]:
    """Normalize Google Places API (New) Nearby Search response to internal format.

    Expected upstream top-level shape:
    {
      "places": [
        {
          "id": "...",
          "displayName": {"text": "..."},
          "location": {"latitude": 35.0, "longitude": 139.0},
          "types": ["cafe", "restaurant"],
          "currentOpeningHours": {"openNow": true}
        }
      ]
    }
    """

    places = payload.get("places", [])
    normalized: list[dict[str, Any]] = []

    for p in places:
        location = p.get("location", {})
        display_name = p.get("displayName", {})

        lat = location.get("latitude")
        lng = location.get("longitude")
        if lat is None or lng is None:
            continue

        types = p.get("types", [])
        category = "restaurant"
        if "cafe" in types:
            category = "cafe"
        elif "bar" in types:
            category = "bar"

        normalized.append(
            {
                "place_id": p.get("id") or p.get("name", ""),
                "name": display_name.get("text") or "Unknown place",
                "lat": float(lat),
                "lng": float(lng),
                "category": category,
                "open_status": bool(p.get("currentOpeningHours", {}).get("openNow", False)),
                "reservation_status": "unknown",
                "crowd_estimation": "medium",
                "atmosphere_tags": [],
                "distance_from_meetup_m": 999,
            }
        )

    return normalized
