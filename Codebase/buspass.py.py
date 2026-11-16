# Bus Pass Management System
# PS No. 59
# Python 3

import os

FILE_NAME = "buspass.txt"

# Pass types and their fees
PASS_TYPES = {
    "Monthly": {"days": 30, "fee": 500},
    "Quarterly": {"days": 90, "fee": 1350},
    "Yearly": {"days": 365, "fee": 4800}
}

# List containing all bus pass dictionaries
passes = []


# Calculate fee and apply student discount
def calculate_fee(pass_type, category):
    fee = PASS_TYPES[pass_type]["fee"]

    if category == "Student":
        fee = fee * 0.75

    return float(fee)


# Generate the next pass ID
def next_pass_id():
    highest_number = 100

    for bus_pass in passes:
        pass_id = bus_pass["id"]

        if pass_id.startswith("BP"):
            try:
                number = int(pass_id[2:])
                highest_number = max(highest_number, number)
            except ValueError:
                continue

    return "BP" + str(highest_number + 1)


# Save all passes in the file
def save_passes():
    try:
        with open(FILE_NAME, "w", encoding="utf-8") as file:
            for p in passes:
                line = (
                    f'{p["id"]}|{p["name"]}|{p["route"]}|'
                    f'{p["type"]}|{p["category"]}|'
                    f'{p["fee"]}|{p["days"]}'
                )
                file.write(line + "\n")

    except OSError:
        print("Error: Could not save passes to the file.")


# Load previously saved passes
def load_passes():
    global passes
    passes = []

    if not os.path.exists(FILE_NAME):
        return

    try:
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            for line in file:
                fields = [x.strip() for x in line.strip().split("|")]

                if not fields or len(fields) < 5:
                    continue

                try:
                    pass_id = fields[0]
                    name = fields[1]
                    route = fields[2]
                    pass_type = fields[3].title()

                    if pass_type not in PASS_TYPES:
                        continue

                    # Support the older 5-field file format too
                    if len(fields) >= 7:
                        category = fields[4].title()
                        fee = float(fields[5].replace("Rs.", "").strip())
                        days = int(fields[6])

                    else:
                        category = "General"
                        fee_text = fields[4].replace("Rs.", "").strip()
                        fee = float(fee_text)
                        days = PASS_TYPES[pass_type]["days"]

                    if category not in ("General", "Student"):
                        continue

                    bus_pass = {
                        "id": pass_id,
                        "name": name,
                        "route": route,
                        "type": pass_type,
                        "category": category,
                        "fee": fee,
                        "days": days
                    }

                    passes.append(bus_pass)

                except (ValueError, IndexError):
                    continue

    except OSError:
        print("Warning: Could not load the saved passes.")


# Display one pass
def show_pass(p):
    fee = p["fee"]
    fee_text = (
        str(int(fee)) if fee.is_integer()
        else f"{fee:.2f}"
    )

    print(
        f'{p["id"]} | {p["name"]} | {p["route"]} | '
        f'{p["type"]} | Fee: Rs. {fee_text} | '
        f'Valid: {p["days"]} days'
    )


# Issue a new bus pass
def issue_pass():
    print("\n--- Issue New Pass ---")

    name = input("Enter passenger name: ").strip()
    route = input("Enter bus route: ").strip()

    if not name or not route:
        print("Name and route cannot be empty. Pass not issued.")
        return

    pass_type = input(
        "Enter pass type (Monthly/Quarterly/Yearly): "
    ).strip().title()

    if pass_type not in PASS_TYPES:
        print(
            "Invalid pass type. Choose Monthly, Quarterly or Yearly. "
            "Pass not issued."
        )
        return

    category = input(
        "Enter category (General/Student): "
    ).strip().title()

    if category not in ("General", "Student"):
        print(
            "Invalid category. Choose General or Student. "
            "Pass not issued."
        )
        return

    fee = calculate_fee(pass_type, category)

    bus_pass = {
        "id": next_pass_id(),
        "name": name,
        "route": route,
        "type": pass_type,
        "category": category,
        "fee": fee,
        "days": PASS_TYPES[pass_type]["days"]
    }

    passes.append(bus_pass)
    save_passes()

    fee_text = (
        str(int(fee)) if fee.is_integer()
        else f"{fee:.2f}"
    )

    print(
        f'Pass issued. ID: {bus_pass["id"]} | '
        f'{name} | {route} | {pass_type} | '
        f'Fee: Rs. {fee_text} | '
        f'Valid: {bus_pass["days"]} days'
    )


# Renew an existing pass
def renew_pass():
    print("\n--- Renew Existing Pass ---")
    pass_id = input("Enter pass ID to renew: ").strip().upper()

    for p in passes:
        if p["id"].upper() == pass_id:
            pass_type = input(
                "Enter new pass type (Monthly/Quarterly/Yearly): "
            ).strip().title()

            if pass_type not in PASS_TYPES:
                print("Invalid pass type. Pass not renewed.")
                return

            p["type"] = pass_type
            p["days"] = PASS_TYPES[pass_type]["days"]
            p["fee"] = calculate_fee(pass_type, p["category"])

            save_passes()
            print("Pass renewed successfully.")
            show_pass(p)
            return

    print("Pass ID not found. Pass not renewed.")


# Search a pass by ID
def search_pass():
    print("\n--- Search Pass ---")
    pass_id = input("Enter pass ID to search: ").strip().upper()

    for p in passes:
        if p["id"].upper() == pass_id:
            show_pass(p)
            return

    print("Pass ID not found.")


# Display all passes
def view_all_passes():
    print("\n--- All Bus Passes ---")

    if not passes:
        print("No passes issued yet.")
        return

    for p in passes:
        show_pass(p)


# Main menu
def main():
    load_passes()

    while True:
        print("\n====== BUS PASS MANAGEMENT SYSTEM ======")
        print("1. Issue New Pass")
        print("2. Renew Existing Pass")
        print("3. Search Pass by ID")
        print("4. View All Passes")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            issue_pass()

        elif choice == "2":
            renew_pass()

        elif choice == "3":
            search_pass()

        elif choice == "4":
            view_all_passes()

        elif choice == "5":
            save_passes()
            print("Thank you for using Bus Pass Management System.")
            break

        else:
            print("Invalid menu option. Please enter a number from 1 to 5.")



# Start the program
if __name__ == "__main__":
    main()