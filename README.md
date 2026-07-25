# Expense Tracker Python 💰

A modern, full-featured Python Expense Tracker web application featuring multi-method authentication (Email / Mobile Number & Google Sign-In) and an interactive post-login financial dashboard with 11 core module features.

---

## 🌟 Key Features Implemented

### 1. 🔐 Multi-Option Authentication Page (Sign-In / Login)
- **Email ID or Mobile Number Login**: Support for logging in via Mobile Number or Email ID with password/OTP verification.
- **Google Email ID Sign-In**: "Continue with Google Email ID" OAuth button situated directly below the main sign-in form.
- **Demo / Guest Access**: Quick one-click guest access for testing.

### 2. 📊 Post-Login Dashboard (Key Feature Modules)
After successful sign-in, the user is navigated to an interactive dashboard equipped with:
1. ➕ **Add Expenses**: Form to record title, amount, category, date, payment method, and optional notes.
2. 🔍 **Search Expenses**: Instant search and filter by keyword, category, and payment method.
3. 📋 **View Expenses**: Tabular list of all transactions with sorting and quick action buttons.
4. 💰 **Total Expenses**: Real-time summary cards displaying Total Spend, Total Count, Monthly Spend, and Top Category.
5. 📊 **Category Report**: Visual progress bars and percentage calculation of spending per category.
6. ✏️ **Edit Expense**: Modal window to update existing transaction details.
7. 🗑️ **Delete Expense**: Instant row deletion with confirmation prompt.
8. 📈 **Chart Analytics**: Interactive Chart.js visualizations including Donut Chart and Monthly Bar Chart.
9. 📑 **Financial Report**: Formatted summary statement of accounts.
10. 📥 **Export Summary**: One-click download of records as **CSV** or **JSON**, plus printable summary report.
11. 📅 **Monthly Expenses**: Historical month-by-month spending logs and itemized averages.

---

## 🚀 How to Run Locally

1. **Clone the Repository / Open Folder**:
   ```bash
   cd expense-tracker-python
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:
   ```bash
   python app.py
   ```

4. **Access in Browser**:
   Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your web browser.

---

## 🤝 Contribution Guidelines (Step-by-Step)

If you are contributing these changes to [sanvinetha/expense-tracker-python](https://github.com/sanvinetha/expense-tracker-python):

1. **Fork the Repository** on GitHub.
2. **Clone your Fork**:
   ```bash
   git clone https://github.com/<your-username>/expense-tracker-python.git
   ```
3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/auth-and-dashboard
   ```
4. **Copy the Updated Files** into your repository folder.
5. **Commit and Push**:
   ```bash
   git add .
   git commit -m "Add authentication page (Email/Mobile/Google) and post-login 11-key-points dashboard"
   git push origin feature/auth-and-dashboard
   ```
6. **Open a Pull Request (PR)** on GitHub targeting the main branch of `sanvinetha/expense-tracker-python`.
