from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pymysql
from typing import List, Optional
from pydantic import BaseModel

app = FastAPI(title="Travel App API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── DB CONNECTION ─────────────────────────────────────────────────────────────
DB_HOST = "192.168.100.40"
DB_USER = "root"
DB_PASSWORD = "P@ssw0rd"  # Update if your MariaDB has a password
DB_NAME = "travel"

def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4"
    )


# ── MODELS ────────────────────────────────────────────────────────────────────
class StyleOut(BaseModel):
    style_id: int
    style_name: str


class PlaceOut(BaseModel):
    place_id: int
    place_name: str
    place_descript: Optional[str] = None
    place_image: Optional[str] = None
    rating: Optional[float] = None
    openning_hr: Optional[str] = None
    style_id: Optional[int] = None


class PlaceCreate(BaseModel):
    """Model for creating a new place"""
    place_name: str
    place_descript: Optional[str] = None
    place_image: Optional[str] = None
    rating: Optional[float] = None
    openning_hr: Optional[str] = None
    style_id: Optional[int] = None


class PlaceUpdate(BaseModel):
    """Model for updating a place"""
    place_name: Optional[str] = None
    place_descript: Optional[str] = None
    place_image: Optional[str] = None
    rating: Optional[float] = None
    openning_hr: Optional[str] = None
    style_id: Optional[int] = None


class LoginRequest(BaseModel):
    """Model for login request"""
    username: str
    password: str


class BudgetOut(BaseModel):
    budget_id: int
    min_budget: float
    max_budget: float
    place_id: int


class TransportationOut(BaseModel):
    transportation_id: int
    tran_cost: float
    place_id: int


class TravelCostOut(BaseModel):
    budget_info: Optional[BudgetOut] = None
    transportation_info: Optional[TransportationOut] = None
    total_cost: Optional[float] = None


# ── ROUTES ────────────────────────────────────────────────────────────────────
@app.get("/health")
def health_check():
    """Check API connection and database status"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Count places
        cursor.execute("SELECT COUNT(*) FROM rec_travel")
        places_count = cursor.fetchone()[0]
        
        # Count styles
        cursor.execute("SELECT COUNT(*) FROM style_travel")
        styles_count = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "status": "healthy",
            "database": "connected",
            "places_count": places_count,
            "styles_count": styles_count
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }


@app.get("/styles", response_model=List[StyleOut])
def get_styles():
    """Return all travel styles from style_travel table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT style_id, style_name FROM style_travel ORDER BY style_id")
        rows = cursor.fetchall()
        conn.close()
        return [{"style_id": row[0], "style_name": row[1]} for row in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/places", response_model=List[PlaceOut])
def get_places(style_id: Optional[int] = None):
    """Return all places from rec_travel table, optionally filtered by style_id"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        if style_id is not None:
            cursor.execute(
                """
                SELECT place_id, place_name, place_descript, place_image,
                       rating, openning_hr, style_id
                FROM rec_travel
                WHERE style_id = %s
                ORDER BY rating DESC
                """,
                (style_id,),
            )
        else:
            cursor.execute(
                """
                SELECT place_id, place_name, place_descript, place_image,
                       rating, openning_hr, style_id
                FROM rec_travel
                ORDER BY rating DESC
                """
            )
        rows = cursor.fetchall()
        conn.close()
        return [
            {
                "place_id": r[0],
                "place_name": r[1],
                "place_descript": r[2],
                "place_image": r[3],
                "rating": float(r[4]) if r[4] else None,
                "openning_hr": r[5],
                "style_id": r[6],
            }
            for r in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/places/{place_id}", response_model=PlaceOut)
def get_place(place_id: int):
    """Return a single place by ID"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT place_id, place_name, place_descript, place_image,
                   rating, openning_hr, style_id
            FROM rec_travel WHERE place_id = %s
            """,
            (place_id,),
        )
        row = cursor.fetchone()
        conn.close()
        if not row:
            raise HTTPException(status_code=404, detail="Place not found")
        return {
            "place_id": row[0],
            "place_name": row[1],
            "place_descript": row[2],
            "place_image": row[3],
            "rating": float(row[4]) if row[4] else None,
            "openning_hr": row[5],
            "style_id": row[6],
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/places", response_model=PlaceOut, status_code=201)
def create_place(place: PlaceCreate):
    """Create a new place in rec_travel table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO rec_travel (place_name, place_descript, place_image, rating, openning_hr, style_id)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (
                place.place_name,
                place.place_descript,
                place.place_image,
                place.rating,
                place.openning_hr,
                place.style_id,
            ),
        )
        conn.commit()
        place_id = cursor.lastrowid
        conn.close()

        return {
            "place_id": place_id,
            "place_name": place.place_name,
            "place_descript": place.place_descript,
            "place_image": place.place_image,
            "rating": place.rating,
            "openning_hr": place.openning_hr,
            "style_id": place.style_id,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/places/{place_id}", response_model=PlaceOut)
def update_place(place_id: int, place: PlaceUpdate):
    """Update an existing place in rec_travel table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if place exists
        cursor.execute("SELECT * FROM rec_travel WHERE place_id = %s", (place_id,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            raise HTTPException(status_code=404, detail="Place not found")

        # Build dynamic update query (only update fields that are provided)
        updates = []
        values = []
        if place.place_name is not None:
            updates.append("place_name = %s")
            values.append(place.place_name)
        if place.place_descript is not None:
            updates.append("place_descript = %s")
            values.append(place.place_descript)
        if place.place_image is not None:
            updates.append("place_image = %s")
            values.append(place.place_image)
        if place.rating is not None:
            updates.append("rating = %s")
            values.append(place.rating)
        if place.openning_hr is not None:
            updates.append("openning_hr = %s")
            values.append(place.openning_hr)
        if place.style_id is not None:
            updates.append("style_id = %s")
            values.append(place.style_id)

        if not updates:
            conn.close()
            raise HTTPException(status_code=400, detail="No fields to update")

        values.append(place_id)
        query = f"UPDATE rec_travel SET {', '.join(updates)} WHERE place_id = %s"
        cursor.execute(query, values)
        conn.commit()
        conn.close()

        # Fetch and return updated place
        return get_place(place_id)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/places/{place_id}", status_code=204)
def delete_place(place_id: int):
    """Delete a place from rec_travel table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Check if place exists
        cursor.execute("SELECT * FROM rec_travel WHERE place_id = %s", (place_id,))
        existing = cursor.fetchone()
        if not existing:
            conn.close()
            raise HTTPException(status_code=404, detail="Place not found")

        # Delete the place
        cursor.execute("DELETE FROM rec_travel WHERE place_id = %s", (place_id,))
        conn.commit()
        conn.close()
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/budget/{place_id}")
def get_budget(place_id: int):
    """Get budget information for a place from budget table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT budget_id, min_budget, max_budget, place_id FROM budget WHERE place_id = %s",
            (place_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "budget_id": row[0],
            "min_budget": float(row[1]),
            "max_budget": float(row[2]),
            "place_id": row[3]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/transportation/{place_id}")
def get_transportation(place_id: int):
    """Get transportation cost information for a place from transportation table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT tran_id, tran_name, tran_cost, tran_time, place_id FROM transportation WHERE place_id = %s LIMIT 1",
            (place_id,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            "tran_id": row[0],
            "tran_name": row[1],
            "tran_cost": float(row[2]),
            "tran_time": row[3],
            "place_id": row[4]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/transportation-options/{place_id}")
def get_transportation_options(place_id: int):
    """Get all transportation options available for a place"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT tran_id, tran_name, tran_cost, tran_time FROM transportation WHERE place_id = %s ORDER BY tran_cost ASC",
            (place_id,)
        )
        rows = cursor.fetchall()
        conn.close()
        
        options = []
        for row in rows:
            options.append({
                "tran_id": row[0],
                "tran_name": row[1],
                "tran_cost": float(row[2]),
                "tran_time": row[3]
            })
        
        return options
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/travel-cost/{place_id}")
def get_travel_cost(place_id: int):
    """Get total travel cost (tran_cost + (min_budget+max_budget)/2)"""
    try:
        # Get budget data
        conn = get_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            "SELECT budget_id, min_budget, max_budget, place_id FROM budget WHERE place_id = %s",
            (place_id,)
        )
        budget_row = cursor.fetchone()
        
        # Get transportation data (get the first one for the place)
        cursor.execute(
            "SELECT tran_id, tran_name, tran_cost, tran_time, place_id FROM transportation WHERE place_id = %s LIMIT 1",
            (place_id,)
        )
        transport_row = cursor.fetchone()
        
        conn.close()
        
        budget_info = None
        transport_info = None
        total_cost = None
        
        if budget_row:
            budget_info = {
                "budget_id": budget_row[0],
                "min_budget": float(budget_row[1]),
                "max_budget": float(budget_row[2]),
                "place_id": budget_row[3]
            }
        
        if transport_row:
            transport_info = {
                "tran_id": transport_row[0],
                "tran_name": transport_row[1],
                "tran_cost": float(transport_row[2]),
                "tran_time": transport_row[3],
                "place_id": transport_row[4]
            }
        
        # Calculate total cost
        if budget_info and transport_info:
            avg_budget = (budget_info["min_budget"] + budget_info["max_budget"]) / 2
            total_cost = transport_info["tran_cost"] + avg_budget
        
        return {
            "budget_info": budget_info,
            "transportation_info": transport_info,
            "total_cost": total_cost
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/login")
def login(request: LoginRequest):
    """Verify user credentials from user_travel table"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        
        # Strip whitespace from input
        username = request.username.strip()
        password = request.password.strip()
        
        # Query user_travel table for matching username and password
        cursor.execute(
            """
            SELECT user_id FROM user_travel 
            WHERE TRIM(username) = %s AND TRIM(password) = %s
            """,
            (username, password)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user:
            # User found and password matches
            return {
                "success": True,
                "message": "Login successful",
                "user_id": user[0],
                "username": username
            }
        else:
            # Invalid username or password
            return {
                "success": False,
                "message": "Invalid username or password"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── RUN ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("travel_app:app", host="0.0.0.0", port=3500, reload=True)