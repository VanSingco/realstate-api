# Real Estate API

A FastAPI REST API that wraps the [HomeHarvest](https://github.com/ZacharyHampton/HomeHarvest) Python library to scrape real estate property data from Realtor.com.

## Installation

1. **Clone and navigate to the project:**
   ```bash
   cd C:\laragon\www\realstate-api
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # Windows (PowerShell/CMD)
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Configure environment (optional):**
   ```bash
   cp .env.example .env
   # Edit .env to set CORS_ORIGINS if needed
   ```

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

- **API Documentation (Swagger UI):** http://localhost:8000/docs
- **Alternative Docs (ReDoc):** http://localhost:8000/redoc

## API Endpoints

### Health Check

```
GET /health
```

Returns API status.

**Response:**
```json
{
  "status": "healthy",
  "service": "realstate-api"
}
```

---

### Search Properties (GET)

```
GET /properties/search
```

Search properties using query parameters. Best for simple searches.

**Required Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `location` | string | ZIP code, city, "city, state", address, or neighborhood |
| `listing_type` | string | `for_sale`, `for_rent`, `sold`, `pending`, `off_market` |

**Optional Filters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `past_days` | int | Only listings from the past N days |
| `past_hours` | int | Only listings from the past N hours |
| `date_from` | date | Start date (YYYY-MM-DD) |
| `date_to` | date | End date (YYYY-MM-DD) |
| `beds_min` | int | Minimum bedrooms |
| `beds_max` | int | Maximum bedrooms |
| `baths_min` | float | Minimum bathrooms |
| `baths_max` | float | Maximum bathrooms |
| `sqft_min` | int | Minimum square footage |
| `sqft_max` | int | Maximum square footage |
| `price_min` | int | Minimum price |
| `price_max` | int | Maximum price |
| `year_built_min` | int | Minimum year built |
| `year_built_max` | int | Maximum year built |
| `lot_sqft_min` | int | Minimum lot square footage |
| `lot_sqft_max` | int | Maximum lot square footage |
| `radius` | float | Search radius in miles |
| `sort_by` | string | `list_date`, `list_price`, `sqft`, `beds`, `baths`, `last_update_date` |
| `limit` | int | Maximum results (max 10,000) |

---

### Search Properties (POST)

```
POST /properties/search
```

Search properties using a JSON request body. Best for complex searches with many filters.

**Request Body:**
```json
{
  "location": "San Francisco, CA",
  "listing_type": "for_sale",
  "beds_min": 2,
  "beds_max": 4,
  "baths_min": 2,
  "price_min": 500000,
  "price_max": 1500000,
  "sqft_min": 1200,
  "sort_by": "list_price",
  "limit": 100
}
```

---

## Example Requests

### Basic search - properties for sale in Beverly Hills
```bash
curl "http://localhost:8000/properties/search?location=90210&listing_type=for_sale"
```

### Search with filters - 2+ beds, under $2M
```bash
curl "http://localhost:8000/properties/search?location=San%20Francisco,%20CA&listing_type=for_sale&beds_min=2&price_max=2000000"
```

### Rentals in Austin
```bash
curl "http://localhost:8000/properties/search?location=Austin,%20TX&listing_type=for_rent&beds_min=1&beds_max=2"
```

### Recently sold (last 30 days)
```bash
curl "http://localhost:8000/properties/search?location=Miami,%20FL&listing_type=sold&past_days=30"
```

### POST request with complex filters
```bash
curl -X POST http://localhost:8000/properties/search \
  -H "Content-Type: application/json" \
  -d '{
    "location": "San Francisco, CA",
    "listing_type": "for_sale",
    "beds_min": 2,
    "beds_max": 4,
    "baths_min": 2,
    "price_min": 500000,
    "price_max": 1500000,
    "sqft_min": 1200,
    "sort_by": "list_price",
    "limit": 50
  }'
```

---

## Response Format

```json
{
  "count": 25,
  "properties": [
    {
      "property_url": "https://www.realtor.com/...",
      "property_id": "1234567890",
      "mls": "CRMLS",
      "mls_id": "ABC123",
      "status": "for_sale",
      "street": "123 Main St",
      "unit": null,
      "city": "Beverly Hills",
      "state": "CA",
      "zip_code": "90210",
      "beds": 3,
      "full_baths": 2,
      "half_baths": 1,
      "sqft": 1800,
      "year_built": 1990,
      "lot_sqft": 5000,
      "list_price": 1250000,
      "list_date": "2024-01-15T00:00:00",
      "days_on_mls": 15,
      "price_per_sqft": 694.44,
      "latitude": 34.0736,
      "longitude": -118.4004,
      "primary_photo": "https://...",
      "agent_name": "John Smith",
      "agent_phone": "(555) 123-4567",
      "office_name": "Luxury Realty",
      "text": "Beautiful 3-bedroom home with modern updates...",
      ...
    }
  ]
}
```

## Property Fields

The API returns comprehensive property data including:

- **Basic Info:** property_url, property_id, listing_id, mls, mls_id, status, permalink
- **Address:** street, unit, city, state, zip_code
- **Description:** style, beds, full_baths, half_baths, sqft, year_built, stories, garage, lot_sqft, text, type
- **Listing Details:** list_price, list_date, sold_price, last_sold_date, days_on_mls, price_per_sqft, hoa_fee, estimated_value
- **Location:** latitude, longitude, neighborhoods, county, fips_code, parcel_number
- **Agent/Broker:** agent_name, agent_email, agent_phone, broker_name, office_name, office_email, office_phones
- **Additional:** photos, primary_photo, alt_photos, tags, flags, open_houses, tax_assessed_value, nearby_schools

## Tech Stack

- **FastAPI** - Modern Python web framework
- **HomeHarvest** - Real estate data scraping library
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## License

MIT
