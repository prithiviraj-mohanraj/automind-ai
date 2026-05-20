from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv

from database import init_db, get_db

from agents import (
    booking_agent,
    inventory_agent,
    delay_agent,
    support_agent,
    workshop_query_agent,
    billing_agent,
    log_activity
)

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

# AUTO SEED IF EMPTY

from seed import seed_database

conn = get_db()

count = conn.execute(
    "SELECT COUNT(*) as c FROM bookings"
).fetchone()["c"]

conn.close()

if count == 0:

    print("DATABASE EMPTY -> AUTO SEEDING")

    seed_database()

# ─────────────────────────────────────────────
# MODELS
# ─────────────────────────────────────────────

class BookingRequest(BaseModel):

    customer: str

    vehicle_number: str

    car_model: str

    description: str
class SupportRequest(BaseModel):
    message: str
    booking_id: Optional[int] = None


class QueryRequest(BaseModel):
    question: str


# ─────────────────────────────────────────────
# ROOT
# ─────────────────────────────────────────────

@app.get("/")
def root():

    return {
        "message": "AutoMind AI Backend Running"
    }
@app.head("/")
def root_head():
    return

# ─────────────────────────────────────────────
# BOOKINGS
# ─────────────────────────────────────────────

@app.get("/api/bookings")
def get_bookings():

    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM bookings
        ORDER BY created_at DESC
        """
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# CREATE BOOKING
# ─────────────────────────────────────────────

@app.post("/api/booking")
def create_booking(req: BookingRequest):

    try:

        if (
            not req.customer.strip()
            or not req.car_model.strip()
            or not req.description.strip()
        ):

            return {
                "success": False,
                "error": "All fields are required"
            }

        conn = get_db()

        active_count = conn.execute(
            """
            SELECT COUNT(*) as c
            FROM bookings
            WHERE status IN (
                'pending',
                'in_progress',
                'waiting'
            )
            """
        ).fetchone()["c"]

        # BOOKING AGENT

        booking_result = booking_agent(
            req.description,
            req.car_model
        )

        # INVENTORY AGENT

        inventory_result = inventory_agent(
            booking_result.get(
                "parts_needed",
                []
            )
        )

        # DELAY AGENT

        delay_result = delay_agent(
            active_count,
            booking_result.get(
                "eta_minutes",
                60
            )
        )

        # BILLING AGENT

        billing_result = billing_agent(
            booking_result.get(
                "likely_issue",
                ""
            ),
            booking_result.get(
                "parts_needed",
                []
            )
        )

        # SAVE BOOKING

        cursor = conn.execute(
    """
    INSERT INTO bookings (

        customer,
        vehicle_number,
        car_model,
        description,
        issue,
        technician,
        status,
        eta_minutes,
        delay_risk,
        priority,
        estimated_cost,
        insurance_provider

    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """,
    (

        req.customer,

        req.vehicle_number,

        req.car_model,

        req.description,

        booking_result.get(
            "likely_issue",
            "General Inspection"
        ),

        booking_result.get(
            "technician",
            "Workshop Team"
        ),

        "pending",

        booking_result.get(
            "eta_minutes",
            120
        ),

        delay_result.get(
            "delay_risk",
            20
        ),

        booking_result.get(
            "severity",
            "MEDIUM"
        ),

        billing_result.get(
            "total_estimate",
            0
        ),

        billing_result.get(
            "insurance_status",
            "Not Covered"
        )

    )
)

        booking_id = cursor.lastrowid

        conn.commit()
        conn.close()

        # LOGS

        log_activity(
            "BookingAgent",
            "Vehicle diagnosed",
            booking_result["likely_issue"],
            booking_id
        )

        log_activity(
            "InventoryAgent",
            "Inventory verified",
            inventory_result["message"],
            booking_id
        )

        log_activity(
            "DelayAgent",
            "Delay prediction generated",
            f"{delay_result['delay_risk']}% risk",
            booking_id
        )

        log_activity(
            "BillingAgent",
            "Repair estimate generated",
            f"₹{billing_result['total_estimate']}",
            booking_id
        )

        return {
            "success": True,
            "booking_id": booking_id,
            "booking": booking_result,
            "inventory": inventory_result,
            "delay": delay_result,
            "billing": billing_result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


# ─────────────────────────────────────────────
# AI QUERY ANALYST
# ─────────────────────────────────────────────

@app.post("/api/query")
def workshop_query(req: QueryRequest):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT
            id,
            customer,
            vehicle_number,
            car_model,
            description,
            issue,
            technician,
            status,
            priority,
            estimated_cost,
            insurance_provider,
            created_at
        FROM bookings
        ORDER BY created_at DESC
        LIMIT 500
        """
    ).fetchall()

    conn.close()

    workshop_data = [
        dict(r)
        for r in rows
    ]

    # DEBUG LOG
    print("TOTAL RECORDS:", len(workshop_data))

    if len(workshop_data) > 0:
        print("SAMPLE RECORD:", workshop_data[0])

    result = workshop_query_agent(
        req.question,
        workshop_data
    )

    return result

# ─────────────────────────────────────────────
# SUPPORT
# ─────────────────────────────────────────────

@app.post("/api/support")
def support(req: SupportRequest):

    context = {}

    if req.booking_id:

        conn = get_db()

        row = conn.execute(
            """
            SELECT *
            FROM bookings
            WHERE id=?
            """,
            (req.booking_id,)
        ).fetchone()

        conn.close()

        if row:
            context = dict(row)

    result = support_agent(
        req.message,
        context
    )

    return result


# ─────────────────────────────────────────────
# ACTIVITY FEED
# ─────────────────────────────────────────────

@app.get("/api/activity-feed")
def feed():

    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM activity_log
        ORDER BY timestamp DESC
        LIMIT 50
        """
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# INVENTORY
# ─────────────────────────────────────────────

@app.get("/api/inventory")
def inventory():

    conn = get_db()

    rows = conn.execute(
        """
        SELECT *
        FROM inventory
        ORDER BY quantity ASC
        """
    ).fetchall()

    conn.close()

    return [dict(r) for r in rows]


# ─────────────────────────────────────────────
# STATS
# ─────────────────────────────────────────────

@app.get("/api/stats")
def stats():

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
        "completed": completed
    }

@app.get("/api/seed")
def run_seed():

    import seed

    seed.seed_database()

    return {
        "success": True,
        "message": "Production database seeded"
    }
