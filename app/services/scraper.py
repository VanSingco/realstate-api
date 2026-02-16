from typing import Optional, Any
from datetime import date
import numpy as np
import pandas as pd
from homeharvest import scrape_property

from app.schemas.property import ListingType, SortBy, PropertyType, Property


def is_scalar_na(value: Any) -> bool:
    """Check if a scalar value is NA/NaN/NaT."""
    try:
        if value is None:
            return True
        if isinstance(value, (list, tuple, np.ndarray, dict)):
            return False
        if isinstance(value, float) and np.isnan(value):
            return True
        if isinstance(value, pd.Timestamp) and pd.isna(value):
            return True
        if pd.api.types.is_scalar(value) and pd.isna(value):
            return True
    except (ValueError, TypeError):
        pass
    return False


def convert_value(value: Any) -> Any:
    """Convert numpy/pandas types to Python native types for JSON serialization."""
    if value is None:
        return None
    # Check for scalar NA values
    if is_scalar_na(value):
        return None
    # Convert pandas Timestamp to ISO string
    if isinstance(value, pd.Timestamp):
        return value.isoformat()
    # Convert datetime objects to ISO string
    if hasattr(value, 'isoformat') and callable(value.isoformat):
        return value.isoformat()
    # Convert numpy types to Python types
    if isinstance(value, (np.integer, np.int64, np.int32)):
        return int(value)
    if isinstance(value, (np.floating, np.float64, np.float32)):
        if np.isnan(value):
            return None
        return float(value)
    if isinstance(value, np.bool_):
        return bool(value)
    if isinstance(value, np.ndarray):
        return [convert_value(v) for v in value.tolist()]
    if isinstance(value, (list, tuple)):
        return [convert_value(v) for v in value]
    if isinstance(value, dict):
        return {k: convert_value(v) for k, v in value.items()}
    return value


class ScraperError(Exception):
    """Custom exception for scraper errors."""
    pass


def search_properties(
    location: str,
    listing_type: ListingType,
    past_days: Optional[int] = None,
    past_hours: Optional[int] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    beds_min: Optional[int] = None,
    beds_max: Optional[int] = None,
    baths_min: Optional[float] = None,
    baths_max: Optional[float] = None,
    sqft_min: Optional[int] = None,
    sqft_max: Optional[int] = None,
    price_min: Optional[int] = None,
    price_max: Optional[int] = None,
    year_built_min: Optional[int] = None,
    year_built_max: Optional[int] = None,
    lot_sqft_min: Optional[int] = None,
    lot_sqft_max: Optional[int] = None,
    property_type: Optional[PropertyType] = None,
    radius: Optional[float] = None,
    sort_by: Optional[SortBy] = None,
    limit: Optional[int] = None,
    offset: Optional[int] = None,
    parallel: Optional[bool] = None,
) -> list[Property]:
    """
    Search for properties using HomeHarvest.

    Args:
        location: Location to search (ZIP, city, address, etc.)
        listing_type: Type of listing (for_sale, for_rent, sold, etc.)
        ... (other filters)

    Returns:
        List of Property objects

    Raises:
        ScraperError: If the scraping fails
    """
    try:
        # Build kwargs for scrape_property
        kwargs = {
            "location": location,
            "listing_type": listing_type.value,
        }

        # Add optional time-based filters
        if past_days is not None:
            kwargs["past_days"] = past_days
        if past_hours is not None:
            kwargs["past_hours"] = past_hours
        if date_from is not None:
            kwargs["date_from"] = date_from.strftime("%Y-%m-%d")
        if date_to is not None:
            kwargs["date_to"] = date_to.strftime("%Y-%m-%d")

        # Add optional property filters
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
            kwargs["property_type"] = [property_type.value]

        # Add optional search options
        if radius is not None:
            kwargs["radius"] = radius
        if sort_by is not None:
            kwargs["sort_by"] = sort_by.value
        if limit is not None:
            kwargs["limit"] = limit
        if offset is not None:
            kwargs["offset"] = offset
        if parallel is not None:
            kwargs["parallel"] = parallel

        # Call HomeHarvest scraper
        df: pd.DataFrame = scrape_property(**kwargs)

        # Convert DataFrame to list of Property objects
        if df.empty:
            return []

        # Convert to list of dictionaries
        records = df.to_dict(orient="records")

        # Convert to Property objects
        properties = []
        for record in records:
            # Clean up the record - convert numpy types to Python types
            cleaned = {key: convert_value(value) for key, value in record.items()}
            properties.append(Property(**cleaned))

        return properties

    except Exception as e:
        raise ScraperError(f"Failed to scrape properties: {str(e)}") from e
