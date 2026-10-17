
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl


class Venue(BaseModel):
    name: str
    website_url: Optional[HttpUrl] = None
    source_urls: list[str] = Field(default_factory=list)

    address: Optional[str] = None
    area: Optional[str] = None

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
