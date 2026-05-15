import random

from faker import Faker

from database import (
    reset_database,
    get_db
)

fake = Faker("en_IN")


def seed_database():

    # RESET DATABASE

    reset_database()

    conn = get_db()

    # ─────────────────────────────────────────────
    # CUSTOMERS
    # ─────────────────────────────────────────────

    customers = [

        "Arun Kumar",
        "Praveen Raj",
        "Vigneshwaran",
        "Karthikeyan",
        "Sathish Kumar",
        "Gokul Raj",
        "Saravanan",
        "Harishankar",
        "Dinesh Babu",
        "Madhan Kumar",
        "Ashwin Prabhu",
        "Naveen Kumar",
        "Lokeshwaran",
        "Anand Raj",
        "Balamurugan",
        "Suresh Babu",
        "Prithiv Raj",
        "Kavin Kumar",
        "Vetri Selvan",
        "Jeeva",
        "Ananya Iyer",
        "Keerthana",
        "Harini",
        "Divya Lakshmi",
        "Shruthi",
        "Nivetha",
        "Gayathri",
        "Pavithra",
        "Meenakshi",
        "Aarthi",
        "Janani",
        "Roshini",
        "Swetha",
        "Mahalakshmi",
        "Nandhini",
        "Deepika",
        "Sumathi",
        "Sivakumar",
        "Tharun",
        "Kishore"
    ]

    # ─────────────────────────────────────────────
    # CARS
    # ─────────────────────────────────────────────

    cars = [

        "Hyundai Creta",
        "Hyundai i20",
        "Hyundai Verna",

        "Maruti Swift",
        "Maruti Baleno",
        "Maruti Brezza",

        "Tata Nexon",
        "Tata Punch",
        "Tata Harrier",

        "Mahindra XUV700",
        "Mahindra Scorpio N",
        "Mahindra Thar",

        "Toyota Innova Crysta",
        "Toyota Fortuner",
        "Toyota Glanza",

        "Honda City",
        "Honda Amaze",
        "Honda Elevate",

        "Kia Seltos",
        "Kia Sonet",

        "Volkswagen Virtus",
        "Skoda Slavia",

        "Renault Triber",
        "Nissan Magnite"
    ]

    # ─────────────────────────────────────────────
    # ISSUES
    # ─────────────────────────────────────────────

    issues = [

        "engine overheating and smoke from bonnet",

        "brake vibration while driving",

        "brake noise during reverse",

        "battery draining overnight",

        "ac not cooling properly",

        "oil leakage under engine",

        "suspension noise on speed breaker",

        "vehicle pulling left side",

        "steering vibration at high speed",

        "engine knocking sound",

        "accident front bumper damage",

        "rear bumper dent",

        "headlight not working",

        "wiring issue after rain",

        "tyre puncture and wheel alignment issue",

        "general periodic service",

        "engine starting problem",

        "coolant leakage issue",

        "gear shifting hard",

        "check engine light on"
    ]

    # ─────────────────────────────────────────────
    # TECHNICIANS
    # ─────────────────────────────────────────────

    technicians = [

        "Aravind M.",
        "Suresh K.",
        "Lokesh R.",
        "Prabhu V.",
        "Naveen Kumar",
        "Dinesh Raj",
        "Karthik S.",
        "Saravana Kumar"
    ]

    # ─────────────────────────────────────────────
    # WORKFLOW STAGES
    # ─────────────────────────────────────────────

    workflow_stages = [

        "Booked",

        "Diagnosing",

        "Awaiting Parts",

        "Repair In Progress",

        "QA Inspection",

        "Ready Delivery",

        "Delivered"
    ]

    # ─────────────────────────────────────────────
    # STATUS
    # ─────────────────────────────────────────────

    statuses = [

        "pending",

        "in_progress",

        "waiting",

        "completed"
    ]

    # ─────────────────────────────────────────────
    # PRIORITIES
    # ─────────────────────────────────────────────

    priorities = [

        "LOW",

        "MEDIUM",

        "HIGH",

        "CRITICAL"
    ]

    # ─────────────────────────────────────────────
    # INSURANCE
    # ─────────────────────────────────────────────

    insurance_providers = [

        "HDFC ERGO",

        "ICICI Lombard",

        "Bajaj Allianz",

        "TATA AIG",

        "Reliance General",

        "No Insurance"
    ]

    # ─────────────────────────────────────────────
    # SERVICE TYPES
    # ─────────────────────────────────────────────

    service_types = [

        "Periodic Service",

        "Repair",

        "Emergency Repair",

        "Insurance Claim",

        "Diagnostics"
    ]

    # ─────────────────────────────────────────────
    # INVENTORY
    # ─────────────────────────────────────────────

    inventory_parts = [

        ("Engine Oil", "Engine", 120, 2200),
        ("Oil Filter", "Engine", 140, 450),
        ("Air Filter", "Engine", 100, 650),
        ("Fuel Filter", "Engine", 85, 750),

        ("Radiator Hose", "Cooling", 40, 950),
        ("Coolant", "Cooling", 100, 900),
        ("Water Pump", "Cooling", 15, 4500),
        ("Thermostat", "Cooling", 30, 1800),

        ("Timing Belt", "Engine", 20, 5500),
        ("Spark Plug", "Engine", 100, 350),
        ("Gasket Kit", "Engine", 25, 3200),

        ("Brake Pads", "Brakes", 70, 3200),
        ("Brake Disc", "Brakes", 40, 6200),
        ("Brake Rotor", "Brakes", 30, 4800),
        ("Brake Fluid", "Brakes", 60, 550),

        ("Battery", "Electrical", 25, 8500),
        ("Alternator Belt", "Electrical", 30, 1200),
        ("Fuse Kit", "Electrical", 100, 350),
        ("Relay", "Electrical", 80, 500),

        ("Wiring Kit", "Electrical", 20, 4500),
        ("Headlight Bulb", "Electrical", 100, 650),

        ("Cabin Air Filter", "HVAC", 50, 850),
        ("AC Gas", "HVAC", 30, 2500),

        ("Bumper Assembly", "Body", 12, 9500),
        ("Paint Kit", "Body", 30, 2200),

        ("Shock Absorber", "Suspension", 25, 7800),

        ("Wheel Bearing", "Suspension", 35, 3200)
    ]

    # ─────────────────────────────────────────────
    # INSERT INVENTORY
    # ─────────────────────────────────────────────

    for item in inventory_parts:

        conn.execute(
            """
            INSERT INTO inventory (
                part_name,
                category,
                quantity,
                unit_cost
            )
            VALUES (?, ?, ?, ?)
            """,
            item
        )

    # ─────────────────────────────────────────────
    # GENERATE BOOKINGS
    # ─────────────────────────────────────────────

    for _ in range(250):

        customer = random.choice(customers)

        car = random.choice(cars)

        issue = random.choice(issues)

        technician = random.choice(technicians)

        workflow_stage = random.choice(
            workflow_stages
        )

        status = random.choice(statuses)

        priority = random.choice(priorities)

        insurance = random.choice(
            insurance_providers
        )

        service_type = random.choice(
            service_types
        )

        vehicle_number = (
            f"TN{random.randint(1,99)}"
            f"{random.choice(['A','B','C','D'])}"
            f"{random.randint(1000,9999)}"
        )

        estimated_cost = random.randint(
            2000,
            120000
        )

        insurance_active = 0

        if insurance != "No Insurance":
            insurance_active = 1

        conn.execute(
            """
            INSERT INTO bookings (

                customer,
                vehicle_number,
                car_model,
                description,
                issue,
                technician,
                status,
                workflow_stage,
                eta_minutes,
                delay_risk,
                service_type,
                priority,
                estimated_cost,
                insurance_provider,
                insurance_active

            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                customer,
                vehicle_number,
                car,
                issue,
                issue,
                technician,
                status,
                workflow_stage,
                random.randint(30, 480),
                random.randint(5, 95),
                service_type,
                priority,
                estimated_cost,
                insurance,
                insurance_active
            )
        )

    # ─────────────────────────────────────────────
    # ACTIVITY LOGS
    # ─────────────────────────────────────────────

    agents = [

        "BookingAgent",

        "InventoryAgent",

        "DelayAgent",

        "BillingAgent",

        "SupportAgent"
    ]

    actions = [

        "Vehicle diagnosed",

        "Inventory checked",

        "Delay risk calculated",

        "Insurance verified",

        "Repair estimate generated",

        "Vehicle inspection started",

        "Parts ordered",

        "Repair completed",

        "Vehicle delivered"
    ]

    for _ in range(1000):

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
                random.choice(agents),
                random.choice(actions),
                fake.sentence(),
                random.randint(1, 250)
            )
        )

    conn.commit()

    conn.close()

    print("SUCCESS: Enterprise automotive dataset generated.")


if __name__ == "__main__":
    seed_database()
