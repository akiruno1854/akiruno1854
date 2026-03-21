from __future__ import annotations

from pathlib import Path
import json

from .schemas import Place, SearchRequest

FIXTURE_PATH = Path(__file__).resolve().parents[2] / "data" / "fixtures" / "places.sample.json"

CROWD_SCORE = {"low": 30, "medium": 15, "high": 0}
RESERVATION_SCORE = {"bookable": 30, "call": 15, "unknown": 5}


class SearchService:
    def __init__(self, fixture_path: Path = FIXTURE_PATH) -> None:
        self.fixture_path = fixture_path

    def load_places(self) -> list[Place]:
        rows = json.loads(self.fixture_path.read_text(encoding="utf-8"))
        return [Place(**row) for row in rows]

    def score_place(self, place: Place, request: SearchRequest) -> Place:
        score = 100.0
        score -= min(place.distance_from_meetup_m / 20, 50)
        score += 10 if place.open_status else -40
        score += CROWD_SCORE[place.crowd_estimation]
        score += RESERVATION_SCORE[place.reservation_status]

        if request.purpose_tags:
            overlap = len(set(request.purpose_tags) & set(place.atmosphere_tags))
            score += overlap * 8

        reason_parts: list[str] = []
        if place.distance_from_meetup_m <= 500:
            reason_parts.append("駅近")
        if place.reservation_status == "bookable":
            reason_parts.append("予約可")
        if place.crowd_estimation == "low":
            reason_parts.append("混雑低")

        place.easiness_score = round(score, 1)
        place.recommendation_reason = "・".join(reason_parts) if reason_parts else "条件適合"
        return place

    def search(self, request: SearchRequest) -> list[Place]:
        places = self.load_places()

        filtered = [
            p
            for p in places
            if p.distance_from_meetup_m <= 800 and p.category in {"cafe", "restaurant", "bar"}
        ]

        scored = [self.score_place(p, request) for p in filtered]
        return sorted(scored, key=lambda p: p.easiness_score, reverse=True)
