from pathlib import Path

from app.backend.schemas import SearchRequest
from app.backend.services import SearchService


def test_search_returns_sorted_by_score_desc() -> None:
    service = SearchService(fixture_path=Path("meetup_spot_planner/data/fixtures/places.sample.json"))
    req = SearchRequest(meetup_point="新宿南口", purpose_tags=["conversation", "quiet"])

    result = service.search(req)

    assert result
    assert result[0].easiness_score >= result[-1].easiness_score
    assert all(p.distance_from_meetup_m <= 800 for p in result)
