
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class BookingProvider(BaseModel):
    """An intermediary that helps book venues; it is not a venue record."""

    name: str
    website_url: HttpUrl
    service_area: Optional[str] = None
    discovery_source: str = "web_search"


class Venue(BaseModel):
    name: str
    website_url: Optional[HttpUrl] = None
    source_urls: list[str] = Field(default_factory=list)

    google_place_id: Optional[str] = None
    google_maps_url: Optional[HttpUrl] = None
    address: Optional[str] = None
    area: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    google_rating: Optional[float] = None
    google_review_count: Optional[int] = None
    place_types: list[str] = Field(default_factory=list)
    discovery_source: str = "unknown"

    capacity_min: Optional[int] = None
    capacity_max: Optional[int] = None

    published_price: Optional[float] = None
    price_currency: str = "INR"
    price_notes: Optional[str] = None

    wifi: Optional[bool] = None
    power_outlets: Optional[bool] = None
    projector_or_display: Optional[bool] = None
    catering: Optional[bool] = None
    parking: Optional[bool] = None

    contact_phone: Optional[str] = None
    contact_email: Optional[str] = None

    date_availability: Optional[str] = None
    evidence_notes: list[str] = Field(default_factory=list)
    unknown_fields: list[str] = Field(default_factory=list)

    research_status: str = "not_researched"
    match_score: Optional[float] = None
    match_reasons: list[str] = Field(default_factory=list)
