# School IT Equipment Inventory Tracker

A simple Python desktop application inspired by real school IT inventory workflows (including GQueues). This is an independent project with sample demonstration records.

## Technologies and requirements

- Python 3.10 or newer with Tkinter
- SQLite (built into Python)
- No MySQL server or external Python packages required for the current version

## How to run

1. Open the existing project folder (where `app.py` and `database.py` are located) in VS Code.
2. Open **Terminal > New Terminal**.
3. On Windows, run `py app.py`. On macOS, run `python3 app.py`.
4. The application creates `inventory.db` on first run and keeps saved records between restarts.

## Trying the application

1. Register equipment with an asset tag, equipment type, model, and school. Examples: `Chromebook` + `Dell 3100`, `Chromebook` + `HP Chromebook`, `Laptop` + `ASUS Laptop`, `Projector` + `Model unknown`.
2. The equipment appears in the inventory table with status `Available`.
3. To see realistic sample data, click **Add Demo Records**. This loads different numbers of Dell, HP, and ASUS Chromebooks in six sample schools, plus HP/ASUS staff laptops, projectors, and cameras.
4. Some demo devices show sample student/staff assignees and are marked `Assigned`. Other devices are `Available` or `Repair`.
5. Use the **Show school** and **Equipment** dropdowns to filter inventory. The school summary counts **Chromebooks only**, not laptops or other devices.
6. Demo records have repeat-safe asset tags. Clicking the demo button twice does not add duplicates.

## Removing an assignment or equipment

1. Click a row in the equipment inventory table.
2. Choose **Unassign Selected** to clear the person's name and role and change the status to **Available**. This works only for a device currently marked **Assigned**. The device stays in the inventory.
3. Choose **Delete Selected** to remove a device from the database completely. You will be asked to confirm before deletion.
4. Changes are saved immediately and remain after restarting the application. The school counts refresh automatically.
5. Clicking **Add Demo Records** again may restore deleted sample equipment. It will not overwrite the status of demo devices you have changed.

## Project files

- `app.py` – Tkinter interface
- `database.py` – SQLite storage, school counts, and sample demonstration data
- `.gitignore` – excludes local database and generated files from Git
- `inventory.db` – created on your computer and **not included** in this ZIP

## Known limitations / future Sprint 2 work

- The sample assignee names and roles in demo records are for demonstration only. You can unassign devices, but cannot yet assign a new person or search by person through the interface.
- Student IDs and staff IDs are not stored in this version. A future sprint will add people, searchable IDs, and real assignment/return workflows.
- The school names are placeholders, not actual district school names.
- Unknown device models are deliberately labeled `Model unknown` instead of guessing.
- The application runs locally on one computer and does not connect to GQueues or a district database.

## Important privacy note

Use only sample student/staff records when demonstrating or sharing your project. Never commit actual student IDs or assignments to a public GitHub repository.

## Updating from the previous version

Close the app, then replace `app.py`, `database.py`, and `README.md` in your existing project directory. **Do not delete your existing `inventory.db`**. The program will add the new columns on next launch without deleting saved equipment. You can change the subtitle of the interface in `app.py` to preserve any wording you customized.
