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

# Custom Styling for Home Screen Cards & Navigation
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
    .feature-card {
        background: rgba(30, 41, 59, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
        transition: transform 0.2s ease, border-color 0.2s ease;
        margin-bottom: 1rem;
    }
    .feature-card:hover {
        border-color: #3b82f6;
        transform: translateY(-3px);
    }
    .feature-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
    }
    .feature-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 0.25rem;
    }
    .feature-desc {
        font-size: 0.825rem;
        color: #94a3b8;
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
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 14px;
        font-weight: 600;
        background-color: rgba(30, 41, 59, 0.5);
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #3b82f6, #6366f1) !important;
        color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Data
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []
if "eliminated_savings" not in st.session_state:
    st.session_state["eliminated_savings"] = 0.0

# Non-essential categories that can be optimized
NON_ESSENTIAL_CATEGORIES = ["Food & Dining", "Shopping", "Entertainment", "Other"]

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
        
        if st.button("🌐 Continue with Google Email ID", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = "google_user@gmail.com"
            st.success("Signed in with Google Email ID!")
            st.rerun()
            
        if st.button("🚀 Quick Demo Guest Login", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = "guest_user@example.com"
            st.rerun()

# ==================== MAIN HOME SCREEN ==================== #
def render_home_dashboard():
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown("<h1 class='main-header'>Expense Tracker</h1>", unsafe_allow_html=True)
        st.markdown(f"Welcome back, **{st.session_state['user_email']}**! Track expenses & save money in Rupees (₹).", unsafe_allow_html=True)
    with head_col2:
        st.write("")
        if st.button("🚪 Sign Out", use_container_width=True):
            st.session_state["logged_in"] = False
            st.rerun()

    st.markdown("---")

    # ALL FEATURE OPTIONS ON TOP HOME TABS INCLUDING NEW "💡 SAVE MONEY" FEATURE
    tabs = st.tabs([
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
    ])

    df = pd.DataFrame(st.session_state["expenses"])

    # TAB 1: TOTAL EXPENSES
    with tabs[0]:
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
            st.info("💡 No expenses added yet. Click on the '➕ Add Expenses' tab to log your first expense!")
        
        st.markdown("---")
        st.subheader("📌 Key Features Direct Access Grid")

        f_col1, f_col2, f_col3 = st.columns(3)
        with f_col1:
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>💡</div>
                <div class='feature-title'>Save Money & Cut Expenses</div>
                <div class='feature-desc'>Identify unnecessary spending & see where money can be saved.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>➕</div>
                <div class='feature-title'>Add Expenses</div>
                <div class='feature-desc'>Log new title, amount in ₹, category, date & payment method.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>📊</div>
                <div class='feature-title'>Category Report</div>
                <div class='feature-desc'>Percentage distribution of spending in ₹ per category.</div>
            </div>
            """, unsafe_allow_html=True)

        with f_col2:
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>🔍</div>
                <div class='feature-title'>Search Expenses</div>
                <div class='feature-desc'>Instant keyword, category & payment method search.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>✏️</div>
                <div class='feature-title'>Edit Expense</div>
                <div class='feature-desc'>Modify details of any existing expense record in ₹.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>📅</div>
                <div class='feature-title'>Monthly Expenses</div>
                <div class='feature-desc'>Month-by-month historical spend comparison in ₹.</div>
            </div>
            """, unsafe_allow_html=True)

        with f_col3:
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>📋</div>
                <div class='feature-title'>View Expenses</div>
                <div class='feature-desc'>Full interactive tabular transaction records in ₹.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>🗑️</div>
                <div class='feature-title'>Delete Expense</div>
                <div class='feature-desc'>Remove expense records from database.</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("""
            <div class='feature-card'>
                <div class='feature-icon'>📈</div>
                <div class='feature-title'>Chart Analytics & 📥 Export</div>
                <div class='feature-desc'>Visual Plotly charts & CSV/JSON downloads in Rupees.</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("📋 Recent Transaction History (₹)")
        if not df.empty:
            display_df = df.copy()
            display_df["amount"] = display_df["amount"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(display_df.sort_values(by="date", ascending=False).head(5), use_container_width=True)
        else:
            st.write("No recent transactions. Added expenses will appear here.")

    # NEW TAB 2: SAVE MONEY & CUT UNNECESSARY EXPENSES
    with tabs[1]:
        st.subheader("💡 Save Money & Cut Unnecessary Expenses")
        st.write("Analyze your spending habits, detect unnecessary expenses, and discover exactly where money can be saved.")
        
        if not df.empty:
            non_essential_df = df[df["category"].isin(NON_ESSENTIAL_CATEGORIES)]
            total_non_essential = non_essential_df["amount"].sum()
            total_spending = df["amount"].sum()
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
                
                if st.button("💡 Eliminate Expense & Add to Money Saved!", type="primary"):
                    saved_amount = selected_save_item["amount"]
                    st.session_state["eliminated_savings"] += saved_amount
                    st.session_state["expenses"] = [exp for exp in st.session_state["expenses"] if exp["id"] != selected_save_item["id"]]
                    st.success(f"🎉 Expense '{selected_save_item['title']}' eliminated! You saved ₹{saved_amount:,.2f}!")
                    st.rerun()
            else:
                st.info("Great job! No non-essential expenses currently logged.")
        else:
            st.info("💡 Add your expenses first to receive personalized money-saving recommendations!")

    # TAB 3: ADD EXPENSES
    with tabs[2]:
        st.subheader("➕ Add New Expense Entry (in ₹)")
        with st.form("add_expense_form_home"):
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

    # TAB 4: VIEW EXPENSES
    with tabs[3]:
        st.subheader("📋 View All Recorded Expenses (₹)")
        if not df.empty:
            view_df = df.copy()
            view_df["amount"] = view_df["amount"].apply(lambda x: f"₹{x:,.2f}")
            st.dataframe(view_df, use_container_width=True)
        else:
            st.info("No expenses logged yet. Add your first expense using the '➕ Add Expenses' tab.")

    # TAB 5: SEARCH EXPENSES
    with tabs[4]:
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

    # TAB 6: CATEGORY REPORT
    with tabs[5]:
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

    # TAB 7: EDIT EXPENSE
    with tabs[6]:
        st.subheader("✏️ Edit Existing Expense (₹)")
        if not df.empty:
            expense_options = {f"#{row['id']} - {row['title']} (₹{row['amount']:,.2f})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Choose Expense to Edit:", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            selected_item = next((item for item in st.session_state["expenses"] if item["id"] == selected_id), None)
            
            if selected_item:
                with st.form("edit_form_home"):
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

    # TAB 8: DELETE EXPENSE
    with tabs[7]:
        st.subheader("🗑️ Delete Expense Entry")
        if not df.empty:
            expense_options = {f"#{row['id']} - {row['title']} (₹{row['amount']:,.2f})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Choose Expense to Delete:", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            if st.button("❌ Confirm Delete", type="primary"):
                st.session_state["expenses"] = [exp for exp in st.session_state["expenses"] if exp["id"] != selected_id]
                st.success("Expense deleted successfully!")
                st.rerun()
        else:
            st.info("No expenses available to delete.")

    # TAB 9: CHART ANALYTICS
    with tabs[8]:
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

    # TAB 10: FINANCIAL REPORT
    with tabs[9]:
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

    # TAB 11: MONTHLY EXPENSES
    with tabs[10]:
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

    # TAB 12: EXPORT SUMMARY
    with tabs[11]:
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
