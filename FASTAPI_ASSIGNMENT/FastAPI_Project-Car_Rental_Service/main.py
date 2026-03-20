from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import json

app = FastAPI()

FILE = "data.json"

# ---------------- FILE HANDLING ----------------
def load_data():
    with open(FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

# ---------------- MODELS ----------------
class Car(BaseModel):
    id: int
    name: str
    brand: str
    price_per_day: float = Field(gt=0)
    available: bool = True

class User(BaseModel):
    id: int
    name: str
    license_number: str

class Booking(BaseModel):
    id: int
    user_id: int
    car_id: int
    days: int = Field(gt=0)
    status: str = "booked"
    total_price: float = 0

# ---------------- HELPERS ----------------
def find_item(data, key, value):
    for item in data:
        if item[key] == value:
            return item
    return None

# ---------------- BASIC ----------------
@app.get("/")
def home():
    return {"message": "Car Rental API (JSON Storage)"}

@app.get("/summary")
def summary():
    data = load_data()
    return {
        "total_cars": len(data["cars"]),
        "total_users": len(data["users"]),
        "total_bookings": len(data["bookings"])
    }

# ---------------- CARS ----------------
@app.get("/cars")
def get_cars(search: Optional[str] = None):
    data = load_data()
    cars = data["cars"]

    if search:
        cars = [c for c in cars if search.lower() in c["name"].lower()]

    return cars

# 🔥 IMPORTANT: ADVANCED ROUTES FIRST
@app.get("/cars/filter")
def filter_cars(max_price: Optional[float] = None, available: Optional[bool] = None):
    data = load_data()
    cars = data["cars"]

    if max_price is not None:
        cars = [c for c in cars if c["price_per_day"] <= max_price]

    if available is not None:
        cars = [c for c in cars if c["available"] == available]

    return cars

@app.get("/cars/sort")
def sort_cars(order: str = "asc"):
    data = load_data()
    cars = data["cars"]

    reverse = True if order == "desc" else False
    return sorted(cars, key=lambda x: x["price_per_day"], reverse=reverse)

@app.get("/cars/page")
def get_cars_page(page: int = 1, limit: int = 3):
    data = load_data()
    cars = data["cars"]

    start = (page - 1) * limit
    return {
        "page": page,
        "cars": cars[start:start + limit]
    }

@app.get("/cars/browse")
def browse(
    search: Optional[str] = None,
    max_price: Optional[float] = None,
    page: int = 1,
    limit: int = 3
):
    data = load_data()
    cars = data["cars"]

    if search:
        cars = [c for c in cars if search.lower() in c["name"].lower()]

    if max_price:
        cars = [c for c in cars if c["price_per_day"] <= max_price]

    start = (page - 1) * limit
    return cars[start:start + limit]

# 🔥 KEEP THIS LAST (VERY IMPORTANT)
@app.get("/cars/{car_id}")
def get_car(car_id: int):
    data = load_data()
    car = find_item(data["cars"], "id", car_id)

    if not car:
        raise HTTPException(404, "Car not found")

    return car

@app.post("/cars")
def create_car(car: Car):
    data = load_data()

    if find_item(data["cars"], "id", car.id):
        raise HTTPException(400, "Car already exists")

    data["cars"].append(car.dict())
    save_data(data)
    return car

@app.put("/cars/{car_id}")
def update_car(car_id: int, price_per_day: float = None, available: bool = None):
    data = load_data()
    car = find_item(data["cars"], "id", car_id)

    if not car:
        raise HTTPException(404, "Car not found")

    if price_per_day is not None:
        car["price_per_day"] = price_per_day

    if available is not None:
        car["available"] = available

    save_data(data)
    return car

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    data = load_data()
    car = find_item(data["cars"], "id", car_id)

    if not car:
        raise HTTPException(404, "Car not found")

    data["cars"].remove(car)
    save_data(data)

    return {"message": "Car deleted"}

# ---------------- USERS ----------------
@app.get("/users")
def get_users():
    data = load_data()
    return data["users"]

@app.post("/users")
def create_user(user: User):
    data = load_data()

    if find_item(data["users"], "id", user.id):
        raise HTTPException(400, "User exists")

    data["users"].append(user.dict())
    save_data(data)
    return user

# ---------------- BOOKINGS ----------------
@app.get("/bookings")
def get_bookings(status: Optional[str] = None):
    data = load_data()
    bookings = data["bookings"]

    if status:
        bookings = [b for b in bookings if b["status"] == status]

    return bookings

@app.post("/bookings")
def create_booking(booking: Booking):
    data = load_data()

    car = find_item(data["cars"], "id", booking.car_id)
    user = find_item(data["users"], "id", booking.user_id)

    if not car:
        raise HTTPException(404, "Car not found")
    if not user:
        raise HTTPException(404, "User not found")
    if not car["available"]:
        raise HTTPException(400, "Car not available")

    booking.total_price = car["price_per_day"] * booking.days
    car["available"] = False

    data["bookings"].append(booking.dict())
    save_data(data)

    return booking

# ---------------- WORKFLOW ----------------
@app.post("/bookings/confirm/{booking_id}")
def confirm_booking(booking_id: int):
    data = load_data()
    booking = find_item(data["bookings"], "id", booking_id)

    if not booking:
        raise HTTPException(404, "Booking not found")

    booking["status"] = "confirmed"
    save_data(data)
    return booking

@app.post("/bookings/complete/{booking_id}")
def complete_booking(booking_id: int):
    data = load_data()
    booking = find_item(data["bookings"], "id", booking_id)

    if not booking:
        raise HTTPException(404, "Booking not found")

    car = find_item(data["cars"], "id", booking["car_id"])
    car["available"] = True

    booking["status"] = "completed"
    save_data(data)
    return booking

@app.post("/bookings/cancel/{booking_id}")
def cancel_booking(booking_id: int):
    data = load_data()
    booking = find_item(data["bookings"], "id", booking_id)

    if not booking:
        raise HTTPException(404, "Booking not found")

    car = find_item(data["cars"], "id", booking["car_id"])
    car["available"] = True

    booking["status"] = "cancelled"
    save_data(data)
    return booking

@app.get("/bookings/filter")
def filter_bookings(status: Optional[str] = None):
    data = load_data()
    bookings = data["bookings"]

    if status:
        bookings = [b for b in bookings if b["status"] == status]

    return bookings