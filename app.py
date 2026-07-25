import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Page Configuration for Streamlit Cloud
st.set_page_config(
    page_title="Expense Tracker Python",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for rich aesthetics and dark/light styling
st.markdown("""
    <style>
    .main-header {
        font-family: 'Outfit', sans-serif;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6, #6366f1);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #94a3b8;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
    }
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
    }
    .google-btn {
        background-color: #ffffff !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        font-weight: 600 !important;
        width: 100%;
        padding: 0.6rem;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Data
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "expenses" not in st.session_state:
    st.session_state["expenses"] = [
        {"id": 101, "title": "Supermarket Groceries", "amount": 145.50, "category": "Groceries", "date": "2026-07-24", "payment_method": "Credit Card", "notes": "Weekly household food"},
        {"id": 102, "title": "Electric Utility Bill", "amount": 92.00, "category": "Utilities & Bills", "date": "2026-07-20", "payment_method": "UPI / Online Transfer", "notes": "Monthly electricity"},
        {"id": 103, "title": "Restaurant Dinner", "amount": 64.80, "category": "Food & Dining", "date": "2026-07-18", "payment_method": "Credit Card", "notes": "Dinner outing"},
        {"id": 104, "title": "Fuel Refill", "amount": 45.00, "category": "Transportation", "date": "2026-07-15", "payment_method": "Debit Card", "notes": "Gasoline for car"},
        {"id": 105, "title": "Online Shopping", "amount": 120.00, "category": "Shopping", "date": "2026-07-10", "payment_method": "Credit Card", "notes": "Headphones"}
    ]

# ==================== SIGN IN / LOGIN PAGE ==================== #
def render_login_page():
    st.markdown("<h1 class='main-header'>Expense Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header'>Manage your personal expenses effortlessly</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Welcome Back - Sign In")
        st.write("Please log in using your Mobile Number or Email ID")
        
        with st.form("login_form"):
            identity = st.text_input("Mobile Number or Email ID", placeholder="e.g. +1 234 567 8900 or user@example.com")
            password = st.text_input("Password / OTP", type="password", placeholder="Enter your password or OTP")
            submit_btn = st.form_submit_button("Sign In ➔", use_container_width=True)
            
            if submit_btn:
                if identity and password:
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = identity
                    st.success("Successfully signed in!")
                    st.rerun()
                else:
                    st.error("Please enter a valid Email/Mobile and Password.")
        
        st.markdown("<div style='text-align: center; margin: 1rem 0; color: #94a3b8;'>─── OR SIGN IN WITH ───</div>", unsafe_allow_html=True)
        
        # Google Email ID Option
        if st.button("🌐 Continue with Google Email ID", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = "google_user@gmail.com"
            st.success("Signed in with Google Email ID!")
            st.rerun()
            
        if st.button("🚀 Quick Demo Guest Login", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = "guest_user@example.com"
            st.rerun()

# ==================== MAIN DASHBOARD ==================== #
def render_dashboard():
    # Sidebar
    st.sidebar.markdown(f"### 👤 Signed In")
    st.sidebar.caption(f"**{st.session_state['user_email']}**")
    if st.sidebar.button("🚪 Sign Out"):
        st.session_state["logged_in"] = False
        st.rerun()
        
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📌 Key Features")
    
    navigation = st.sidebar.radio(
        "Select Feature Page:",
        [
            "💰 Total Expenses",
            "➕ Add Expenses",
            "📋 View Expenses",
            "🔍 Search Expenses",
            "📊 Category Report",
            "✏️ Edit Expense",
            "🗑️ Delete Expense",
            "📈 Chart Analytics",
            "📑 Financial Report",
            "📅 Monthly Expenses",
            "📥 Export Summary"
        ]
    )

    df = pd.DataFrame(st.session_state["expenses"])

    # 1. TOTAL EXPENSES
    if navigation == "💰 Total Expenses":
        st.title("💰 Total Expenses Summary")
        
        if not df.empty:
            total_amount = df["amount"].sum()
            total_count = len(df)
            avg_amount = df["amount"].mean()
            top_category = df.groupby("category")["amount"].sum().idxmax()
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Expenses", f"${total_amount:,.2f}")
            c2.metric("Total Transactions", total_count)
            c3.metric("Average Expense", f"${avg_amount:,.2f}")
            c4.metric("Top Category", top_category)
            
            st.markdown("---")
            st.subheader("Recent Expenses Activity")
            st.dataframe(df.sort_values(by="date", ascending=False).head(5), use_container_width=True)
        else:
            st.info("No expense data recorded yet.")

    # 2. ADD EXPENSES
    elif navigation == "➕ Add Expenses":
        st.title("➕ Add New Expense")
        
        with st.form("add_expense_form"):
            col_a, col_b = st.columns(2)
            title = col_a.text_input("Expense Title", placeholder="e.g. Grocery Shopping")
            amount = col_b.number_input("Amount ($)", min_value=0.01, step=1.0)
            
            col_c, col_d, col_e = st.columns(3)
            category = col_c.selectbox("Category", ["Groceries", "Food & Dining", "Transportation", "Utilities & Bills", "Shopping", "Entertainment", "Health & Medical", "Other"])
            exp_date = col_d.date_input("Date", datetime.today())
            payment_method = col_e.selectbox("Payment Method", ["Credit Card", "Debit Card", "UPI / Online Transfer", "Cash"])
            
            notes = st.text_area("Notes (Optional)", placeholder="Additional details...")
            
            submitted = st.form_submit_button("Submit Expense", use_container_width=True)
            if submitted:
                if title:
                    new_item = {
                        "id": int(datetime.now().timestamp()),
                        "title": title,
                        "amount": float(amount),
                        "category": category,
                        "date": str(exp_date),
                        "payment_method": payment_method,
                        "notes": notes
                    }
                    st.session_state["expenses"].insert(0, new_item)
                    st.success(f"Successfully added expense: {title} (${amount:.2f})")
                    st.rerun()
                else:
                    st.error("Please enter an expense title.")

    # 3. VIEW EXPENSES
    elif navigation == "📋 View Expenses":
        st.title("📋 View All Expenses")
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No expenses found.")

    # 4. SEARCH EXPENSES
    elif navigation == "🔍 Search Expenses":
        st.title("🔍 Search & Filter Expenses")
        
        col_s1, col_s2, col_s3 = st.columns(3)
        keyword = col_s1.text_input("Search Keyword", placeholder="Title or notes...")
        category_filter = col_s2.selectbox("Filter Category", ["ALL"] + list(df["category"].unique() if not df.empty else []))
        payment_filter = col_s3.selectbox("Filter Payment Method", ["ALL"] + list(df["payment_method"].unique() if not df.empty else []))
        
        filtered_df = df.copy()
        if not filtered_df.empty:
            if keyword:
                filtered_df = filtered_df[filtered_df["title"].str.contains(keyword, case=False, na=False) | filtered_df["notes"].str.contains(keyword, case=False, na=False)]
            if category_filter != "ALL":
                filtered_df = filtered_df[filtered_df["category"] == category_filter]
            if payment_filter != "ALL":
                filtered_df = filtered_df[filtered_df["payment_method"] == payment_filter]
                
            st.write(f"Found {len(filtered_df)} matching transactions:")
            st.dataframe(filtered_df, use_container_width=True)

    # 5. CATEGORY REPORT
    elif navigation == "📊 Category Report":
        st.title("📊 Category Breakdown Report")
        if not df.empty:
            cat_df = df.groupby("category")["amount"].agg(["sum", "count"]).reset_index()
            cat_df.columns = ["Category", "Total Spent ($)", "Transaction Count"]
            total_sum = cat_df["Total Spent ($)"].sum()
            cat_df["Percentage (%)"] = (cat_df["Total Spent ($)"] / total_sum * 100).round(1)
            
            st.dataframe(cat_df.sort_values(by="Total Spent ($)", ascending=False), use_container_width=True)
            
            fig = px.pie(cat_df, names="Category", values="Total Spent ($)", title="Category Spend Percentage", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)

    # 6. EDIT EXPENSE
    elif navigation == "✏️ Edit Expense":
        st.title("✏️ Edit Expense Entry")
        if not df.empty:
            expense_options = {f"#{row['id']} - {row['title']} (${row['amount']})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Select Expense to Edit:", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            selected_item = next((item for item in st.session_state["expenses"] if item["id"] == selected_id), None)
            
            if selected_item:
                with st.form("edit_form"):
                    edit_title = st.text_input("Title", value=selected_item["title"])
                    edit_amount = st.number_input("Amount ($)", value=float(selected_item["amount"]), step=1.0)
                    edit_category = st.selectbox("Category", ["Groceries", "Food & Dining", "Transportation", "Utilities & Bills", "Shopping", "Entertainment", "Health & Medical", "Other"], index=0)
                    edit_date = st.date_input("Date", datetime.strptime(selected_item["date"], "%Y-%m-%d"))
                    edit_payment = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "UPI / Online Transfer", "Cash"], index=0)
                    edit_notes = st.text_area("Notes", value=selected_item.get("notes", ""))
                    
                    if st.form_submit_button("Save Changes"):
                        selected_item["title"] = edit_title
                        selected_item["amount"] = edit_amount
                        selected_item["category"] = edit_category
                        selected_item["date"] = str(edit_date)
                        selected_item["payment_method"] = edit_payment
                        selected_item["notes"] = edit_notes
                        st.success("Expense updated successfully!")
                        st.rerun()

    # 7. DELETE EXPENSE
    elif navigation == "🗑️ Delete Expense":
        st.title("🗑️ Delete Expense Entry")
        if not df.empty:
            expense_options = {f"#{row['id']} - {row['title']} (${row['amount']})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Select Expense to Delete:", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            if st.button("❌ Confirm Delete Expense", type="primary"):
                st.session_state["expenses"] = [exp for exp in st.session_state["expenses"] if exp["id"] != selected_id]
                st.success("Expense deleted successfully!")
                st.rerun()

    # 8. CHART ANALYTICS
    elif navigation == "📈 Chart Analytics":
        st.title("📈 Visual Chart Analytics")
        if not df.empty:
            col_ch1, col_ch2 = st.columns(2)
            
            with col_ch1:
                fig_pie = px.pie(df, names="category", values="amount", title="Category Share", hole=0.3)
                st.plotly_chart(fig_pie, use_container_width=True)
                
            with col_ch2:
                df["month"] = df["date"].str.slice(0, 7)
                monthly_df = df.groupby("month")["amount"].sum().reset_index()
                fig_bar = px.bar(monthly_df, x="month", y="amount", title="Monthly Expense Trend", labels={"amount": "Amount ($)", "month": "Month"})
                st.plotly_chart(fig_bar, use_container_width=True)

    # 9. FINANCIAL REPORT
    elif navigation == "📑 Financial Report":
        st.title("📑 Financial Statement Report")
        if not df.empty:
            st.markdown(f"**Report Generated for User:** `{st.session_state['user_email']}`")
            st.markdown(f"**Date:** `{datetime.now().strftime('%B %d, %Y')}`")
            
            summary_df = df.groupby("category").agg(
                Total_Amount=("amount", "sum"),
                Transaction_Count=("amount", "count"),
                Average_Amount=("amount", "mean")
            ).reset_index()
            
            st.dataframe(summary_df, use_container_width=True)

    # 10. MONTHLY EXPENSES
    elif navigation == "📅 Monthly Expenses":
        st.title("📅 Monthly Expenses Breakdown")
        if not df.empty:
            df["Month-Year"] = df["date"].str.slice(0, 7)
            month_df = df.groupby("Month-Year").agg(
                Total_Spent=("amount", "sum"),
                Item_Count=("amount", "count"),
                Average_Spend=("amount", "mean")
            ).reset_index().sort_values(by="Month-Year", ascending=False)
            
            st.dataframe(month_df, use_container_width=True)

    # 11. EXPORT SUMMARY
    elif navigation == "📥 Export Summary":
        st.title("📥 Export Expense Summary")
        if not df.empty:
            csv_data = df.to_csv(index=False).encode('utf-8')
            json_data = json.dumps(st.session_state["expenses"], indent=2)
            
            c_exp1, c_exp2 = st.columns(2)
            with c_exp1:
                st.subheader("Export CSV File")
                st.download_button(
                    label="📄 Download CSV Report",
                    data=csv_data,
                    file_name=f"expense_report_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with c_exp2:
                st.subheader("Export JSON Data")
                st.download_button(
                    label="code Download JSON Backup",
                    data=json_data,
                    file_name=f"expense_backup_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )

# Main Application Entrypoint
if __name__ == "__main__":
    if not st.session_state["logged_in"]:
        render_login_page()
    else:
        render_dashboard()
