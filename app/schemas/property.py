from enum import Enum
from typing import Optional, Any
from datetime import date
from pydantic import BaseModel, Field


class ListingType(str, Enum):
    FOR_SALE = "for_sale"
    FOR_RENT = "for_rent"
    SOLD = "sold"
    PENDING = "pending"
    OFF_MARKET = "off_market"


class SortBy(str, Enum):
    LIST_DATE = "list_date"
    LIST_PRICE = "list_price"
    SQFT = "sqft"
    BEDS = "beds"
    BATHS = "baths"
    LAST_UPDATE_DATE = "last_update_date"


class PropertyType(str, Enum):
    SINGLE_FAMILY = "single_family"
    MULTI_FAMILY = "multi_family"
    CONDO = "condo"
    TOWNHOUSE = "townhouse"
    LAND = "land"
    OTHER = "other"


class PropertySearchRequest(BaseModel):
    """Request model for property search with all HomeHarvest parameters."""

    location: str = Field(
        ...,
        description="Location to search (ZIP code, city, 'city, state', address, or neighborhood)",
        examples=["San Francisco, CA", "90210", "123 Main St, Los Angeles, CA"]
    )
    listing_type: ListingType = Field(
        ...,
        description="Type of listing to search for"
    )

    # Time-based filters
    past_days: Optional[int] = Field(
        None,
        ge=1,
        description="Only show listings from the past N days"
    )
    past_hours: Optional[int] = Field(
        None,
        ge=1,
        description="Only show listings from the past N hours"
    )
    date_from: Optional[date] = Field(
        None,
        description="Start date for listing search (YYYY-MM-DD)"
    )
    date_to: Optional[date] = Field(
        None,
        description="End date for listing search (YYYY-MM-DD)"
    )

    # Property filters
    beds_min: Optional[int] = Field(None, ge=0, description="Minimum number of bedrooms")
    beds_max: Optional[int] = Field(None, ge=0, description="Maximum number of bedrooms")
    baths_min: Optional[float] = Field(None, ge=0, description="Minimum number of bathrooms")
    baths_max: Optional[float] = Field(None, ge=0, description="Maximum number of bathrooms")
    sqft_min: Optional[int] = Field(None, ge=0, description="Minimum square footage")
    sqft_max: Optional[int] = Field(None, ge=0, description="Maximum square footage")
    price_min: Optional[int] = Field(None, ge=0, description="Minimum price")
    price_max: Optional[int] = Field(None, ge=0, description="Maximum price")
    year_built_min: Optional[int] = Field(None, ge=1800, description="Minimum year built")
    year_built_max: Optional[int] = Field(None, le=2030, description="Maximum year built")
    lot_sqft_min: Optional[int] = Field(None, ge=0, description="Minimum lot square footage")
    lot_sqft_max: Optional[int] = Field(None, ge=0, description="Maximum lot square footage")
    property_type: Optional[PropertyType] = Field(
        None,
        description="Type of property (single_family, multi_family, condo, townhouse, land, other)"
    )

    # Search options
    radius: Optional[float] = Field(
        None,
        ge=0,
        description="Search radius in miles from the location"
    )
    sort_by: Optional[SortBy] = Field(
        None,
        description="Sort results by this field"
    )
    limit: Optional[int] = Field(
        None,
        ge=1,
        le=10000,
        description="Maximum number of results to return (max 10,000)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "location": "San Francisco, CA",
                    "listing_type": "for_sale",
                    "beds_min": 2,
                    "beds_max": 4,
                    "price_max": 1500000,
                    "sort_by": "list_price",
                    "limit": 100
                }
            ]
        }
    }


class Property(BaseModel):
    """Individual property data from HomeHarvest."""

    # Basic Information
    property_url: Optional[str] = None
    property_id: Optional[str] = None
    listing_id: Optional[str] = None
    mls: Optional[str] = None
    mls_id: Optional[str] = None
    mls_status: Optional[str] = None
    status: Optional[str] = None
    permalink: Optional[str] = None

    # Address Details
    street: Optional[str] = None
    unit: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None

    # Property Description
    style: Optional[str] = None
    beds: Optional[int] = None
    full_baths: Optional[int] = None
    half_baths: Optional[int] = None
    sqft: Optional[int] = None
    year_built: Optional[int] = None
    stories: Optional[int] = None
    garage: Optional[int] = None
    lot_sqft: Optional[int] = None
    text: Optional[str] = None
    type: Optional[str] = None

    # Property Listing Details
    days_on_mls: Optional[int] = None
    list_price: Optional[int] = None
    list_price_min: Optional[int] = None
    list_price_max: Optional[int] = None
    list_date: Optional[str] = None
    pending_date: Optional[str] = None
    sold_price: Optional[int] = None
    last_sold_date: Optional[str] = None
    last_status_change_date: Optional[str] = None
    last_update_date: Optional[str] = None
    last_sold_price: Optional[int] = None
    price_per_sqft: Optional[float] = None
    new_construction: Optional[bool] = None
    hoa_fee: Optional[int] = None
    monthly_fees: Optional[Any] = None
    one_time_fees: Optional[Any] = None
    estimated_value: Optional[int] = None

    # Tax Information
    tax_assessed_value: Optional[int] = None
    tax_history: Optional[Any] = None

    # Location Details
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    neighborhoods: Optional[str] = None
    county: Optional[str] = None
    fips_code: Optional[str] = None
    parcel_number: Optional[str] = None
    nearby_schools: Optional[Any] = None

    # Agent/Broker/Office Info
    agent_uuid: Optional[str] = None
    agent_name: Optional[str] = None
    agent_email: Optional[str] = None
    agent_phone: Optional[str] = None
    agent_state_license: Optional[str] = None
    broker_uuid: Optional[str] = None
    broker_name: Optional[str] = None
    office_uuid: Optional[str] = None
    office_name: Optional[str] = None
    office_email: Optional[str] = None
    office_phones: Optional[Any] = None

    # Additional Fields
    estimated_monthly_rental: Optional[int] = None
    tags: Optional[Any] = None
    flags: Optional[Any] = None
    photos: Optional[Any] = None
    primary_photo: Optional[str] = None
    alt_photos: Optional[Any] = None
    open_houses: Optional[Any] = None
    units: Optional[Any] = None
    pet_policy: Optional[Any] = None
    parking: Optional[Any] = None
    parking_garage: Optional[int] = None
    terms: Optional[Any] = None
    current_estimates: Optional[Any] = None
    estimates: Optional[Any] = None


class PropertySearchResponse(BaseModel):
    """Response model for property search."""

    count: int = Field(..., description="Number of properties returned")
    properties: list[Property] = Field(..., description="List of properties")
