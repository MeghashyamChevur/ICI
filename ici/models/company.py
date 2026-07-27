"""Company model definitions."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True)
class Company:
    """Represents a company record used by collectors and validators."""

    symbol: str
    company_name: str
    isin: Optional[str] = None
    nse_code: Optional[str] = None
    bse_code: Optional[str] = None
    sector: Optional[str] = None
    industry: Optional[str] = None
    exchange: Optional[str] = None
    listing_status: Optional[str] = None
    market_cap: Optional[float] = None
    market_cap_category: Optional[str] = None
    listing_date: Optional[str] = None
    face_value: Optional[float] = None
    website: Optional[str] = None
    headquarters: Optional[str] = None
    business_description: Optional[str] = None
