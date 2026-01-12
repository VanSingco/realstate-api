from fastapi import APIRouter, HTTPException

from app.schemas.property import (
    PropertySearchRequest,
    PropertySearchResponse,
)
from app.services.scraper import search_properties, ScraperError

router = APIRouter(prefix="/properties", tags=["properties"])


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
