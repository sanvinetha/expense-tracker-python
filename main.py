import csv
import json
import os
from datetime import datetime

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JSON_FILE = "expenses.json"
CSV_FILE = "expenses.csv"


def _ordinal(day: int) -> str:
    if 10 <= day % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
    return f"{day}{suffix}"


def format_date(dt: datetime) -> str:
    return f"{_ordinal(dt.day)} {dt.strftime('%B %Y')}"


def get_non_empty_text(prompt: str, field_name: str) -> str:
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print(f"{field_name} cannot be empty. Please try again.")


def get_valid_amount(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        if not value:
            print("Amount cannot be empty. Please try again.")
            continue
        try:
            amount_value = float(value)
        except ValueError:
            print("Please enter a valid number for amount.")
            continue
        if amount_value < 0:
            print("Amount cannot be negative. Please try again.")
            continue
        return amount_value


def get_valid_category(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if not value:
            return "Uncategorized"
        if value.isdigit():
            print("Category must be text, not just numbers. Please try again.")
            continue
        return value


def get_valid_date(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value == "":
            return ""
        try:
            parsed = datetime.strptime(value, "%Y-%m-%d")
            return format_date(parsed)
        except ValueError:
            print("Date format invalid. Use YYYY-MM-DD.")


def get_menu_choice(prompt: str, valid_choices: list[str]) -> str:
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print(f"Invalid choice. Please enter one of: {', '.join(valid_choices)}.")


def write_expenses_to_csv(rows):
    """Persist expenses to the CSV file in a consistent format."""
    with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = ["description", "amount", "category", "date"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                "description": row.get("description", ""),
                "amount": row.get("amount", ""),
                "category": row.get("category", ""),
                "date": row.get("date", "")
            })


def save_expenses(rows):
    """Save expenses to both the JSON file and the CSV file."""
    with open(JSON_FILE, "w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)
    write_expenses_to_csv(rows)


def load_expenses():
    """Load expenses from JSON if available, otherwise fall back to CSV."""
    if os.path.exists(JSON_FILE):
        try:
            with open(JSON_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)
            if isinstance(data, list):
                return data
            raise ValueError("Invalid JSON format")
        except (json.JSONDecodeError, ValueError):
            print("Warning: expenses.json is corrupted. Falling back to CSV and creating a new JSON file.")
            corrupt_backup = JSON_FILE + ".bak"
            try:
                os.replace(JSON_FILE, corrupt_backup)
                print(f"Backed up corrupt file to {corrupt_backup}")
            except OSError:
                pass

    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            rows = list(reader)
        save_expenses(rows)
        return rows

    raise FileNotFoundError


def print_expense_table(rows):
    """Print rows in a clean table with fixed-width columns."""
    description_width = 30
    category_width = 12
    date_width = 18

    header = f"{'No.':<4} {'Description':<{description_width}} {'Amount':>10} {'Category':<{category_width}} {'Date':<{date_width}}"
    print(header)
    print('-' * len(header))

    for i, row in enumerate(rows, start=1):
        desc = row.get("description", "")[:description_width]
        amt = row.get("amount", "")
        cat = row.get("category", "")[:category_width]
        date = row.get("date", "")[:date_width]
        print(f"{i:<4} {desc:<{description_width}} {amt:>10} {cat:<{category_width}} {date:<{date_width}}")


def add_expense():
    # Ask user for description, amount, category, and date, then append to JSON and CSV
    print("Add a new expense")
    description = get_non_empty_text("Enter expense description: ", "Description")
    amount_value = get_valid_amount("Enter amount: ")
    category = get_valid_category("Enter category (e.g., food, transport) [optional]: ")
    date_value = get_valid_date("Enter date (YYYY-MM-DD) or press Enter for today: ")

    if date_value == "":
        date_value = format_date(datetime.today())

    try:
        rows = load_expenses()
    except FileNotFoundError:
        rows = []

    new_expense = {
        "description": description,
        "amount": str(amount_value),
        "category": category,
        "date": date_value,
    }
    rows.append(new_expense)
    save_expenses(rows)

    print("Expense saved!")


def view_expenses():
    # Read and print all expenses, showing category and date when present
    try:
        rows = load_expenses()

        if not rows:
            print("No expenses found.")
            return

        print("\nSaved expenses:")
        print_expense_table(rows)

    except FileNotFoundError:
        print("No expenses recorded yet (expenses.csv not found).")


def show_total_expenses():
    # Sum the 'amount' column and print the total
    total = 0.0
    found = False

    try:
        rows = load_expenses()
        for row in rows:
            amt_str = row.get("amount", "").strip()
            if not amt_str:
                continue
            try:
                total += float(amt_str)
                found = True
            except ValueError:
                continue

        if not found:
            print("No numeric expenses found to total.")
        else:
            print(f"Total expenses: {total:.2f}")

    except FileNotFoundError:
        print("No expenses recorded yet.")


def remove_expense():
    # Show expenses, ask user which one to remove, and save the remaining rows
    try:
        rows = load_expenses()

        if not rows:
            print("No expenses to remove.")
            return

    except FileNotFoundError:
        print("No expenses recorded yet (expenses.csv not found).")
        return

    # Display the list with numbers and extra fields
    print("\nWhich expense would you like to remove?")
    for i, row in enumerate(rows, start=1):
        desc = row.get("description", "")
        amt = row.get("amount", "")
        cat = row.get("category", "")
        date = row.get("date", "")
        parts = [f"{i}. {desc} - {amt}"]
        if cat:
            parts.append(f"[{cat}]")
        if date:
            parts.append(f"({date})")
        print(" ".join(parts))

    while True:
        choice = input("Enter the number to remove (or press Enter to cancel): ").strip()
        if choice == "":
            print("Cancelled.")
            return

        try:
            index = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if index < 1 or index > len(rows):
            print(f"Number out of range. Please choose 1-{len(rows)}.")
            continue

        break

    # Remove the selected row
    removed = rows.pop(index - 1)
    save_expenses(rows)

    print(f"Removed: {removed.get('description','')} - {removed.get('amount','')}")


def search_expenses():
    # Search expenses by description or category
    try:
        rows = load_expenses()

        if not rows:
            print("No expenses found.")
            return

    except FileNotFoundError:
        print("No expenses recorded yet (expenses.csv not found).")
        return

    while True:
        search_term = input("Enter title or category to search: ").strip().lower()
        if search_term:
            break
        print("Search text cannot be empty. Please try again.")

    matches = []
    for row in rows:
        description = row.get("description", "").lower()
        category = row.get("category", "").lower()
        if search_term in description or search_term in category:
            matches.append(row)

    if not matches:
        print("No expenses matched your search.")
        return

    print("\nSearch results:")
    print_expense_table(matches)


def edit_expense():
    # Allow the user to select and edit an existing expense
    try:
        rows = load_expenses()

        if not rows:
            print("No expenses to edit.")
            return

    except FileNotFoundError:
        print("No expenses recorded yet (expenses.csv not found).")
        return

    print("\nSelect an expense to edit:")
    print_expense_table(rows)

    while True:
        choice = input("Enter the expense number to edit (or press Enter to cancel): ").strip()
        if choice == "":
            print("Cancelled.")
            return

        try:
            index = int(choice)
        except ValueError:
            print("Please enter a valid number.")
            continue

        if index < 1 or index > len(rows):
            print(f"Number out of range. Please choose 1-{len(rows)}.")
            continue

        break

    expense = rows[index - 1]
    print(f"Editing expense {index}: {expense.get('description', '')} - {expense.get('amount', '')}")

    new_description = input("Enter new title (press Enter to keep current): ").strip()
    if new_description:
        expense['description'] = new_description

    while True:
        new_amount = input("Enter new amount (press Enter to keep current): ").strip()
        if new_amount == "":
            break
        try:
            amount_value = float(new_amount)
        except ValueError:
            print("Please enter a valid number for amount.")
            continue
        if amount_value < 0:
            print("Amount cannot be negative. Please try again.")
            continue
        expense['amount'] = str(amount_value)
        break

    while True:
        new_category = input("Enter new category (press Enter to keep current): ").strip()
        if new_category == "":
            break
        if new_category.isdigit():
            print("Category must be text, not just numbers. Please try again.")
            continue
        expense['category'] = new_category
        break

    save_expenses(rows)

    print("Expense updated successfully.")


def category_wise_report():
    # Calculate total spending per category and display it sorted by highest amount
    try:
        rows = load_expenses()

        if not rows:
            print("No expenses found.")
            return

    except FileNotFoundError:
        print("No expenses recorded yet.")
        return

    totals = {}
    for row in rows:
        category = row.get("category", "").strip() or "Uncategorized"
        amount_str = str(row.get("amount", "")).strip()
        try:
            amount_value = float(amount_str)
        except ValueError:
            continue
        totals[category] = totals.get(category, 0.0) + amount_value

    if not totals:
        print("No numeric expenses found to report.")
        return

    sorted_totals = sorted(totals.items(), key=lambda item: item[1], reverse=True)
    print("\nCategory-wise Report:")
    print(f"{'Category':<20} {'Total':>12}")
    print('-' * 33)
    for category, total in sorted_totals:
        print(f"{category:<20} {total:>12.2f}")
    print('-' * 33)
    print(f"{'Grand Total':<20} {sum(totals.values()):>12.2f}\n")


def monthly_expense_report():
    # Group total spending by month from the stored date labels and print a readable report
    try:
        rows = load_expenses()

        if not rows:
            print("No expenses found.")
            return

    except FileNotFoundError:
        print("No expenses recorded yet.")
        return

    monthly_totals = {}
    month_order = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }

    for row in rows:
        amount_str = str(row.get("amount", "")).strip()
        try:
            amount_value = float(amount_str)
        except ValueError:
            continue

        date_text = row.get("date", "").strip()
        parts = date_text.split()
        if len(parts) < 2:
            continue

        month_name = parts[-2]
        year_value = parts[-1]
        month_key = f"{month_name} {year_value}"
        monthly_totals[month_key] = monthly_totals.get(month_key, 0.0) + amount_value

    if not monthly_totals:
        print("No numeric expenses found to report.")
        return

    sorted_months = sorted(
        monthly_totals.items(),
        key=lambda item: (int(item[0].rsplit(" ", 1)[1]), month_order.get(item[0].rsplit(" ", 1)[0], 0))
    )

    print("\nMonthly Expense Report:")
    print(f"{'Month':<15} {'Total':>12}")
    print('-' * 29)
    for month_name, total in sorted_months:
        print(f"{month_name:<15} {total:>12.2f}")
    print('-' * 29)
    print(f"{'Grand Total':<15} {sum(monthly_totals.values()):>12.2f}\n")


def expense_charts():
    """Generate and save pie, bar, and line charts for the current expense data."""
    try:
        rows = load_expenses()
    except FileNotFoundError:
        print("No expenses recorded yet.")
        return

    if not rows:
        print("No expenses found to chart.")
        return

    charts_dir = os.path.join(os.getcwd(), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    category_totals = {}
    monthly_totals = {}
    month_order = {
        "January": 1,
        "February": 2,
        "March": 3,
        "April": 4,
        "May": 5,
        "June": 6,
        "July": 7,
        "August": 8,
        "September": 9,
        "October": 10,
        "November": 11,
        "December": 12,
    }

    for row in rows:
        amount_str = str(row.get("amount", "")).strip()
        try:
            amount_value = float(amount_str)
        except ValueError:
            continue

        category = row.get("category", "").strip() or "Uncategorized"
        category_totals[category] = category_totals.get(category, 0.0) + amount_value

        date_text = row.get("date", "").strip()
        parts = date_text.split()
        if len(parts) >= 2:
            month_name = parts[-2]
            year_value = parts[-1]
            month_key = f"{month_name} {year_value}"
            monthly_totals[month_key] = monthly_totals.get(month_key, 0.0) + amount_value

    if not category_totals:
        print("No numeric expenses found to chart.")
        return

    labels = list(category_totals.keys())
    values = list(category_totals.values())

    pie_fig, pie_ax = plt.subplots(figsize=(7, 7))
    pie_ax.pie(values, labels=labels, autopct="%1.1f%%", startangle=90)
    pie_ax.set_title("Expense Distribution by Category")
    pie_path = os.path.join(charts_dir, "expense_distribution_pie.png")
    pie_fig.savefig(pie_path, bbox_inches="tight")
    plt.close(pie_fig)

    bar_fig, bar_ax = plt.subplots(figsize=(8, 5))
    bar_ax.bar(labels, values, color="skyblue")
    bar_ax.set_title("Total Expenses by Category")
    bar_ax.set_ylabel("Amount")
    bar_ax.set_xlabel("Category")
    bar_ax.tick_params(axis="x", rotation=45)
    bar_path = os.path.join(charts_dir, "expense_totals_bar.png")
    bar_fig.savefig(bar_path, bbox_inches="tight")
    plt.close(bar_fig)

    if monthly_totals:
        sorted_months = sorted(
            monthly_totals.items(),
            key=lambda item: (int(item[0].rsplit(" ", 1)[1]), month_order.get(item[0].rsplit(" ", 1)[0], 0))
        )
        month_labels = [month for month, _ in sorted_months]
        month_values = [total for _, total in sorted_months]

        line_fig, line_ax = plt.subplots(figsize=(8, 5))
        line_ax.plot(month_labels, month_values, marker="o", color="green")
        line_ax.set_title("Monthly Expense Trend")
        line_ax.set_ylabel("Amount")
        line_ax.set_xlabel("Month")
        line_ax.tick_params(axis="x", rotation=45)
        line_path = os.path.join(charts_dir, "monthly_expense_trend.png")
        line_fig.savefig(line_path, bbox_inches="tight")
        plt.close(line_fig)

    print("Charts generated and saved to the charts folder.")
    print(f"Saved files: {pie_path}, {bar_path}")
    if monthly_totals:
        print(f"Saved files: {line_path}")


def export_summary():
    # Export a text summary with total and each expense
    try:
        rows = load_expenses()

        if not rows:
            print("No expenses found to export.")
            return

    except FileNotFoundError:
        print("No expenses recorded yet.")
        return

    total = 0.0
    lines = ["Expense Summary:\n"]

    for i, row in enumerate(rows, start=1):
        desc = row.get("description", "")
        amt = row.get("amount", "")
        cat = row.get("category", "")
        date = row.get("date", "")
        try:
            total += float(amt)
        except ValueError:
            pass

        parts = [f"{i}. {desc} - {amt}"]
        if cat:
            parts.append(f"[{cat}]")
        if date:
            parts.append(f"({date})")
        lines.append(" ".join(parts))

    lines.append(f"\nTotal expenses: {total:.2f}\n")

    with open("summary.txt", "w", encoding="utf-8") as summary_file:
        summary_file.write("\n".join(lines))

    print("Summary exported to summary.txt")


def main():
    # Attempt to load saved expenses on startup.
    try:
        load_expenses()
    except FileNotFoundError:
        pass

    # Menu to add, view, total, remove, export, or exit
    while True:
        print("\nChoose an option:")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Show total expenses")
        print("4. Remove an expense")
        print("5. Search expense")
        print("6. Edit expense")
        print("7. Category-wise Report")
        print("8. Monthly Expense Report")
        print("9. Expense Charts")
        print("10. Export summary")
        print("11. Exit")

        choice = get_menu_choice("Enter choice (1/2/3/4/5/6/7/8/9/10/11): ", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"])

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            show_total_expenses()
        elif choice == "4":
            remove_expense()
        elif choice == "5":
            search_expenses()
        elif choice == "6":
            edit_expense()
        elif choice == "7":
            category_wise_report()
        elif choice == "8":
            monthly_expense_report()
        elif choice == "9":
            expense_charts()
        elif choice == "10":
            export_summary()
        elif choice == "11":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, or 11.")


if __name__ == "__main__":
    main()