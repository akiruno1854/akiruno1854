from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .schemas import SearchRequest, SearchResponse
from .services import SearchService

app = FastAPI(title="Meetup Spot Planner MVP")
service = SearchService()

frontend_dir = Path(__file__).resolve().parents[1] / "frontend"
app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.get("/", include_in_schema=False)
def index() -> FileResponse:
    return FileResponse(frontend_dir / "index.html")


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/search", response_model=SearchResponse)
def search(payload: SearchRequest) -> SearchResponse:
    places = service.search(payload)
    return SearchResponse(
        meetup_point=payload.meetup_point,
        map_markers=places,
        ranked_places=places,
    )
