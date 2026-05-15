from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from database import init_db, get_db
# from agents import (
#     booking_agent,
#     inventory_agent,
#     delay_agent,
#     support_agent,
#     log_activity,
# )
def booking_agent(a, b):
    return {
        "likely_issue": "Engine issue",
        "technician": "Mike T.",
        "eta_minutes": 60,
        "parts_needed": []
    }

def inventory_agent(parts):
    return {
        "all_available": True,
        "missing_parts": [],
        "message": "Parts available"
    }

def delay_agent(a, b):
    return {
        "delay_risk": 20,
        "message": "Low delay risk"
    }

def support_agent(message, context):
    return {
        "reply": "Your vehicle is under inspection."
    }

def log_activity(a, b, c, d=None):
    pass
load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# ─────────────────────────────────────────────
# SIMPLE PYDANTIC MODELS
# ─────────────────────────────────────────────

class BookingRequest(BaseModel):
    customer: str
    car_model: str
    description: str


class SupportRequest(BaseModel):
    message: str
    booking_id: int = 0


class StatusUpdate(BaseModel):
    booking_id: int
    status: str


# ─────────────────────────────────────────────
# GET BOOKINGS
# ─────────────────────────────────────────────

@app.get("/api/bookings")
def get_bookings():
    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM bookings ORDER BY created_at DESC"
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# CREATE BOOKING
# ─────────────────────────────────────────────

@app.post("/api/booking")
def create_booking(req: BookingRequest):

    conn = get_db()

    # Count active jobs
    active_count = conn.execute(
        """
        SELECT COUNT(*) as c
        FROM bookings
        WHERE status IN ('pending','in_progress','waiting')
        """
    ).fetchone()["c"]

    # ── AGENT 1 ───────────────────────

    log_activity(
        "BookingAgent",
        "Analyzing complaint",
        req.description[:60]
    )

    booking_result = booking_agent(
        req.description,
        req.car_model
    )

    # ── AGENT 2 ───────────────────────

    log_activity(
        "InventoryAgent",
        "Checking inventory",
        str(booking_result.get("parts_needed", []))
    )

    inv_result = inventory_agent(
        booking_result.get("parts_needed", [])
    )

    # ── AGENT 3 ───────────────────────

    log_activity(
        "DelayAgent",
        "Checking workload",
        f"Active jobs: {active_count}"
    )

    delay_result = delay_agent(
        active_count,
        booking_result.get("eta_minutes", 60)
    )

    # ── SAVE BOOKING ───────────────────────

    cursor = conn.execute(
        """
        INSERT INTO bookings
        (
            customer,
            car_model,
            description,
            issue,
            technician,
            eta_minutes,
            delay_risk,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, 'pending')
        """,
        (
            req.customer,
            req.car_model,
            req.description,
            booking_result["likely_issue"],
            booking_result["technician"],
            booking_result["eta_minutes"],
            delay_result["delay_risk"],
        )
    )

    booking_id = cursor.lastrowid

    conn.commit()
    conn.close()

    # ── ACTIVITY LOGS ───────────────────────

    log_activity(
        "BookingAgent",
        "Booking created",
        f"Booking #{booking_id}",
        booking_id
    )

    log_activity(
        "InventoryAgent",
        inv_result["message"],
        "",
        booking_id
    )

    log_activity(
        "DelayAgent",
        delay_result["message"],
        "",
        booking_id
    )

    return {
        "success": True,
        "booking_id": booking_id,
        "booking": booking_result,
        "inventory": inv_result,
        "delay": delay_result,
    }


# ─────────────────────────────────────────────
# SUPPORT CHAT
# ─────────────────────────────────────────────

@app.post("/api/support")
def chat_support(req: SupportRequest):

    context = {}

    if req.booking_id != 0:

        conn = get_db()

        row = conn.execute(
            "SELECT * FROM bookings WHERE id=?",
            (req.booking_id,)
        ).fetchone()

        conn.close()

        if row:
            context = dict(row)

    log_activity(
        "SupportAgent",
        "Customer support request",
        req.message[:60],
        req.booking_id
    )

    result = support_agent(req.message, context)

    log_activity(
        "SupportAgent",
        "Reply generated",
        result["reply"][:80],
        req.booking_id
    )

    return result


# ─────────────────────────────────────────────
# UPDATE STATUS
# ─────────────────────────────────────────────

@app.patch("/api/booking/status")
def update_status(req: StatusUpdate):

    conn = get_db()

    conn.execute(
        "UPDATE bookings SET status=? WHERE id=?",
        (req.status, req.booking_id)
    )

    conn.commit()
    conn.close()

    log_activity(
        "BookingAgent",
        f"Status updated to {req.status}",
        "",
        req.booking_id
    )

    return {"success": True}


# ─────────────────────────────────────────────
# ACTIVITY FEED
# ─────────────────────────────────────────────

@app.get("/api/activity-feed")
def activity_feed():

    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM activity_log
        ORDER BY timestamp DESC
        LIMIT 30
        """
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# INVENTORY
# ─────────────────────────────────────────────

@app.get("/api/inventory")
def get_inventory():

    conn = get_db()

    rows = conn.execute(
        "SELECT * FROM inventory ORDER BY part_name"
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# DASHBOARD STATS
# ─────────────────────────────────────────────

@app.get("/api/stats")
def get_stats():

    conn = get_db()

    total = conn.execute(
        "SELECT COUNT(*) as c FROM bookings"
    ).fetchone()["c"]

    active = conn.execute(
        """
        SELECT COUNT(*) as c
        FROM bookings
        WHERE status='in_progress'
        """
    ).fetchone()["c"]

    pending = conn.execute(
        """
        SELECT COUNT(*) as c
        FROM bookings
        WHERE status='pending'
        """
    ).fetchone()["c"]

    completed = conn.execute(
        """
        SELECT COUNT(*) as c
        FROM bookings
        WHERE status='completed'
        """
    ).fetchone()["c"]

    conn.close()

    return {
        "total": total,
        "active": active,
        "pending": pending,
        "completed": completed,
    }