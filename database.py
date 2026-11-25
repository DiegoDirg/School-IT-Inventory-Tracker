'''
Diego Eusse
CS 319
Professor: Ankit Agrawal 
November 25, 2026
School IT Equipment Inventory Tracker
A simple softare application to track the inventory of IT equipment in a school district. 
The program allows users to register new equipment, view the inventory, and search for specific items by asset tag. It also provides a summary of equipment counts by school and allows for the unassignment and deletion of equipment records.
'''
"""Save and retrieve equipment using a local SQLite database."""

import os
import sqlite3

DATABASE = os.path.join(os.path.dirname(__file__), "inventory.db")

# Schools within the inventory system
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
            AssignedRole TEXT NOT NULL DEFAULT '',
            AssignedID TEXT NOT NULL DEFAULT ''
        )
    """)

    # Allow the addition of missing columns to older databases
    cursor.execute("PRAGMA table_info(Equipment)")
    columns = [column[1] for column in cursor.fetchall()]

    if "School" not in columns:
        cursor.execute("ALTER TABLE Equipment ADD COLUMN School TEXT NOT NULL DEFAULT 'Unassigned'")

    if "AssignedTo" not in columns:
        cursor.execute("ALTER TABLE Equipment ADD COLUMN AssignedTo TEXT NOT NULL DEFAULT ''")

    if "AssignedRole" not in columns:
        cursor.execute("ALTER TABLE Equipment ADD COLUMN AssignedRole TEXT NOT NULL DEFAULT ''")
    
    if "AssignedID" not in columns:
        cursor.execute("ALTER TABLE Equipment ADD COLUMN AssignedID TEXT NOT NULL DEFAULT ''")

    connection.commit()
    connection.close()


# Add new equipment
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


# Display equipment in the inventory
def view_equipment(school="All Schools", equipment_type="All Types"):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    fields = "AssetTag, Type, Model, School, Status, AssignedTo, AssignedRole, AssignedID"

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


#Search for equipment using the asset tag entered by the user
def search_equipment(asset_tag):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT AssetTag, Type, Model, School, Status, AssignedTo, AssignedRole, AssignedID"
        "FROM Equipment WHERE AssetTag = ?",
        (asset_tag.strip(),)
    )

    equipment = cursor.fetchone()

    connection.close()
    return equipment

#Search function to find equipment assigned to a specific person using the search text entered by the user.
def search_people(search_text):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT AssetTag, Type, Model, School, Status, AssignedTo, AssignedRole, AssignedID "
        "FROM Equipment WHERE AssignedTo LIKE ? OR AssignedID = ? ORDER BY AssetTag",
        ("%" + search_text.strip() + "%", search_text.strip())
    )

    equipment = cursor.fetchall()

    connection.close()
    return equipment

# Count of Chromebooks for each school
def school_counts():
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


# Remove the person assigned to equipment
def unassign_equipment(asset_tag):
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


# Delete equipment from the database
def delete_equipment(asset_tag):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM Equipment WHERE AssetTag = ?",
        (asset_tag,)
    )

    deleted = cursor.rowcount > 0

    connection.commit()
    connection.close()

    return deleted


# Add demonstration equipment records
def add_demo_equipment():
    chromebook_counts = [3, 5, 2, 6, 4, 7]

    chromebook_models = [
        "Dell 3100",
        "HP Chromebook",
        "ASUS Chromebook"
    ]

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # Each school has a different number of Chromebooks
    for school_number in range(1, 7):
        school = SCHOOLS[school_number - 1]

        for number in range(1, chromebook_counts[school_number - 1] + 1):
            asset_tag = f"DEMO-{school_number}-{number:03d}"
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

    # Other schools equipment
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

     # Give sample students their ID numbers
    for number in range(1, 7):
        name = f"Sample Student {number:02d}"
        student_id = f"STU-{number:03d}"

        cursor.execute(
            "UPDATE Equipment SET AssignedID = ? WHERE AssignedTo = ? AND AssignedID = ''",
            (student_id, name)
        )

    # Give sample staff their ID numbers
    for number in range(1, 11):
        name = f"Sample Staff {number:02d}"
        staff_id = f"STA-{number:03d}"

        cursor.execute(
            "UPDATE Equipment SET AssignedID = ? WHERE AssignedTo = ? AND AssignedID = ''",
            (staff_id, name)
        )

    connection.commit()
    connection.close()
