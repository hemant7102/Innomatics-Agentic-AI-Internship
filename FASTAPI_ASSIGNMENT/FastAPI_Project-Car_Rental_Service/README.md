# Car Rental API (FastAPI)

A minimal, functional REST API for managing car listings with filtering, sorting, and pagination. Built as part of a backend assignment to demonstrate API design fundamentals using FastAPI.

---

## What This Project Does

This API allows you to:

* Retrieve available cars
* Filter cars based on price
* Sort cars in ascending or descending order
* Apply pagination to large datasets
* Simulate basic booking functionality

No database is used — data is handled via in-memory structures / JSON.

---

## Why This Exists

This project focuses on:

* Understanding how REST APIs work
* Practicing query parameters (filtering, sorting, pagination)
* Learning FastAPI fundamentals
* Structuring backend logic cleanly

---

## Tech Used

* Python 3.x
* FastAPI
* Uvicorn
* Pydantic

---

## Project Structure

```bash
.
├── main.py
├── requirements.txt
├── README.md
└── venv/   # not included in repo
```

---

## How to Run

### 1. Clone the repo

```bash
git clone <your-repo-link>
cd <project-folder>
```

### 2. Create virtual environment

```bash
python -m venv venv
```

### 3. Activate it

```bash
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Start server

```bash
uvicorn main:app --reload
```

---

## API Endpoints

### Get all cars

```
GET /cars
```

### Filter by price

```
GET /cars/filter?max_price=2000
```

### Sort cars

```
GET /cars/sort?order=asc
GET /cars/sort?order=desc
```

### Pagination

```
GET /cars?page=1&limit=5
```

### Book a car

```
POST /book
```

---

## Testing

Open in browser:

```
http://127.0.0.1:8000/docs
```

---

## Limitations (Be Honest)

* No database (data resets on restart)
* No authentication
* No real booking persistence
* Not production-ready

---

## Next Improvements

* Replace JSON with PostgreSQL
* Add authentication (JWT)
* Separate routes, models, services
* Add proper error handling

---

## Author

Hemant Narute

