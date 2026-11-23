"""School IT Equipment Inventory Tracker - basic Tkinter application."""

import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk

from database import (SCHOOLS, create_table, add_equipment, view_equipment,
                      school_counts, add_demo_equipment, unassign_equipment, delete_equipment)


def save_equipment():
    asset_tag = asset_entry.get().strip()
    equipment_type = type_choice.get()
    model = model_entry.get().strip()
    school = school_choice.get()

    if asset_tag == "" or model == "":
        messagebox.showerror("Missing information", "Enter an asset tag and model.")
        return

    try:
        add_equipment(asset_tag, equipment_type, model, school)
    except sqlite3.IntegrityError:
        messagebox.showerror("Duplicate", "That asset tag already exists.")
        return

    asset_entry.delete(0, tk.END)
    model_entry.delete(0, tk.END)
    refresh_screen()
    messagebox.showinfo("Saved", "Equipment registered successfully!")


def show_equipment():
    for item in equipment_table.get_children():
        equipment_table.delete(item)

    selected_school = filter_choice.get()
    selected_type = type_filter.get()
    for record in view_equipment(selected_school, selected_type):
        equipment_table.insert("", tk.END, values=record)


def show_school_counts():
    for index, row in enumerate(school_counts()):
        school, total, available, assigned, repair = row
        count_labels[index].config(text=f"{total:>5}      {available:>8}      {assigned:>8}      {repair:>6}")


def refresh_screen():
    show_equipment()
    show_school_counts()


def load_demo_data():
    add_demo_equipment()
    refresh_screen()
    messagebox.showinfo("Demo records", "Demo equipment records were added for six schools.")


def get_selected_asset_tag():
    selected = equipment_table.selection()
    if not selected:
        messagebox.showwarning("Select equipment", "Select a row in the equipment list first.")
        return None
    return equipment_table.item(selected[0], "values")[0]


def remove_assignment():
    asset_tag = get_selected_asset_tag()
    if asset_tag is None:
        return

    if unassign_equipment(asset_tag):
        refresh_screen()
        messagebox.showinfo("Assignment removed", "Equipment is now Available.")
    else:
        messagebox.showerror("Not assigned", "This equipment is not currently assigned.")


def remove_equipment():
    asset_tag = get_selected_asset_tag()
    if asset_tag is None:
        return

    confirmed = messagebox.askyesno(
        "Delete equipment", f"Permanently remove {asset_tag} from the database?"
    )
    if not confirmed:
        return

    if delete_equipment(asset_tag):
        refresh_screen()
        messagebox.showinfo("Equipment deleted", f"{asset_tag} was removed.")
    else:
        messagebox.showerror("Not found", "This equipment record was not found.")


create_table()

window = tk.Tk()
window.title("School IT Equipment Inventory Tracker")
window.geometry("1130x680")

heading = tk.Frame(window)
heading.pack(fill="x", pady=12)
tk.Label(heading, text="School IT Equipment Inventory Tracker", font=("Arial", 18, "bold")).pack()
tk.Label(heading, text="District equipment records | School and staff data only").pack()

top = tk.Frame(window)
top.pack(fill="x", padx=15)

registration = tk.LabelFrame(top, text="Register Equipment", padx=15, pady=8)
registration.pack(side="left", fill="both", padx=(0, 12))

tk.Label(registration, text="Asset Tag:").pack(anchor="w")
asset_entry = tk.Entry(registration, width=31)
asset_entry.pack(pady=(0, 8))

tk.Label(registration, text="Equipment Type:").pack(anchor="w")
type_choice = tk.StringVar(value="Chromebook")
tk.OptionMenu(registration, type_choice, "Chromebook", "Laptop", "Projector", "Camera", "Other").pack(anchor="w", pady=(0, 8))

tk.Label(registration, text="Model (e.g. Dell 3100, HP, ASUS):").pack(anchor="w")
model_entry = tk.Entry(registration, width=31)
model_entry.pack(pady=(0, 8))

tk.Label(registration, text="School:").pack(anchor="w")
school_choice = tk.StringVar(value=SCHOOLS[0])
tk.OptionMenu(registration, school_choice, *SCHOOLS).pack(anchor="w", pady=(0, 8))

tk.Button(registration, text="Add Equipment", command=save_equipment).pack(anchor="w", pady=4)

summary = tk.LabelFrame(top, text="Chromebooks by School", padx=12, pady=10)
summary.pack(side="left", fill="both", expand=True)

tk.Label(summary, text="School", font=("Arial", 10, "bold"), width=15, anchor="w").grid(row=0, column=0, sticky="w")
tk.Label(summary, text="Total       Available       Assigned       Repair", font=("Consolas", 10, "bold")).grid(row=0, column=1, sticky="w")

count_labels = []
for index, school in enumerate(SCHOOLS):
    tk.Label(summary, text=school, width=15, anchor="w").grid(row=index + 1, column=0, pady=9, sticky="w")
    label = tk.Label(summary, text="", font=("Consolas", 10), anchor="w")
    label.grid(row=index + 1, column=1, sticky="w")
    count_labels.append(label)

tk.Label(summary, text="Totals count Chromebooks only; other equipment appears below.", fg="gray").grid(
    row=7, column=0, columnspan=2, pady=(10, 0), sticky="w")

inventory = tk.LabelFrame(window, text="Equipment Inventory", padx=10, pady=8)
inventory.pack(fill="both", expand=True, padx=15, pady=12)

controls = tk.Frame(inventory)
controls.pack(fill="x", pady=(0, 8))
tk.Label(controls, text="Show school:").pack(side="left")
filter_choice = tk.StringVar(value="All Schools")
filter_menu = ttk.Combobox(controls, textvariable=filter_choice, values=["All Schools"] + SCHOOLS + ["Unassigned"], state="readonly", width=16)
filter_menu.pack(side="left", padx=7)
filter_menu.bind("<<ComboboxSelected>>", lambda event: show_equipment())

tk.Label(controls, text="Equipment:").pack(side="left", padx=(10, 0))
type_filter = tk.StringVar(value="All Types")
type_menu = ttk.Combobox(controls, textvariable=type_filter,
                         values=["All Types", "Chromebook", "Laptop", "Projector", "Camera", "Other"],
                         state="readonly", width=14)
type_menu.pack(side="left", padx=7)
type_menu.bind("<<ComboboxSelected>>", lambda event: show_equipment())

tk.Button(controls, text="Refresh", command=refresh_screen).pack(side="left", padx=5)
tk.Button(controls, text="Unassign Selected", command=remove_assignment).pack(side="left", padx=5)
tk.Button(controls, text="Delete Selected", command=remove_equipment).pack(side="left", padx=5)
tk.Button(controls, text="Add Demo Records", command=load_demo_data).pack(side="right")

columns = ("Asset Tag", "Type", "Model", "School", "Status", "Assigned To", "Role")
equipment_table = ttk.Treeview(inventory, columns=columns, show="headings", height=11)
widths = (145, 100, 190, 110, 95, 160, 100)
for index, column in enumerate(columns):
    equipment_table.heading(column, text=column)
    equipment_table.column(column, width=widths[index], minwidth=70)
equipment_table.pack(fill="both", expand=True)

refresh_screen()
window.mainloop()
