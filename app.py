import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import json

# Page Configuration for Streamlit Cloud
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Interactive Cards and Styled Buttons
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
    .savings-card {
        background: rgba(16, 185, 129, 0.12);
        border: 1px solid rgba(16, 185, 129, 0.3);
        border-radius: 12px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    .savings-title {
        font-weight: 700;
        color: #10b981;
        font-size: 1.1rem;
        margin-bottom: 0.25rem;
    }
    /* Style all action buttons to look like rich cards */
    div.stButton > button {
        border-radius: 12px !important;
        padding: 1rem 1.25rem !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        background: rgba(30, 41, 59, 0.7) !important;
        color: #f8fafc !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    div.stButton > button:hover {
        border-color: #3b82f6 !important;
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 18px rgba(59, 130, 246, 0.3) !important;
    }
    .nav-pill-active button {
        background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
        border-color: #6366f1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Data
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "💰 Total Expenses"
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []
if "eliminated_savings" not in st.session_state:
    st.session_state["eliminated_savings"] = 0.0

NON_ESSENTIAL_CATEGORIES = ["Food & Dining", "Shopping", "Entertainment", "Other"]

# Function to safely switch pages
def set_page(page_name):
    st.session_state["active_page"] = page_name

# ==================== SIGN IN / LOGIN PAGE ==================== #
def render_login_page():
    st.markdown("<h1 class='main-header' style='text-align: center;'>Expense Tracker</h1>", unsafe_allow_html=True)
    st.markdown("<p class='sub-header' style='text-align: center;'>Manage your personal expenses & save money in Rupees (₹)</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("Sign In to Access Dashboard")
        st.write("Please log in using your Mobile Number or Email ID")
        
        with st.form("login_form"):
            identity = st.text_input("Mobile Number or Email ID", placeholder="e.g. +91 98765 43210 or user@example.com")
            password = st.text_input("Password / OTP", type="password", placeholder="Enter password or OTP")
            submit_btn = st.form_submit_button("Sign In ➔", use_container_width=True)
            
            if submit_btn:
                if identity and password:
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = identity
                    st.success("Successfully signed in!")
                    st.rerun()
                else:
                    st.error("Please enter your Mobile Number or Email ID and Password.")
        
        st.markdown("<div style='text-align: center; margin: 1rem 0; color: #94a3b8;'>─── OR SIGN IN WITH ───</div>", unsafe_allow_html=True)
        
        if st.button("🌐 Continue with Google Email ID", key="login_google", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = "google_user@gmail.com"
            st.success("Signed in with Google Email ID!")
            st.rerun()
            
        if st.button("🚀 Quick Demo Guest Login", key="login_guest", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = "guest_user@example.com"
            st.rerun()

# ==================== MAIN HOME SCREEN ==================== #
def render_home_dashboard():
    # Top User Header Bar
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown("<h1 class='main-header'>Expense Tracker</h1>", unsafe_allow_html=True)
        st.markdown(f"Welcome back, **{st.session_state['user_email']}**! Track expenses & save money in Rupees (₹).", unsafe_allow_html=True)
    with head_col2:
        st.write("")
        if st.button("🚪 Sign Out", key="top_logout", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

    st.markdown("---")

    # TOP INTERACTIVE NAVIGATION BUTTONS BAR
    page_options = [
        "💰 Total Expenses",
        "💡 Save Money",
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

    # Render top interactive menu buttons across 6 columns x 2 rows
    nav_cols_1 = st.columns(6)
    for idx, page in enumerate(page_options[:6]):
        with nav_cols_1[idx]:
            is_active = (st.session_state["active_page"] == page)
            btn_label = f"▸ {page}" if is_active else page
            if st.button(btn_label, key=f"nav_top_{idx}", use_container_width=True):
                set_page(page)
                st.rerun()

    nav_cols_2 = st.columns(6)
    for idx, page in enumerate(page_options[6:]):
        with nav_cols_2[idx]:
            is_active = (st.session_state["active_page"] == page)
            btn_label = f"▸ {page}" if is_active else page
            if st.button(btn_label, key=f"nav_top_{idx+6}", use_container_width=True):
                set_page(page)
                st.rerun()

    st.markdown("---")

    df = pd.DataFrame(st.session_state["expenses"])
    current_page = st.session_state["active_page"]

    # ================= PAGE 1: TOTAL EXPENSES (HOME OVERVIEW) =================
    if current_page == "💰 Total Expenses":
        st.subheader("💰 Financial Summary (in ₹)")
        
        if not df.empty:
            total_amount = df["amount"].sum()
            total_count = len(df)
            avg_amount = df["amount"].mean()
            top_category = df.groupby("category")["amount"].sum().idxmax()
            
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Total Expenses", f"₹{total_amount:,.2f}")
            c2.metric("Total Transactions", total_count)
            c3.metric("Average Expense", f"₹{avg_amount:,.2f}")
            c4.metric("Top Category", top_category)
        else:
            st.info("💡 No expenses added yet. Click on the '➕ Add Expenses' card below to log your first expense!")
        
        st.markdown("---")
        st.subheader("📌 Key Features Direct Access Grid (Click Any Card Below)")

        # 100% INTERACTIVE CLICKABLE CARDS GRID
        grid_col1, grid_col2, grid_col3 = st.columns(3)
        
        with grid_col1:
            if st.button("💡 Save Money & Cut Expenses\n\nIdentify unnecessary spending & see where money can be saved.", key="card_save", use_container_width=True):
                set_page("💡 Save Money")
                st.rerun()

            if st.button("➕ Add Expenses\n\nLog new title, amount in ₹, category, date & payment method.", key="card_add", use_container_width=True):
                set_page("➕ Add Expenses")
                st.rerun()

            if st.button("📊 Category Report\n\nPercentage distribution of spending in ₹ per category.", key="card_cat", use_container_width=True):
                set_page("📊 Category Report")
                st.rerun()

        with grid_col2:
            if st.button("🔍 Search Expenses\n\nInstant keyword, category & payment method search.", key="card_search", use_container_width=True):
                set_page("🔍 Search Expenses")
                st.rerun()

            if st.button("✏️ Edit Expense\n\nModify details of any existing expense record in ₹.", key="card_edit", use_container_width=True):
                set_page("✏️ Edit Expense")
                st.rerun()

            if st.button("📅 Monthly Expenses\n\nMonth-by-month historical spend comparison in ₹.", key="card_monthly", use_container_width=True):
                set_page("📅 Monthly Expenses")
                st.rerun()

        with grid_col3:
            if st.button("📋 View Expenses\n\nFull interactive tabular transaction records in ₹.", key="card_view", use_container_width=True):
                set_page("📋 View Expenses")
                st.rerun()

            if st.button("🗑️ Delete Expense\n\nRemove expense records from database.", key="card_delete", use_container_width=True):
                set_page("🗑️ Delete Expense")
                st.rerun()

            if st.button("📈 Chart Analytics & 📥 Export\n\nVisual Plotly charts & CSV/JSON downloads in Rupees.", key="card_chart", use_container_width=True):
                set_page("📈 Chart Analytics")
                st.rerun()

        st.markdown("---")
        st.subheader("📋 Recent Transaction History (₹)")
        if not df.empty:
            display_df = df.copy()
            display_df["amount"] = display_df["amount"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(display_df.sort_values(by="date", ascending=False).head(5), use_container_width=True)
        else:
            st.write("No recent transactions. Added expenses will appear here.")

    # ================= PAGE 2: SAVE MONEY =================
    elif current_page == "💡 Save Money":
        st.subheader("💡 Save Money & Cut Unnecessary Expenses")
        st.write("Analyze your spending habits, detect unnecessary expenses, and discover exactly where money can be saved.")
        
        if not df.empty:
            non_essential_df = df[df["category"].isin(NON_ESSENTIAL_CATEGORIES)]
            total_non_essential = non_essential_df["amount"].sum()
            potential_savings_30 = total_non_essential * 0.30
            
            s_col1, s_col2, s_col3 = st.columns(3)
            s_col1.metric("Non-Essential Spending", f"₹{total_non_essential:,.2f}")
            s_col2.metric("Potential Monthly Savings (30% Cut)", f"₹{potential_savings_30:,.2f}")
            s_col3.metric("Total Saved from Eliminated Expenses", f"₹{st.session_state['eliminated_savings']:,.2f}")
            
            st.markdown("---")
            st.subheader("🎯 Where Money Can Be Saved (Smart Recommendations)")
            
            rec_col1, rec_col2 = st.columns(2)
            with rec_col1:
                dining_spend = df[df["category"] == "Food & Dining"]["amount"].sum()
                if dining_spend > 0:
                    st.markdown(f"""
                    <div class='savings-card'>
                        <div class='savings-title'>🍽️ Food & Dining Out Savings</div>
                        <div>You spent <b>₹{dining_spend:,.2f}</b> on dining out. Cooking at home 2 extra days per week can save you approx <b>₹{dining_spend * 0.4:,.2f}</b> monthly!</div>
                    </div>
                    """, unsafe_allow_html=True)

                shopping_spend = df[df["category"] == "Shopping"]["amount"].sum()
                if shopping_spend > 0:
                    st.markdown(f"""
                    <div class='savings-card'>
                        <div class='savings-title'>🛍️ Shopping & Impulse Buy Savings</div>
                        <div>You spent <b>₹{shopping_spend:,.2f}</b> on shopping. Applying a 48-hour wait rule before buying non-essentials can save <b>₹{shopping_spend * 0.35:,.2f}</b>!</div>
                    </div>
                    """, unsafe_allow_html=True)

            with rec_col2:
                ent_spend = df[df["category"] == "Entertainment"]["amount"].sum()
                if ent_spend > 0:
                    st.markdown(f"""
                    <div class='savings-card'>
                        <div class='savings-title'>🎬 Entertainment & Subscriptions</div>
                        <div>You spent <b>₹{ent_spend:,.2f}</b> on entertainment. Auditing unused streaming services can save you up to <b>₹{ent_spend * 0.5:,.2f}</b>.</div>
                    </div>
                    """, unsafe_allow_html=True)

                other_spend = df[df["category"] == "Other"]["amount"].sum()
                if other_spend > 0:
                    st.markdown(f"""
                    <div class='savings-card'>
                        <div class='savings-title'>📦 Miscellaneous Expenses</div>
                        <div>You spent <b>₹{other_spend:,.2f}</b> on unclassified items. Tracking small daily cash purchases saves up to <b>₹{other_spend * 0.25:,.2f}</b>.</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("✂️ Remove Unnecessary Expenses to Save Money")
            st.write("Select an optional / non-essential expense to eliminate it and save money:")
            
            if not non_essential_df.empty:
                save_options = {f"#{row['id']} - {row['title']} (₹{row['amount']:,.2f}) [{row['category']}]": row for _, row in non_essential_df.iterrows()}
                selected_save_label = st.selectbox("Select Unnecessary Expense to Remove & Save:", list(save_options.keys()))
                selected_save_item = save_options[selected_save_label]
                
                if st.button("💡 Eliminate Expense & Add to Money Saved!", key="btn_eliminate", type="primary"):
                    saved_amount = selected_save_item["amount"]
                    st.session_state["eliminated_savings"] += saved_amount
                    st.session_state["expenses"] = [exp for exp in st.session_state["expenses"] if exp["id"] != selected_save_item["id"]]
                    st.success(f"🎉 Expense '{selected_save_item['title']}' eliminated! You saved ₹{saved_amount:,.2f}!")
                    st.rerun()
            else:
                st.info("Great job! No non-essential expenses currently logged.")
        else:
            st.info("💡 Add your expenses first to receive personalized money-saving recommendations!")

    # ================= PAGE 3: ADD EXPENSES =================
    elif current_page == "➕ Add Expenses":
        st.subheader("➕ Add New Expense Entry (in ₹)")
        with st.form("add_expense_form_main"):
            col_a, col_b = st.columns(2)
            title = col_a.text_input("Expense Title", placeholder="e.g. Supermarket Groceries")
            amount = col_b.number_input("Amount (₹)", min_value=1.0, step=10.0)
            
            col_c, col_d, col_e = st.columns(3)
            category = col_c.selectbox("Category", ["Groceries", "Food & Dining", "Transportation", "Utilities & Bills", "Shopping", "Entertainment", "Health & Medical", "Other"])
            exp_date = col_d.date_input("Date", datetime.today())
            payment_method = col_e.selectbox("Payment Method", ["UPI / Online Transfer", "Credit Card", "Debit Card", "Cash"])
            
            notes = st.text_area("Notes (Optional)", placeholder="Add additional details...")
            
            submitted = st.form_submit_button("Save Expense Entry", use_container_width=True)
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
                    st.success(f"Added: {title} (₹{amount:,.2f})")
                    st.rerun()
                else:
                    st.error("Please enter an expense title.")

    # ================= PAGE 4: VIEW EXPENSES =================
    elif current_page == "📋 View Expenses":
        st.subheader("📋 View All Recorded Expenses (₹)")
        if not df.empty:
            view_df = df.copy()
            view_df["amount"] = view_df["amount"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(view_df, use_container_width=True)
        else:
            st.info("No expenses logged yet. Click '➕ Add Expenses' above to add your first expense.")

    # ================= PAGE 5: SEARCH EXPENSES =================
    elif current_page == "🔍 Search Expenses":
        st.subheader("🔍 Search & Filter Expenses")
        if not df.empty:
            col_s1, col_s2, col_s3 = st.columns(3)
            keyword = col_s1.text_input("Search Keyword", placeholder="Search title or notes...")
            category_filter = col_s2.selectbox("Category Filter", ["ALL"] + list(df["category"].unique()))
            payment_filter = col_s3.selectbox("Payment Method Filter", ["ALL"] + list(df["payment_method"].unique()))
            
            filtered_df = df.copy()
            if keyword:
                filtered_df = filtered_df[filtered_df["title"].str.contains(keyword, case=False, na=False) | filtered_df["notes"].str.contains(keyword, case=False, na=False)]
            if category_filter != "ALL":
                filtered_df = filtered_df[filtered_df["category"] == category_filter]
            if payment_filter != "ALL":
                filtered_df = filtered_df[filtered_df["payment_method"] == payment_filter]
                
            st.write(f"Showing {len(filtered_df)} matching results:")
            filtered_df["amount"] = filtered_df["amount"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No expenses available to search. Add an expense first.")

    # ================= PAGE 6: CATEGORY REPORT =================
    elif current_page == "📊 Category Report":
        st.subheader("📊 Category Report & Distribution (₹)")
        if not df.empty:
            cat_df = df.groupby("category")["amount"].agg(["sum", "count"]).reset_index()
            cat_df.columns = ["Category", "Total Spent (₹)", "Count"]
            total_sum = cat_df["Total Spent (₹)"].sum()
            cat_df["Percentage (%)"] = (cat_df["Total Spent (₹)"] / total_sum * 100).round(1)
            
            st.dataframe(cat_df.sort_values(by="Total Spent (₹)", ascending=False), use_container_width=True)
            
            fig = px.pie(cat_df, names="Category", values="Total Spent (₹)", title="Category Share (%)", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available yet. Add an expense first.")

    # ================= PAGE 7: EDIT EXPENSE =================
    elif current_page == "✏️ Edit Expense":
        st.subheader("✏️ Edit Existing Expense (₹)")
        if not df.empty:
            expense_options = {f"#{row['id']} - {row['title']} (₹{row['amount']:,.2f})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Choose Expense to Edit:", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            selected_item = next((item for item in st.session_state["expenses"] if item["id"] == selected_id), None)
            
            if selected_item:
                with st.form("edit_form_main"):
                    edit_title = st.text_input("Title", value=selected_item["title"])
                    edit_amount = st.number_input("Amount (₹)", value=float(selected_item["amount"]), step=10.0)
                    edit_category = st.selectbox("Category", ["Groceries", "Food & Dining", "Transportation", "Utilities & Bills", "Shopping", "Entertainment", "Health & Medical", "Other"], index=0)
                    edit_date = st.date_input("Date", datetime.strptime(selected_item["date"], "%Y-%m-%d"))
                    edit_payment = st.selectbox("Payment Method", ["UPI / Online Transfer", "Credit Card", "Debit Card", "Cash"], index=0)
                    edit_notes = st.text_area("Notes", value=selected_item.get("notes", ""))
                    
                    if st.form_submit_button("Update Expense Entry"):
                        selected_item["title"] = edit_title
                        selected_item["amount"] = edit_amount
                        selected_item["category"] = edit_category
                        selected_item["date"] = str(edit_date)
                        selected_item["payment_method"] = edit_payment
                        selected_item["notes"] = edit_notes
                        st.success("Expense updated successfully!")
                        st.rerun()
        else:
            st.info("No expenses available to edit.")

    # ================= PAGE 8: DELETE EXPENSE =================
    elif current_page == "🗑️ Delete Expense":
        st.subheader("🗑️ Delete Expense Entry")
        if not df.empty:
            expense_options = {f"#{row['id']} - {row['title']} (₹{row['amount']:,.2f})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Choose Expense to Delete:", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            if st.button("❌ Confirm Delete", key="btn_confirm_delete", type="primary"):
                st.session_state["expenses"] = [exp for exp in st.session_state["expenses"] if exp["id"] != selected_id]
                st.success("Expense deleted successfully!")
                st.rerun()
        else:
            st.info("No expenses available to delete.")

    # ================= PAGE 9: CHART ANALYTICS =================
    elif current_page == "📈 Chart Analytics":
        st.subheader("📈 Interactive Chart Analytics (₹)")
        if not df.empty:
            c_ch1, c_ch2 = st.columns(2)
            with c_ch1:
                fig_pie = px.pie(df, names="category", values="amount", title="Category Distribution in Rupees (₹)", hole=0.3)
                st.plotly_chart(fig_pie, use_container_width=True)
            with c_ch2:
                df["month"] = df["date"].str.slice(0, 7)
                monthly_df = df.groupby("month")["amount"].sum().reset_index()
                fig_bar = px.bar(monthly_df, x="month", y="amount", title="Monthly Spending Trend (₹)", labels={"amount": "Amount (₹)", "month": "Month"})
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No charts to display yet. Add an expense first.")

    # ================= PAGE 10: FINANCIAL REPORT =================
    elif current_page == "📑 Financial Report":
        st.subheader("📑 Financial Statement Report (₹)")
        if not df.empty:
            st.markdown(f"**Report Account:** `{st.session_state['user_email']}` | **Date:** `{datetime.now().strftime('%B %d, %Y')}`")
            summary_df = df.groupby("category").agg(
                Total_Amount_Rupees=("amount", "sum"),
                Transaction_Count=("amount", "count"),
                Average_Amount_Rupees=("amount", "mean")
            ).reset_index()
            summary_df["Total_Amount_Rupees"] = summary_df["Total_Amount_Rupees"].apply(lambda x: f"₹{x:,.2f}")
            summary_df["Average_Amount_Rupees"] = summary_df["Average_Amount_Rupees"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(summary_df, use_container_width=True)
        else:
            st.info("No financial report available. Add an expense first.")

    # ================= PAGE 11: MONTHLY EXPENSES =================
    elif current_page == "📅 Monthly Expenses":
        st.subheader("📅 Monthly Expenses Breakdown (₹)")
        if not df.empty:
            df["Month-Year"] = df["date"].str.slice(0, 7)
            month_df = df.groupby("Month-Year").agg(
                Total_Spent=("amount", "sum"),
                Item_Count=("amount", "count"),
                Average_Spend=("amount", "mean")
            ).reset_index().sort_values(by="Month-Year", ascending=False)
            
            month_df["Total_Spent"] = month_df["Total_Spent"].apply(lambda x: f"₹{x:,.2f}")
            month_df["Average_Spend"] = month_df["Average_Spend"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(month_df, use_container_width=True)
        else:
            st.info("No monthly expense records available yet.")

    # ================= PAGE 12: EXPORT SUMMARY =================
    elif current_page == "📥 Export Summary":
        st.subheader("📥 Export Summary Data (in ₹)")
        if not df.empty:
            csv_data = df.to_csv(index=False).encode('utf-8')
            json_data = json.dumps(st.session_state["expenses"], indent=2)
            
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                st.download_button(
                    label="📄 Download CSV File (₹)",
                    data=csv_data,
                    file_name=f"expense_summary_rupees_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with e_col2:
                st.download_button(
                    label="code Download JSON File (₹)",
                    data=json_data,
                    file_name=f"expense_summary_rupees_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("No expense data available to export. Add an expense first.")

# Main Application Entrypoint
if __name__ == "__main__":
    if not st.session_state["logged_in"]:
        render_login_page()
    else:
        render_home_dashboard()
