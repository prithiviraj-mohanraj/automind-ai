from rapidfuzz import fuzz
import os
import json
import re
import difflib

from dotenv import load_dotenv
from groq import Groq

from database import get_db
from automotive_knowledge import ISSUE_MATRIX

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MODEL = "llama-3.1-8b-instant"

# ─────────────────────────────────────────────
# LOG ACTIVITY
# ─────────────────────────────────────────────

def log_activity(
    agent: str,
    action: str,
    details: str,
    booking_id: int = None
):

    conn = get_db()

    conn.execute(
        """
        INSERT INTO activity_log (
            agent,
            action,
            details,
            booking_id
        )
        VALUES (?, ?, ?, ?)
        """,
        (
            agent,
            action,
            details,
            booking_id
        )
    )

    conn.commit()
    conn.close()

# ─────────────────────────────────────────────
# FUZZY ISSUE DETECTION
# ─────────────────────────────────────────────

def detect_issues(text: str):

    text = text.lower()

    detected = []

    for issue in ISSUE_MATRIX.keys():

        if issue in text:
            detected.append(issue)
            continue

        # FUZZY MATCHING

        similarity = difflib.SequenceMatcher(
            None,
            text,
            issue
        ).ratio()

        if similarity > 0.55:
            detected.append(issue)

    return list(set(detected))

# ─────────────────────────────────────────────
# TRIAGE INSPECTION AGENT
# ─────────────────────────────────────────────

def booking_agent(
    description: str,
    car_model: str
):

    detected_issues = detect_issues(description)

    # FALLBACK

    if not detected_issues:

        detected_issues = ["service"]

    systems = []
    parts = []
    specialists = []
    severity_score = 0

    safe_to_drive = True

    insurance_items = []

    estimated_hours = []

    inspection_levels = []

    severity_rank = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    highest_severity = "LOW"

    # ─────────────────────────────────────
    # AGGREGATE KNOWLEDGE
    # ─────────────────────────────────────

    for issue in detected_issues:

        data = ISSUE_MATRIX.get(issue)

        if not data:
            continue

        systems.extend(
            data["systems_to_check"]
        )

        parts.extend(
            data["parts_needed"]
        )

        specialists.append(
            data["specialist"]
        )

        inspection_levels.append(
            data["inspection_level"]
        )

        estimated_hours.append(
            data["estimated_hours"]
        )

        insurance_items.append(
            data["insurance"]
        )

        if not data["safe_to_drive"]:
            safe_to_drive = False

        if severity_rank[data["severity"]] > severity_score:

            severity_score = severity_rank[data["severity"]]

            highest_severity = data["severity"]

    # REMOVE DUPLICATES

    systems = list(set(systems))
    parts = list(set(parts))
    specialists = list(set(specialists))
    inspection_levels = list(set(inspection_levels))

    # MULTI ISSUE DETECTION

    multi_issue = len(detected_issues) > 1

    # ─────────────────────────────────────
    # AI EXPLANATION
    # ─────────────────────────────────────

    prompt = f"""
You are a professional automotive workshop AI.

Customer issue:
{description}

Detected issues:
{detected_issues}

Generate:
- professional inspection summary
- likely root cause
- workshop recommendation

Maximum 120 words.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=180
    )

    ai_summary = response.choices[0].message.content.strip()

    return {

        # OLD COMPATIBILITY

        "likely_issue": ", ".join(detected_issues),
        "technician": specialists[0] if specialists else "General Technician",
        "eta_minutes": 180,
        "parts_needed": parts,

        # NEW ENTERPRISE DATA

        "severity": highest_severity,
        "safe_to_drive": safe_to_drive,
        "inspection_levels": inspection_levels,
        "systems_to_check": systems,
        "specialists_required": specialists,
        "multi_issue_detected": multi_issue,
        "insurance_status": insurance_items,
        "inspection_summary": ai_summary
    }

# ─────────────────────────────────────────────
# INVENTORY AGENT
# ─────────────────────────────────────────────

def inventory_agent(parts_needed: list):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT
            part_name,
            quantity
        FROM inventory
        """
    ).fetchall()

    conn.close()

    inventory_map = {
        row["part_name"].lower(): row["quantity"]
        for row in rows
    }

    available = []
    missing = []

    for part in parts_needed:

        qty = inventory_map.get(
            part.lower(),
            0
        )

        if qty > 0:
            available.append(part)
        else:
            missing.append(part)

    if missing:

        message = (
            f"Missing parts detected: "
            f"{', '.join(missing)}"
        )

    else:

        message = "All required parts available"

    return {
        "all_available": len(missing) == 0,
        "available_parts": available,
        "missing_parts": missing,
        "message": message
    }

# ─────────────────────────────────────────────
# DELAY AGENT
# ─────────────────────────────────────────────

def delay_agent(
    active_jobs: int,
    eta_minutes: int
):

    risk = min(
        95,
        (active_jobs * 12) + (eta_minutes // 10)
    )

    if risk < 30:
        msg = "Workshop load normal"

    elif risk < 60:
        msg = "Moderate workshop load"

    else:
        msg = "High workshop congestion"

    return {
        "delay_risk": risk,
        "message": msg
    }

# ─────────────────────────────────────────────
# SUPPORT AGENT
# ─────────────────────────────────────────────

def support_agent(
    message: str,
    booking_context: dict
):

    ctx = f"""
Customer:
{booking_context.get('customer')}

Vehicle:
{booking_context.get('car_model')}

Issue:
{booking_context.get('issue')}

Status:
{booking_context.get('status')}

Technician:
{booking_context.get('technician')}
"""

    prompt = f"""
You are a premium automotive customer support AI.

Booking context:
{ctx}

Customer message:
{message}

Reply professionally.
Maximum 100 words.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=150
    )

    return {
        "reply": response.choices[0].message.content.strip()
    }

# ─────────────────────────────────────────────
# WORKSHOP QUERY AGENT
# ─────────────────────────────────────────────

def workshop_query_agent(
    question: str,
    workshop_data: list
):

    question_lower = question.lower().strip()

    # ─────────────────────────────────────
    # SMART CUSTOMER SEARCH
    # ─────────────────────────────────────

    best_customer = None
    best_score = 0

    for row in workshop_data:

        customer = str(
            row.get("customer", "")
        ).lower()

        score = fuzz.partial_ratio(
            customer,
            question_lower
        )

        if score > best_score:

            best_score = score
            best_customer = row

    if best_score > 70 and best_customer:

        return {
            "answer":
            f"Customer {best_customer['customer']} is present in workshop records. "
            f"Vehicle Number: {best_customer.get('vehicle_number', 'N/A')}. "
            f"Car Model: {best_customer.get('car_model', 'N/A')}. "
            f"Issue: {best_customer.get('issue', 'N/A')}. "
            f"Technician: {best_customer.get('technician', 'N/A')}. "
            f"Current Status: {best_customer.get('status', 'N/A')}."
        }

    # ─────────────────────────────────────
    # VEHICLE NUMBER SEARCH
    # ─────────────────────────────────────

    best_vehicle = None
    best_vehicle_score = 0

    for row in workshop_data:

        vehicle = str(
            row.get("vehicle_number", "")
        ).lower()

        score = fuzz.partial_ratio(
            vehicle,
            question_lower
        )

        if score > best_vehicle_score:

            best_vehicle_score = score
            best_vehicle = row

    if best_vehicle_score > 80 and best_vehicle:

        return {
            "answer":
            f"Vehicle {best_vehicle['vehicle_number']} belongs to "
            f"{best_vehicle.get('customer')}. "
            f"Car Model: {best_vehicle.get('car_model')}. "
            f"Issue: {best_vehicle.get('issue')}. "
            f"Status: {best_vehicle.get('status')}."
        }

    # ─────────────────────────────────────
    # TECHNICIAN ANALYTICS
    # ─────────────────────────────────────

    if (
        "technician" in question_lower
        or "mechanic" in question_lower
    ):

        tech_count = {}

        for row in workshop_data:

            tech = row.get(
                "technician",
                "Unknown"
            )

            tech_count[tech] = (
                tech_count.get(tech, 0) + 1
            )

        sorted_techs = sorted(
            tech_count.items(),
            key=lambda x: x[1],
            reverse=True
        )

        summary = []

        for tech, count in sorted_techs[:5]:

            summary.append(
                f"{tech} ({count} jobs)"
            )

        return {
            "answer":
            "Top technicians by workload: "
            + ", ".join(summary)
        }

    # ─────────────────────────────────────
    # VEHICLE MODEL SEARCH
    # ─────────────────────────────────────

    models_found = []

    for row in workshop_data:

        model = str(
            row.get("car_model", "")
        ).lower()

        if any(
            word in model
            for word in question_lower.split()
        ):

            models_found.append(
                f"{row.get('customer')} - {row.get('car_model')}"
            )

    if models_found:

        return {
            "answer":
            "Matching workshop vehicles: "
            + ", ".join(models_found[:10])
        }

    # ─────────────────────────────────────
    # INSURANCE CLAIMS
    # ─────────────────────────────────────

    if "insurance" in question_lower:

        insured = []

        for row in workshop_data:

            insurance = row.get(
                "insurance_provider",
                ""
            )

            if insurance != "No Insurance":

                insured.append(
                    f"{row.get('customer')} ({insurance})"
                )

        return {
            "answer":
            "Vehicles under insurance coverage: "
            + ", ".join(insured[:10])
        }

    # ─────────────────────────────────────
    # HIGH PRIORITY
    # ─────────────────────────────────────

    if (
        "critical" in question_lower
        or "high priority" in question_lower
    ):

        criticals = []

        for row in workshop_data:

            priority = str(
                row.get("priority", "")
            ).upper()

            if priority in ["HIGH", "CRITICAL"]:

                criticals.append(
                    f"{row.get('customer')} - {row.get('car_model')}"
                )

        return {
            "answer":
            "Critical workshop repairs: "
            + ", ".join(criticals[:10])
        }

    # ─────────────────────────────────────
    # FALLBACK AI
    # ─────────────────────────────────────

    compact_data = workshop_data[:15]

    prompt = f"""
You are an enterprise automotive workshop analyst AI.

Workshop data:
{compact_data}

Question:
{question}

Answer professionally.
Maximum 120 words.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_tokens=150
    )

    return {
        "answer":
        response.choices[0].message.content.strip()
    }
# ─────────────────────────────────────────────
# BILLING AGENT
# ─────────────────────────────────────────────

def billing_agent(
    detected_issue: str,
    parts_needed: list
):

    conn = get_db()

    rows = conn.execute(
        """
        SELECT
            part_name,
            unit_cost
        FROM inventory
        """
    ).fetchall()

    conn.close()

    cost_map = {
        row["part_name"]: row["unit_cost"]
        for row in rows
    }

    parts_total = 0

    for part in parts_needed:

        parts_total += cost_map.get(
            part,
            1500
        )

    labor = 3500

    gst = (parts_total + labor) * 0.18

    total = parts_total + labor + gst

    insurance_covered = any(
        x.lower() == "covered"
        for x in [detected_issue]
    )

    insurance_discount = 0

    if insurance_covered:
        insurance_discount = total * 0.6

    customer_payable = total - insurance_discount

    return {
    "parts_cost": round(parts_total, 2),
    "labor_cost": labor,
    "gst": round(gst, 2),
    "total_estimate": round(total, 2),
    "insurance_applicable": insurance_covered,
    "insurance_covered_amount": round(insurance_discount, 2),
    "customer_payable": round(customer_payable, 2)
}