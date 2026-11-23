"""Save and retrieve equipment using a local SQLite database."""

import os
import sqlite3

DATABASE = os.path.join(os.path.dirname(__file__), "inventory.db")

# Sample school labels for our project demonstration.
SCHOOLS = ["School 1", "School 2", "School 3", "School 4", "School 5", "School 6"]


def create_table():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Equipment (
            AssetTag TEXT PRIMARY KEY,
            Type TEXT NOT NULL,
            Model TEXT NOT NULL,
            Status TEXT NOT NULL DEFAULT 'Available',
            School TEXT NOT NULL DEFAULT 'Unassigned',
            AssignedTo TEXT NOT NULL DEFAULT '',
            AssignedRole TEXT NOT NULL DEFAULT ''
        )
    """)

    # Add new columns to older versions without deleting saved equipment.
    cursor.execute("PRAGMA table_info(Equipment)")
    columns = [column[1] for column in cursor.fetchall()]

    if "School" not in columns:
        cursor.execute("ALTER TABLE Equipment ADD COLUMN School TEXT NOT NULL DEFAULT 'Unassigned'")
    if "AssignedTo" not in columns:
        cursor.execute("ALTER TABLE Equipment ADD COLUMN AssignedTo TEXT NOT NULL DEFAULT ''")
    if "AssignedRole" not in columns:
        cursor.execute("ALTER TABLE Equipment ADD COLUMN AssignedRole TEXT NOT NULL DEFAULT ''")

    connection.commit()
    connection.close()


def add_equipment(asset_tag, equipment_type, model, school):
    connection = sqlite3.connect(DATABASE)
    try:
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO Equipment (AssetTag, Type, Model, School) VALUES (?, ?, ?, ?)",
            (asset_tag, equipment_type, model, school)
        )
        connection.commit()
    finally:
        connection.close()


def view_equipment(school="All Schools", equipment_type="All Types"):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    fields = "AssetTag, Type, Model, School, Status, AssignedTo, AssignedRole"

    if school == "All Schools" and equipment_type == "All Types":
        cursor.execute(f"SELECT {fields} FROM Equipment ORDER BY AssetTag")
    elif school == "All Schools":
        cursor.execute(
            f"SELECT {fields} FROM Equipment WHERE Type = ? ORDER BY AssetTag",
            (equipment_type,)
        )
    elif equipment_type == "All Types":
        cursor.execute(
            f"SELECT {fields} FROM Equipment WHERE School = ? ORDER BY AssetTag",
            (school,)
        )
    else:
        cursor.execute(
            f"SELECT {fields} FROM Equipment WHERE School = ? AND Type = ? ORDER BY AssetTag",
            (school, equipment_type)
        )

    equipment = cursor.fetchall()
    connection.close()
    return equipment


def school_counts():
    """Count only Chromebooks for each school, grouped by status."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("SELECT School, Status FROM Equipment WHERE Type = 'Chromebook'")
    chromebooks = cursor.fetchall()
    connection.close()

    results = []
    for school in SCHOOLS:
        total = 0
        available = 0
        assigned = 0
        repair = 0

        for record_school, status in chromebooks:
            if record_school == school:
                total += 1
                if status == "Available":
                    available += 1
                elif status == "Assigned":
                    assigned += 1
                elif status == "Repair":
                    repair += 1

        results.append((school, total, available, assigned, repair))

    return results


def unassign_equipment(asset_tag):
    """Remove the assignee but keep the equipment in the inventory."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Equipment SET Status = 'Available', AssignedTo = '', AssignedRole = '' "
        "WHERE AssetTag = ? AND Status = 'Assigned'",
        (asset_tag,)
    )
    changed = cursor.rowcount > 0
    connection.commit()
    connection.close()
    return changed


def delete_equipment(asset_tag):
    """Permanently delete an equipment record by asset tag."""
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Equipment WHERE AssetTag = ?", (asset_tag,))
    deleted = cursor.rowcount > 0
    connection.commit()
    connection.close()
    return deleted


def add_demo_equipment():
    """Add sample Chromebooks, staff laptops, projectors, and cameras."""
    chromebook_counts = [3, 5, 2, 6, 4, 7]
    chromebook_models = ["Dell 3100", "HP Chromebook", "ASUS Chromebook"]

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Each school has a different number of Chromebooks.
    for school_number in range(1, 7):
        school = SCHOOLS[school_number - 1]
        for number in range(1, chromebook_counts[school_number - 1] + 1):
            asset_tag = f"DEMO-{school_number}-{number:03d}"  # Same IDs as the earlier demo version.
            model = chromebook_models[(school_number + number) % len(chromebook_models)]
            status = "Available"
            assigned_to = ""
            assigned_role = ""

            if number == 1:
                status = "Assigned"
                assigned_to = f"Sample Student {school_number:02d}"
                assigned_role = "Student"
            elif number == 2 and school_number in [2, 4]:
                status = "Repair"
            elif number == 3 and school_number in [1, 5]:
                status = "Assigned"
                assigned_to = f"Sample Staff {school_number:02d}"
                assigned_role = "Staff"

            cursor.execute(
                "INSERT OR IGNORE INTO Equipment "
                "(AssetTag, Type, Model, School, Status, AssignedTo, AssignedRole) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                (asset_tag, "Chromebook", model, school, status, assigned_to, assigned_role)
            )

    # A handful of other devices, including laptops issued to staff.
    extra_devices = [
        ("DEMO-LT-101", "Laptop", "HP Laptop", "School 1", "Assigned", "Sample Staff 07", "Staff"),
        ("DEMO-LT-102", "Laptop", "ASUS Laptop", "School 2", "Assigned", "Sample Staff 08", "Staff"),
        ("DEMO-LT-103", "Laptop", "HP Laptop", "School 3", "Assigned", "Sample Staff 09", "Staff"),
        ("DEMO-LT-104", "Laptop", "ASUS Laptop", "School 4", "Available", "", ""),
        ("DEMO-LT-105", "Laptop", "HP Laptop", "School 5", "Assigned", "Sample Staff 10", "Staff"),
        ("DEMO-LT-106", "Laptop", "ASUS Laptop", "School 6", "Available", "", ""),
        ("DEMO-PJ-101", "Projector", "Model unknown", "School 1", "Available", "", ""),
        ("DEMO-PJ-102", "Projector", "Model unknown", "School 3", "Available", "", ""),
        ("DEMO-PJ-103", "Projector", "Model unknown", "School 5", "Repair", "", ""),
        ("DEMO-CAM-101", "Camera", "Model unknown", "School 2", "Available", "", ""),
        ("DEMO-CAM-102", "Camera", "Model unknown", "School 4", "Available", "", ""),
        ("DEMO-CAM-103", "Camera", "Model unknown", "School 6", "Available", "", "")
    ]

    for device in extra_devices:
        cursor.execute(
            "INSERT OR IGNORE INTO Equipment "
            "(AssetTag, Type, Model, School, Status, AssignedTo, AssignedRole) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            device
        )

    connection.commit()
    connection.close()
