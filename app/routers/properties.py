from typing import Optional
from datetime import date
from fastapi import APIRouter, HTTPException, Query

from app.schemas.property import (
    ListingType,
    SortBy,
    PropertyType,
    PropertySearchRequest,
    PropertySearchResponse,
)
from app.services.scraper import search_properties, ScraperError

router = APIRouter(prefix="/properties", tags=["properties"])


@router.get("/search", response_model=PropertySearchResponse)
async def search_properties_get(
    location: str = Query(
        ...,
        description="Location to search (ZIP code, city, 'city, state', address, or neighborhood)",
        examples=["San Francisco, CA", "90210"]
    ),
    listing_type: ListingType = Query(
        ...,
        description="Type of listing to search for"
    ),
    past_days: Optional[int] = Query(None, ge=1, description="Only show listings from the past N days"),
    past_hours: Optional[int] = Query(None, ge=1, description="Only show listings from the past N hours"),
    date_from: Optional[date] = Query(None, description="Start date for listing search (YYYY-MM-DD)"),
    date_to: Optional[date] = Query(None, description="End date for listing search (YYYY-MM-DD)"),
    beds_min: Optional[int] = Query(None, ge=0, description="Minimum number of bedrooms"),
    beds_max: Optional[int] = Query(None, ge=0, description="Maximum number of bedrooms"),
    baths_min: Optional[float] = Query(None, ge=0, description="Minimum number of bathrooms"),
    baths_max: Optional[float] = Query(None, ge=0, description="Maximum number of bathrooms"),
    sqft_min: Optional[int] = Query(None, ge=0, description="Minimum square footage"),
    sqft_max: Optional[int] = Query(None, ge=0, description="Maximum square footage"),
    price_min: Optional[int] = Query(None, ge=0, description="Minimum price"),
    price_max: Optional[int] = Query(None, ge=0, description="Maximum price"),
    year_built_min: Optional[int] = Query(None, ge=1800, description="Minimum year built"),
    year_built_max: Optional[int] = Query(None, le=2030, description="Maximum year built"),
    lot_sqft_min: Optional[int] = Query(None, ge=0, description="Minimum lot square footage"),
    lot_sqft_max: Optional[int] = Query(None, ge=0, description="Maximum lot square footage"),
    property_type: Optional[PropertyType] = Query(None, description="Type of property (single_family, multi_family, condo, townhouse, land, other)"),
    radius: Optional[float] = Query(None, ge=0, description="Search radius in miles"),
    sort_by: Optional[SortBy] = Query(None, description="Sort results by this field"),
    limit: Optional[int] = Query(None, ge=1, le=10000, description="Maximum results (max 10,000)"),
    offset: Optional[int] = Query(None, ge=0, description="Starting position for pagination"),
    parallel: Optional[bool] = Query(None, description="Pagination strategy (True=parallel, False=sequential)"),
):
    """
    Search for properties using query parameters.

    This endpoint is ideal for simple searches with a few filters.
    For complex queries with many parameters, use POST /properties/search instead.
    """
    try:
        # Build kwargs with only provided parameters
        kwargs = {
            "location": location,
            "listing_type": listing_type,
        }
        if past_days is not None:
            kwargs["past_days"] = past_days
        if past_hours is not None:
            kwargs["past_hours"] = past_hours
        if date_from is not None:
            kwargs["date_from"] = date_from
        if date_to is not None:
            kwargs["date_to"] = date_to
        if beds_min is not None:
            kwargs["beds_min"] = beds_min
        if beds_max is not None:
            kwargs["beds_max"] = beds_max
        if baths_min is not None:
            kwargs["baths_min"] = baths_min
        if baths_max is not None:
            kwargs["baths_max"] = baths_max
        if sqft_min is not None:
            kwargs["sqft_min"] = sqft_min
        if sqft_max is not None:
            kwargs["sqft_max"] = sqft_max
        if price_min is not None:
            kwargs["price_min"] = price_min
        if price_max is not None:
            kwargs["price_max"] = price_max
        if year_built_min is not None:
            kwargs["year_built_min"] = year_built_min
        if year_built_max is not None:
            kwargs["year_built_max"] = year_built_max
        if lot_sqft_min is not None:
            kwargs["lot_sqft_min"] = lot_sqft_min
        if lot_sqft_max is not None:
            kwargs["lot_sqft_max"] = lot_sqft_max
        if property_type is not None:
            kwargs["property_type"] = property_type
        if radius is not None:
            kwargs["radius"] = radius
        if sort_by is not None:
            kwargs["sort_by"] = sort_by
        if limit is not None:
            kwargs["limit"] = limit
        if offset is not None:
            kwargs["offset"] = offset
        if parallel is not None:
            kwargs["parallel"] = parallel

        properties = search_properties(**kwargs)
        return PropertySearchResponse(count=len(properties), properties=properties, total_count=len(properties))
    except ScraperError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


@router.post("/search", response_model=PropertySearchResponse)
async def search_properties_post(request: PropertySearchRequest):
    """
    Search for properties using a request body.

    This endpoint is ideal for complex searches with many filters.
    All parameters are passed in the JSON body.
    """
    try:
        # Build kwargs with only provided parameters
        kwargs = {
            "location": request.location,
            "listing_type": request.listing_type,
        }
        if request.past_days is not None:
            kwargs["past_days"] = request.past_days
        if request.past_hours is not None:
            kwargs["past_hours"] = request.past_hours
        if request.date_from is not None:
            kwargs["date_from"] = request.date_from
        if request.date_to is not None:
            kwargs["date_to"] = request.date_to
        if request.beds_min is not None:
            kwargs["beds_min"] = request.beds_min
        if request.beds_max is not None:
            kwargs["beds_max"] = request.beds_max
        if request.baths_min is not None:
            kwargs["baths_min"] = request.baths_min
        if request.baths_max is not None:
            kwargs["baths_max"] = request.baths_max
        if request.sqft_min is not None:
            kwargs["sqft_min"] = request.sqft_min
        if request.sqft_max is not None:
            kwargs["sqft_max"] = request.sqft_max
        if request.price_min is not None:
            kwargs["price_min"] = request.price_min
        if request.price_max is not None:
            kwargs["price_max"] = request.price_max
        if request.year_built_min is not None:
            kwargs["year_built_min"] = request.year_built_min
        if request.year_built_max is not None:
            kwargs["year_built_max"] = request.year_built_max
        if request.lot_sqft_min is not None:
            kwargs["lot_sqft_min"] = request.lot_sqft_min
        if request.lot_sqft_max is not None:
            kwargs["lot_sqft_max"] = request.lot_sqft_max
        if request.property_type is not None:
            kwargs["property_type"] = request.property_type
        if request.radius is not None:
            kwargs["radius"] = request.radius
        if request.sort_by is not None:
            kwargs["sort_by"] = request.sort_by
        if request.limit is not None:
            kwargs["limit"] = request.limit
        if request.offset is not None:
            kwargs["offset"] = request.offset
        if request.parallel is not None:
            kwargs["parallel"] = request.parallel

        properties = search_properties(**kwargs)
        return PropertySearchResponse(count=len(properties), properties=properties, total_count=len(properties))
    except ScraperError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
