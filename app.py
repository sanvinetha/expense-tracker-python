import streamlit as st
from datetime import datetime
from main import (load_expenses, save_expenses, format_date, expense_charts, monthly_expense_report, export_summary,)

st.set_page_config(page_title="Expense Tracker", page_icon="💰")

st.title("💰 Expense Tracker")

menu = st.sidebar.selectbox(
    "Menu",
    [
        "Home",
        "Add Expense",
        "View Expenses",
        "Total Expenses",
        "Category Report",
        "Search Expense",
        "Edit Expense",
        "Delete Expense",
        "Monthly Report",
        "Reports",
        "Charts",
        "Export Summary"
    ]
)

if menu == "Home":
    st.write("Welcome to the Expense Tracker!")

elif menu == "Add Expense":
    description = st.text_input("Description")

    amount = st.number_input("Amount", min_value=0.0)

    category = st.text_input("Category")

    date = st.date_input("Date")

    if st.button("Save Expense"):

        try:
            rows = load_expenses()
        except FileNotFoundError:
            rows = []

        rows.append({
            "description": description,
            "amount": str(amount),
            "category": category if category else "Uncategorized",
            "date": format_date(datetime.combine(date, datetime.min.time()))
        })

        save_expenses(rows)

        st.success("Expense saved successfully!")

elif menu == "View Expenses":
    try:
        rows = load_expenses()

        if rows:
            st.subheader("Saved Expenses")
            st.table(rows)
        else:
            st.info("No expenses found.")

    except FileNotFoundError:
        st.warning("No expenses found.")

elif menu == "Total Expenses":

    try:
        rows = load_expenses()

        total = 0

        for row in rows:
            total += float(row["amount"])

        st.metric("Total Expenses", f"₹ {total:.2f}")

    except FileNotFoundError:
        st.warning("No expenses found.")

elif menu == "Category Report":

    try:
        rows = load_expenses()

        category_totals = {}

        for row in rows:
            category = row["category"]

            amount = float(row["amount"])

            category_totals[category] = category_totals.get(category, 0) + amount

        st.subheader("Category-wise Report")

        st.table([
            {"Category": k, "Total": v}
            for k, v in category_totals.items()
        ])

    except FileNotFoundError:
        st.warning("No expenses found.")

elif menu == "Search Expense":

    try:
        rows = load_expenses()

        search = st.text_input("Enter description or category")

        if search:

            matches = []

            for row in rows:

                if (search.lower() in row["description"].lower()
                        or search.lower() in row["category"].lower()):

                    matches.append(row)

            if matches:
                st.subheader("Search Results")
                st.table(matches)
            else:
                st.warning("No matching expenses found.")

    except FileNotFoundError:
        st.warning("No expenses found.")

elif menu == "Edit Expense":

    try:
        rows = load_expenses()

        if not rows:
            st.warning("No expenses found.")
        else:
            st.subheader("Edit Expense")

            expense_list = [
                f"{i+1}. {row['description']} - ₹{row['amount']}"
                for i, row in enumerate(rows)
            ]

            selected = st.selectbox(
                "Select an expense",
                expense_list
            )

            index = expense_list.index(selected)
            expense = rows[index]

            description = st.text_input(
                "Description",
                value=expense["description"]
            )

            amount = st.number_input(
                "Amount",
                min_value=0.0,
                value=float(expense["amount"])
            )

            category = st.text_input(
                "Category",
                value=expense["category"]
            )

            if st.button("Update Expense"):

                expense["description"] = description
                expense["amount"] = amount
                expense["category"] = category

                save_expenses(rows)

                st.success("Expense updated successfully!")

    except FileNotFoundError:
        st.warning("No expenses found.")


elif menu == "Delete Expense":

    try:
        rows = load_expenses()

        if not rows:
            st.warning("No expenses found.")
        else:
            st.subheader("Delete Expense")

            expense_names = [
                f"{i+1}. {row['description']} - ₹{row['amount']}"
                for i, row in enumerate(rows)
            ]

            selected = st.selectbox(
                "Select an expense to delete",
                expense_names
            )

            if st.button("Delete Expense"):

                index = expense_names.index(selected)

                rows.pop(index)

                save_expenses(rows)

                st.success("Expense deleted successfully!")

    except FileNotFoundError:
        st.warning("No expenses found.")

elif menu == "Monthly Report":

    try:
        rows = load_expenses()

        monthly_totals = {}

        for row in rows:
            parts = row["date"].split()

            if len(parts) >= 2:
                month = f"{parts[-2]} {parts[-1]}"

                monthly_totals[month] = (
                    monthly_totals.get(month, 0)
                    + float(row["amount"])
                )

        st.subheader("Monthly Expense Report")

        st.table([
            {"Month": month, "Total": total}
            for month, total in monthly_totals.items()
        ])

    except FileNotFoundError:
        st.warning("No expenses found.")

elif menu == "Reports":
    st.write("This page will show reports.")

elif menu == "Charts":
    expense_charts()


    st.subheader("Expense Charts")

    import os

    if os.path.exists("charts/expense_distribution_pie.png"):
        st.image("charts/expense_distribution_pie.png", caption="Expense Distribution")

    if os.path.exists("charts/expense_totals_bar.png"):
        st.image("charts/expense_totals_bar.png", caption="Category Totals")

    if os.path.exists("charts/monthly_expense_trend.png"):
        st.image("charts/monthly_expense_trend.png", caption="Monthly Trend")

elif menu == "Export Summary":

    if st.button("Export Summary"):

        export_summary()

        st.success("Summary exported successfully!")

        st.info("The file 'summary.txt' has been created in your project folder.")