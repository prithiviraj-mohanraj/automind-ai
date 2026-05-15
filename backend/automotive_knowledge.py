# automotive_knowledge.py

ISSUE_MATRIX = {

    # =========================================================
    # ENGINE / COOLING
    # =========================================================

    "overheating": {
        "severity": "CRITICAL",
        "safe_to_drive": False,
        "inspection_level": "Advanced Engine Inspection",
        "systems_to_check": [
            "Radiator",
            "Coolant Level",
            "Coolant Leakage",
            "Thermostat",
            "Water Pump",
            "Cooling Fan",
            "Head Gasket",
            "Engine Oil",
            "Temperature Sensor",
            "Radiator Cap"
        ],
        "parts_needed": [
            "Coolant",
            "Radiator Hose",
            "Thermostat",
            "Water Pump",
            "Radiator Fan"
        ],
        "specialist": "Senior Engine Specialist",
        "estimated_hours": "5-8",
        "insurance": "Not Covered"
    },

    "engine knocking": {
        "severity": "CRITICAL",
        "safe_to_drive": False,
        "inspection_level": "Advanced Engine Diagnostics",
        "systems_to_check": [
            "Piston Assembly",
            "Crankshaft",
            "Connecting Rod",
            "Engine Bearings",
            "Engine Oil Quality",
            "Timing Chain"
        ],
        "parts_needed": [
            "Engine Oil",
            "Bearing Kit",
            "Timing Chain Kit"
        ],
        "specialist": "Engine Diagnostics Specialist",
        "estimated_hours": "8-14",
        "insurance": "Partial"
    },

    "engine noise": {
        "severity": "HIGH",
        "safe_to_drive": False,
        "inspection_level": "Mechanical Inspection",
        "systems_to_check": [
            "Engine Mount",
            "Timing Belt",
            "Alternator",
            "Belt Tensioner",
            "Piston Assembly"
        ],
        "parts_needed": [
            "Timing Belt",
            "Engine Mount",
            "Alternator Belt"
        ],
        "specialist": "Senior Engine Specialist",
        "estimated_hours": "4-7",
        "insurance": "Not Covered"
    },

    "oil leakage": {
        "severity": "HIGH",
        "safe_to_drive": False,
        "inspection_level": "Leakage Inspection",
        "systems_to_check": [
            "Oil Pan",
            "Valve Cover Gasket",
            "Oil Filter",
            "Oil Seal",
            "Turbo Oil Line"
        ],
        "parts_needed": [
            "Engine Oil",
            "Oil Seal",
            "Gasket Kit"
        ],
        "specialist": "Engine Repair Specialist",
        "estimated_hours": "3-6",
        "insurance": "Partial"
    },

    "smoke": {
        "severity": "CRITICAL",
        "safe_to_drive": False,
        "inspection_level": "Combustion Diagnostics",
        "systems_to_check": [
            "Engine Combustion",
            "Coolant Leakage",
            "Turbocharger",
            "Wiring Harness",
            "Exhaust System",
            "Head Gasket"
        ],
        "parts_needed": [
            "Coolant",
            "Gasket Kit",
            "Turbo Hose"
        ],
        "specialist": "Engine Diagnostics Specialist",
        "estimated_hours": "5-10",
        "insurance": "Partial"
    },

    # =========================================================
    # BRAKING SYSTEM
    # =========================================================

    "brake failure": {
        "severity": "CRITICAL",
        "safe_to_drive": False,
        "inspection_level": "Brake Emergency Inspection",
        "systems_to_check": [
            "Brake Pads",
            "Brake Disc",
            "Brake Fluid",
            "Brake Line",
            "ABS Module",
            "Master Cylinder"
        ],
        "parts_needed": [
            "Brake Pads",
            "Brake Disc",
            "Brake Fluid",
            "Brake Line"
        ],
        "specialist": "Brake Specialist",
        "estimated_hours": "4-7",
        "insurance": "Not Covered"
    },

    "brake vibration": {
        "severity": "HIGH",
        "safe_to_drive": False,
        "inspection_level": "Brake & Suspension Inspection",
        "systems_to_check": [
            "Brake Rotor",
            "Brake Disc",
            "Wheel Alignment",
            "Suspension",
            "Tyre Wear"
        ],
        "parts_needed": [
            "Brake Rotor",
            "Brake Disc"
        ],
        "specialist": "Brake & Suspension Specialist",
        "estimated_hours": "3-5",
        "insurance": "Not Covered"
    },

    "brake noise": {
        "severity": "HIGH",
        "safe_to_drive": False,
        "inspection_level": "Brake Inspection",
        "systems_to_check": [
            "Brake Pads",
            "Brake Caliper",
            "Brake Disc",
            "Brake Fluid"
        ],
        "parts_needed": [
            "Brake Pads",
            "Brake Fluid"
        ],
        "specialist": "Brake Specialist",
        "estimated_hours": "2-4",
        "insurance": "Not Covered"
    },

    # =========================================================
    # ELECTRICAL
    # =========================================================

    "battery": {
        "severity": "MEDIUM",
        "safe_to_drive": True,
        "inspection_level": "Electrical Diagnostics",
        "systems_to_check": [
            "Battery Voltage",
            "Alternator",
            "Starter Motor",
            "Battery Terminal",
            "Charging System"
        ],
        "parts_needed": [
            "Battery",
            "Fuse Kit",
            "Alternator Belt"
        ],
        "specialist": "Electrical Specialist",
        "estimated_hours": "1-3",
        "insurance": "Not Covered"
    },

    "wiring": {
        "severity": "HIGH",
        "safe_to_drive": False,
        "inspection_level": "Electrical Wiring Inspection",
        "systems_to_check": [
            "Wiring Harness",
            "Fuse Box",
            "ECU",
            "Battery",
            "Ground Connection"
        ],
        "parts_needed": [
            "Wiring Kit",
            "Fuse Kit",
            "Relay"
        ],
        "specialist": "Electrical Specialist",
        "estimated_hours": "4-8",
        "insurance": "Partial"
    },

    "headlight": {
        "severity": "LOW",
        "safe_to_drive": True,
        "inspection_level": "Lighting Inspection",
        "systems_to_check": [
            "Headlight Unit",
            "Relay",
            "Fuse",
            "Battery Voltage"
        ],
        "parts_needed": [
            "Headlight Bulb",
            "Relay",
            "Fuse"
        ],
        "specialist": "Electrical Specialist",
        "estimated_hours": "1-2",
        "insurance": "Not Covered"
    },

    # =========================================================
    # AC / HVAC
    # =========================================================

    "ac not cooling": {
        "severity": "MEDIUM",
        "safe_to_drive": True,
        "inspection_level": "HVAC Diagnostics",
        "systems_to_check": [
            "AC Compressor",
            "Condenser",
            "Cooling Coil",
            "Cabin Filter",
            "AC Gas Pressure"
        ],
        "parts_needed": [
            "AC Gas",
            "Cabin Air Filter",
            "AC Compressor Oil"
        ],
        "specialist": "HVAC Specialist",
        "estimated_hours": "2-5",
        "insurance": "Not Covered"
    },

    # =========================================================
    # TYRES / SUSPENSION
    # =========================================================

    "tyre puncture": {
        "severity": "MEDIUM",
        "safe_to_drive": False,
        "inspection_level": "Tyre Inspection",
        "systems_to_check": [
            "Tyre Pressure",
            "Wheel Alignment",
            "Tyre Sidewall",
            "Wheel Rim"
        ],
        "parts_needed": [
            "Tubeless Repair Kit",
            "Tyre Valve"
        ],
        "specialist": "Tyre Specialist",
        "estimated_hours": "1-2",
        "insurance": "Not Covered"
    },

    "suspension noise": {
        "severity": "HIGH",
        "safe_to_drive": False,
        "inspection_level": "Suspension Inspection",
        "systems_to_check": [
            "Shock Absorber",
            "Lower Arm",
            "Suspension Bush",
            "Steering Rack"
        ],
        "parts_needed": [
            "Shock Absorber",
            "Suspension Bush"
        ],
        "specialist": "Suspension Specialist",
        "estimated_hours": "4-6",
        "insurance": "Partial"
    },

    # =========================================================
    # BODY / ACCIDENT
    # =========================================================

    "dent": {
        "severity": "MEDIUM",
        "safe_to_drive": True,
        "inspection_level": "Body Inspection",
        "systems_to_check": [
            "Door Panel",
            "Fender",
            "Paint Damage",
            "Bumper Alignment"
        ],
        "parts_needed": [
            "Body Filler",
            "Paint Kit",
            "Panel Clip"
        ],
        "specialist": "Body Shop Specialist",
        "estimated_hours": "5-12",
        "insurance": "Covered"
    },

    "bumper damage": {
        "severity": "MEDIUM",
        "safe_to_drive": True,
        "inspection_level": "Body Repair Inspection",
        "systems_to_check": [
            "Front Bumper",
            "Rear Bumper",
            "Parking Sensors",
            "Mounting Brackets"
        ],
        "parts_needed": [
            "Bumper Assembly",
            "Sensor Clip",
            "Paint Kit"
        ],
        "specialist": "Body Shop Specialist",
        "estimated_hours": "4-8",
        "insurance": "Covered"
    },

    "accident": {
        "severity": "CRITICAL",
        "safe_to_drive": False,
        "inspection_level": "Accidental Damage Assessment",
        "systems_to_check": [
            "Chassis Alignment",
            "Suspension Damage",
            "Airbags",
            "Body Frame",
            "Steering Column"
        ],
        "parts_needed": [
            "Airbag Module",
            "Bumper Assembly",
            "Suspension Kit"
        ],
        "specialist": "Insurance Inspection Specialist",
        "estimated_hours": "10-20",
        "insurance": "Covered"
    },

    # =========================================================
    # SERVICE
    # =========================================================

    "service": {
        "severity": "LOW",
        "safe_to_drive": True,
        "inspection_level": "Periodic Service",
        "systems_to_check": [
            "Engine Oil",
            "Oil Filter",
            "Air Filter",
            "Brake Fluid",
            "Coolant",
            "Battery Health",
            "Tyre Pressure",
            "Wheel Alignment"
        ],
        "parts_needed": [
            "Engine Oil",
            "Oil Filter",
            "Air Filter",
            "Coolant"
        ],
        "specialist": "General Service Technician",
        "estimated_hours": "2-4",
        "insurance": "Not Covered"
    }
}