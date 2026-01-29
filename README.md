# FastAPI Project with PostgreSQL Database

A FastAPI application for managing product and user events with PostgreSQL database integration.

## Project Structure

```
.
├── main.py              # FastAPI application with event endpoints
├── database.py          # Database configuration and table definitions
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── .dockerignore        # Files to exclude from Docker build
├── .gitignore          # Files to exclude from git
└── README.md           # This file
```

## Prerequisites

- Docker and Docker Compose (optional)
- Python 3.9+ (if running locally)
- PostgreSQL 13+ (if running locally)

## Features

- **Product Events API**: Track product-related events with comprehensive metadata
- **User Events API**: Monitor user activities
- **Automatic API Documentation**: Interactive Swagger UI and ReDoc
- **Async Database Support**: Efficient async/await pattern with SQLAlchemy
- **Type Safety**: Pydantic models for request/response validation

## Quick Start with Docker

### 1. Build the Docker Image

```bash
docker build -t fastapi-app .
```

### 2. Run the Container

```bash
docker run -d -p 8000:8000 --name fastapi-container fastapi-app
```

### 3. Access the Application

- **API Root**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Running Locally

### 1. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up PostgreSQL

Ensure PostgreSQL is running and create a database. The default connection string in `database.py` is:

```
postgresql://postgres:postgres@localhost:5432/reporting
```

Modify `DATABASE_URL` in `database.py` if needed.

### 4. Run the Application

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints

### Lost Products

**GET** `/lost-products/`

- **Description**: Retrieve products that have been borrowed for more than 3 months
- **Response**: List of ProductLost objects (product_id only)
- **Query Logic**: Filters for products with the latest event type of 'borrow' and event date older than 3 months

Example response:

```json
[
  {
    "product_id": "1"
  },
  {
    "product_id": "2"
  }
]
```

### Unreturned Products with Expiring Payment Methods

**GET** `/unreturned-products/`

- **Description**: Retrieve unreturned borrowed products where the user's payment method is expiring within 30 days
- **Response**: List of unreturned product objects with payment method expiration dates
- **Query Logic**:
  - Finds products with latest event type of 'borrow'
  - Matches with users' latest payment method information
  - Filters for payment methods expiring within 30 days

Example response:

```json
[
  {
    "product_id": "1"
  },
  {
    "product_id": "2"
  }
]
```

### Product Events

**GET** `/product-events/`

- **Description**: Retrieve all product events from the database
- **Response**: List of ProductEvent objects
- **Status Codes**:
  - `200 OK` - Successfully retrieved events
  - `500 Internal Server Error` - Database connection error

Example response:

```json
[
  {
    "id": 1,
    "evt_type": "borrow",
    "user_id": "user123",
    "product_id": "prod456",
    "location_id": "loc789",
    "location": "Warehouse A",
    "evt_date": "2024-01-15T10:30:00",
    "transaction_id": "txn001",
    "platform": "web",
    "meta": null,
    "created": "2024-01-15T10:30:00",
    "last_modified": "2024-01-15T10:30:00"
  }
]
```

### User Events

**GET** `/user-events/`

- **Description**: Retrieve all user events from the database
- **Response**: List of UserEvent objects
- **Status Codes**:
  - `200 OK` - Successfully retrieved events
  - `500 Internal Server Error` - Database connection error

Example response:

```json
[
  {
    "id": 1,
    "evt_type": "add-payment-method",
    "user_id": "user123",
    "evt_date": "2024-01-10T14:20:00",
    "platform": "mobile",
    "meta": "{\"valid_until\": \"12/25\"}",
    "created": "2024-01-10T14:20:00",
    "last_modified": "2024-01-10T14:20:00"
  }
]
```

## Data Models

### ProductEvent

```python
{
  "id": int,
  "evt_type": str,
  "user_id": str,
  "product_id": str,
  "location_id": str,
  "location": str,
  "evt_date": datetime,
  "transaction_id": str,
  "platform": str,
  "meta": str,
  "created": datetime,
  "last_modified": datetime
}
```

### UserEvent

```python
{
  "id": int,
  "evt_type": str,
  "user_id": str,
  "evt_date": datetime,
  "platform": str,
  "meta": str,
  "created": datetime,
  "last_modified": datetime
}
```

## Common Queries

### Find Lost Products

Products with unreturned borrows for 3+ months:

```sql
WITH latest_events AS (
  SELECT
    product_id,
    evt_type,
    evt_date,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY evt_date DESC) as rn
  FROM product_events
)
SELECT product_id
FROM latest_events
WHERE rn = 1
  AND evt_type = 'borrow'
  AND evt_date <= NOW() - INTERVAL '3 months'
ORDER BY product_id;
```

### Find Unreturned Products with Expiring Payment Methods

Products not yet returned where user payment expires within 30 days:

```sql
WITH latest_product_events AS (
  SELECT
    product_id,
    user_id,
    evt_type,
    ROW_NUMBER() OVER (PARTITION BY product_id ORDER BY evt_date DESC) as rn
  FROM product_events
),
unreturned_borrows AS (
  SELECT product_id, user_id
  FROM latest_product_events
  WHERE rn = 1 AND evt_type = 'borrow'
),
latest_payment_methods AS (
  SELECT
    user_id,
    meta,
    ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY evt_date DESC) as rn
  FROM user_events
  WHERE evt_type = 'add-payment-method'
)
SELECT
  ub.product_id,
  ub.user_id,
  lpm.meta
FROM unreturned_borrows ub
JOIN latest_payment_methods lpm ON ub.user_id = lpm.user_id
WHERE lpm.rn = 1
  AND TO_DATE(SUBSTRING(lpm.meta FROM '"valid_until": "([^"]+)"'), 'MM/YY')
      <= NOW() + INTERVAL '30 days'
ORDER BY ub.product_id;
```

## Docker Commands

```bash
# View running containers
docker ps

# Stop container
docker stop fastapi-container

# Start container
docker start fastapi-container

# View logs
docker logs -f fastapi-container

# Remove container
docker rm fastapi-container

# Remove image
docker rmi fastapi-app
```

## Dependencies

- **fastapi** (0.104.1) - Web framework
- **uvicorn** (0.24.0) - ASGI server
- **SQLAlchemy** (2.0.23) - ORM
- **databases** (0.8.0) - Async database support
- **psycopg2-binary** (2.9.9) - PostgreSQL adapter

## Troubleshooting

### Port Already in Use

Map to a different port:

```bash
docker run -d -p 8001:8000 --name fastapi-container fastapi-app
```

Access at `http://localhost:8001`

### Database Connection Error

Verify PostgreSQL is running and the connection string in `database.py` is correct.

### Import Errors

Ensure all dependencies are installed:

```bash
pip install -r requirements.txt
```

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
