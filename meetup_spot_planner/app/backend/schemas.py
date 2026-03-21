from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

CrowdLevel = Literal["low", "medium", "high"]
ReservationStatus = Literal["bookable", "call", "unknown"]


class SearchRequest(BaseModel):
    meetup_point: str = Field(..., min_length=1, description="待ち合わせ地点")
    time: str | None = Field(default=None, description="利用時刻(簡易) " )
    headcount: int | None = Field(default=None, ge=1, le=20)
    purpose_tags: list[str] = Field(default_factory=list)


class Place(BaseModel):
    place_id: str
    name: str
    lat: float
    lng: float
    category: str
    open_status: bool
    reservation_status: ReservationStatus
    crowd_estimation: CrowdLevel
    atmosphere_tags: list[str]
    distance_from_meetup_m: int
    easiness_score: float = 0.0
    recommendation_reason: str = ""


class SearchResponse(BaseModel):
    meetup_point: str
    map_markers: list[Place]
    ranked_places: list[Place]
