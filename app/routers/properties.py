from typing import Optional
from datetime import date
from fastapi import APIRouter, HTTPException, Query

from app.schemas.property import (
    ListingType,
    SortBy,
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
    radius: Optional[float] = Query(None, ge=0, description="Search radius in miles"),
    sort_by: Optional[SortBy] = Query(None, description="Sort results by this field"),
    limit: Optional[int] = Query(None, ge=1, le=10000, description="Maximum results (max 10,000)"),
):
    """
    Search for properties using query parameters.

    This endpoint is ideal for simple searches with a few filters.
    For complex queries with many parameters, use POST /properties/search instead.
    """
    try:
        properties = search_properties(
            location=location,
            listing_type=listing_type,
            past_days=past_days,
            past_hours=past_hours,
            date_from=date_from,
            date_to=date_to,
            beds_min=beds_min,
            beds_max=beds_max,
            baths_min=baths_min,
            baths_max=baths_max,
            sqft_min=sqft_min,
            sqft_max=sqft_max,
            price_min=price_min,
            price_max=price_max,
            year_built_min=year_built_min,
            year_built_max=year_built_max,
            lot_sqft_min=lot_sqft_min,
            lot_sqft_max=lot_sqft_max,
            radius=radius,
            sort_by=sort_by,
            limit=limit,
        )
        return PropertySearchResponse(count=len(properties), properties=properties)
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
        properties = search_properties(
            location=request.location,
            listing_type=request.listing_type,
            past_days=request.past_days,
            past_hours=request.past_hours,
            date_from=request.date_from,
            date_to=request.date_to,
            beds_min=request.beds_min,
            beds_max=request.beds_max,
            baths_min=request.baths_min,
            baths_max=request.baths_max,
            sqft_min=request.sqft_min,
            sqft_max=request.sqft_max,
            price_min=request.price_min,
            price_max=request.price_max,
            year_built_min=request.year_built_min,
            year_built_max=request.year_built_max,
            lot_sqft_min=request.lot_sqft_min,
            lot_sqft_max=request.lot_sqft_max,
            radius=request.radius,
            sort_by=request.sort_by,
            limit=request.limit,
        )
        return PropertySearchResponse(count=len(properties), properties=properties)
    except ScraperError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")
