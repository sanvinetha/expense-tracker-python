# Expense Tracker

A simple and user-friendly command-line expense tracker built with Python. It helps you record daily expenses, review past entries, calculate totals, and generate reports by category and month.

## Overview

Expense Tracker is a lightweight personal finance tool designed for quick expense management from the terminal. It stores data in JSON and CSV files so your records remain available across runs.

## Features

- Add new expenses with description, amount, category, and date
- View all saved expenses in a readable table format
- Show the total amount spent
- Remove existing expenses safely
- Search expenses by title or category
- Edit existing expense entries
- Generate a category-wise spending report
- Generate a monthly expense report
- Export a summary to a text file
- Validate user input to avoid crashes from invalid entries

## Technologies Used

- Python 3
- Standard library modules:
  - csv
  - json
  - os
  - datetime

## Installation

1. Clone or download this repository.
2. Open the project folder.
3. Run the program with Python:

```bash
python main.py
```

## Usage

When you run the program, you will see a menu with several options:

1. Add expense
2. View expenses
3. Show total expenses
4. Remove an expense
5. Search expense
6. Edit expense
7. Category-wise Report
8. Monthly Expense Report
9. Export summary
10. Exit

Follow the on-screen prompts to add or manage expenses.

## Project Structure

```text
Expense Tracker/
├── main.py
├── expenses.csv
├── expenses.json
├── README.md
└── summary.txt   (created after exporting a summary)
```

## Sample Output

```text
Choose an option:
1. Add expense
2. View expenses
3. Show total expenses
4. Remove an expense
5. Search expense
6. Edit expense
7. Category-wise Report
8. Monthly Expense Report
9. Export summary
10. Exit
```

```text
Monthly Expense Report:
Month                  Total
-----------------------------
April 2026             16.49
May 2026                7.75
-----------------------------
Grand Total            24.24
```

## Future Improvements

Potential enhancements for future versions:

- Add graphical charts and visual summaries
- Support monthly budgets and spending limits
- Add filtering by date range
- Include persistent login or user profiles
- Improve data export to CSV/Excel formats

## Author

Created by Sanvi Cheruku and Srivalli Kakkireni.
