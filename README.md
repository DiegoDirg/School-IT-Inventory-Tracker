# School IT Equipment Inventory Tracker

This is my CS 319 project. I created a simple Python application to keep track of school IT equipment, such as Chromebooks, laptops, projectors, and cameras. The project is based on school IT inventory work and uses sample records.

## Requirements

- Python 3.10 or newer
- Tkinter for the interface
- SQLite for the database

## How to run

1. Open the project folder in VS Code.
2. Open the terminal.
3. Run `py app.py`.
4. The application will open and create an `inventory.db` file if one does not already exist.

## Features

- Register equipment using an asset tag, equipment type, model, and school.
- View equipment and filter by school or equipment type.
- View Chromebook counts for each of the six schools.
- Search for equipment using an asset tag.
- Search for equipment assigned to a student or staff member using their name or ID.
- Unassign or delete equipment.
- Add sample equipment records using the **Add Demo Records** button.

## User Stories
For Sprint 2, I worked on two user stories based on locating equipment from my original project proposal.

User story 01 — Search Equipment by Asset Tag

As a technology staff member, I want to search for equipment using its asset tag so I can quickly locate a specific device.

User story 02 — Search Equipment by Student or Staff

As a technology staff member, I want to search for students or staff by their name or ID so I can identify which equipment is assigned to them.

Both user stories were completed and merged into the main branch through GitHub pull requests.

## SOLID Principles

For Sprint 2, I used two SOLID principles gatherd from our recent lecture in Week 10

**Single Responsibility Principle (SRP):** In `app.py`, I created the `display_result()` function to handle displaying search results instead of repeating that code.

**Dependency Inversion Principle (DIP):** In `people_search.py`, I created separate classes for searching people. The `PeopleSearchService` class receives a search source instead of directly depending on SQLite.

## Testing

I used pytest to create automated tests for the equipment and student/staff searches.

To install pytest, run:

`py -m pip install pytest`

To run the tests, use:

`py -m pytest -v`

All 5 automated tests passed.

## Project Files

- `app.py` - Main application and Tkinter interface.
- `database.py` - SQLite database functions.
- `people_search.py` - Classes used for the student/staff search.
- `Tests/test_database.py` - Automated tests.
- `inventory.db` - Local database created when running the program.

## Limitations

The application runs locally and does not connect to an actual school database which could still be done using MySQL. It uses sample student and staff information. New student or staff assignments cannot currently be created through the interface.