from infra.maps.google_places_adapter import normalize_nearby_search_response


def test_normalize_google_places_new_response() -> None:
    payload = {
        "places": [
            {
                "id": "ChI123",
                "displayName": {"text": "Cafe Example"},
                "location": {"latitude": 35.68, "longitude": 139.70},
                "types": ["cafe", "food"],
                "currentOpeningHours": {"openNow": True},
            }
        ]
    }

    out = normalize_nearby_search_response(payload)

    assert len(out) == 1
    assert out[0]["place_id"] == "ChI123"
    assert out[0]["name"] == "Cafe Example"
    assert out[0]["category"] == "cafe"
    assert out[0]["open_status"] is True
