import sqlite3

DB_PATH = "bookings.db"

def get_db():

    conn = sqlite3.connect(DB_PATH)

    conn.row_factory = sqlite3.Row

    return conn

def init_db():

    conn = get_db()

    conn.executescript("""

    CREATE TABLE IF NOT EXISTS bookings (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        customer TEXT NOT NULL,

        vehicle_number TEXT,

        car_model TEXT NOT NULL,

        description TEXT NOT NULL,

        issue TEXT,

        technician TEXT,

        status TEXT DEFAULT 'pending',

        workflow_stage TEXT DEFAULT 'Booked',

        eta_minutes INTEGER,

        delay_risk INTEGER DEFAULT 0,

        service_type TEXT,

        priority TEXT,

        estimated_cost REAL DEFAULT 0,

        insurance_provider TEXT,

        insurance_active INTEGER DEFAULT 0,

        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS inventory (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        part_name TEXT NOT NULL,

        category TEXT,

        quantity INTEGER DEFAULT 0,

        unit_cost REAL DEFAULT 0.0
    );

    CREATE TABLE IF NOT EXISTS activity_log (

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        agent TEXT NOT NULL,

        action TEXT NOT NULL,

        details TEXT,

        booking_id INTEGER,

        timestamp TEXT DEFAULT CURRENT_TIMESTAMP
    );

    """)

    conn.commit()
    conn.close()

def reset_database():

    conn = get_db()

    conn.executescript("""

    DROP TABLE IF EXISTS bookings;

    DROP TABLE IF EXISTS inventory;

    DROP TABLE IF EXISTS activity_log;

    """)

    conn.commit()
    conn.close()

    init_db()