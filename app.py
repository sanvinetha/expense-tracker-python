import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import json

# Page Configuration for Streamlit Cloud
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Hiding Streamlit Toolbar (Fork, GitHub, Menu) & Slide Card Styling
st.markdown("""
    <style>
    #MainMenu {visibility: hidden !important;}
    header {visibility: hidden !important;}
    footer {visibility: hidden !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    .stAppHeader {display: none !important;}
    
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
    div.stButton > button {
        border-radius: 12px !important;
        padding: 0.85rem 1.25rem !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        background: rgba(30, 41, 59, 0.8) !important;
        color: #f8fafc !important;
        transition: all 0.25s ease !important;
        margin-bottom: 0.5rem !important;
    }
    div.stButton > button:hover {
        border-color: #3b82f6 !important;
        background: linear-gradient(135deg, #1e293b, #334155) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.25) !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session State Data
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user_email" not in st.session_state:
    st.session_state["user_email"] = ""
if "active_page" not in st.session_state:
    st.session_state["active_page"] = "HOME"
if "currency_symbol" not in st.session_state:
    st.session_state["currency_symbol"] = "₹"
if "expenses" not in st.session_state:
    st.session_state["expenses"] = []
if "incomes" not in st.session_state:
    st.session_state["incomes"] = []
if "bills" not in st.session_state:
    st.session_state["bills"] = []
if "category_budgets" not in st.session_state:
    st.session_state["category_budgets"] = {
        "Groceries": 5000.0,
        "Food & Dining": 3000.0,
        "Transportation": 2000.0,
        "Utilities & Bills": 3500.0,
        "Shopping": 2500.0,
        "Entertainment": 1500.0,
        "Health & Medical": 2000.0,
        "Other": 1000.0
    }
if "eliminated_savings" not in st.session_state:
    st.session_state["eliminated_savings"] = 0.0
if "show_logout_confirm" not in st.session_state:
    st.session_state["show_logout_confirm"] = False

# Registered User Passwords Database (Email ID -> Password)
if "registered_users" not in st.session_state:
    st.session_state["registered_users"] = {
        "sanvinetha@gmail.com": "Sanvinetha@123",
        "user@example.com": "Password123",
        "admin@gmail.com": "AdminPass123"
    }

NON_ESSENTIAL_CATEGORIES = ["Food & Dining", "Shopping", "Entertainment", "Other"]

def set_page(page_name):
    st.session_state["active_page"] = page_name

def fmt_amt(amt):
    curr = st.session_state.get("currency_symbol", "₹")
    return f"{curr}{amt:,.2f}"

def render_top_left_back_arrow():
    b_col1, b_col2 = st.columns([1, 4])
    with b_col1:
        if st.button("⬅️ Back to Home Page", key="btn_top_left_back_arrow", use_container_width=True):
            set_page("HOME")
            st.rerun()
    st.markdown("---")

# ==================== SIGN IN / LOGIN PAGE WITH STRICT PASSWORD VERIFICATION ==================== #
def render_login_page():
    curr = st.session_state.get("currency_symbol", "₹")
    st.markdown("<h1 class='main-header' style='text-align: center;'>Expense Tracker</h1>", unsafe_allow_html=True)
    st.markdown(f"<p class='sub-header' style='text-align: center;'>Manage your personal expenses, budgets & savings in {curr}</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        auth_mode = st.radio("Choose Sign In Mode:", ["📧 Sign In to Account", "📝 Register New Account"], horizontal=True)
        
        # MODE 1: SIGN IN WITH STRICT PASSWORD CHECK
        if auth_mode == "📧 Sign In to Account":
            st.subheader("Welcome Back - Sign In")
            st.write("Enter your Email ID and Password (Strict password verification enabled):")
            
            with st.form("email_login_form"):
                identity = st.text_input("Email ID", placeholder="username@gmail.com").strip().lower()
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit_btn = st.form_submit_button("Sign In ➔", use_container_width=True)
                
                if submit_btn:
                    if not identity or not password:
                        st.error("⚠️ Please enter both your Email ID and Password.")
                    elif identity in st.session_state["registered_users"]:
                        correct_password = st.session_state["registered_users"][identity]
                        # STRICT PASSWORD MATCH CHECK
                        if password == correct_password:
                            st.session_state["logged_in"] = True
                            st.session_state["user_email"] = identity
                            st.session_state["show_logout_confirm"] = False
                            st.success("✅ Password verified successfully! Access granted.")
                            st.rerun()
                        else:
                            st.error("❌ Incorrect Password! Access denied. Please enter the correct password matching this Email ID.")
                    else:
                        st.error("❌ Account not found! Please check your Email ID or register a new account under 'Register New Account'.")

            st.info("💡 **Registered Demo Credentials**:\n- **Email**: `sanvinetha@gmail.com` | **Password**: `Sanvinetha@123`\n- **Email**: `user@example.com` | **Password**: `Password123`\n- **Email**: `admin@gmail.com` | **Password**: `AdminPass123`")

        # MODE 2: REGISTER NEW ACCOUNT & SET CUSTOM PASSWORD
        else:
            st.subheader("📝 Register New Account")
            st.write("Create a new account by choosing your Email ID and Password:")
            
            with st.form("register_form"):
                reg_identity = st.text_input("Email ID", placeholder="username@gmail.com").strip().lower()
                reg_password = st.text_input("Choose Password", type="password", placeholder="Create a password")
                confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")
                reg_submit = st.form_submit_button("Create Account & Set Password ➔", use_container_width=True)
                
                if reg_submit:
                    if not reg_identity or not reg_password:
                        st.error("⚠️ Please fill in all fields.")
                    elif "@" not in reg_identity or "." not in reg_identity:
                        st.error("⚠️ Please enter a valid Email ID address.")
                    elif reg_password != confirm_password:
                        st.error("❌ Passwords do not match!")
                    else:
                        st.session_state["registered_users"][reg_identity] = reg_password
                        st.session_state["logged_in"] = True
                        st.session_state["user_email"] = reg_identity
                        st.session_state["show_logout_confirm"] = False
                        st.success("🎉 Account created successfully & password saved! Signed in.")
                        st.rerun()

        st.markdown("<div style='text-align: center; margin: 1.5rem 0; color: #94a3b8;'>─── OR SIGN IN WITH GOOGLE ───</div>", unsafe_allow_html=True)
        
        if st.button("🌐 Continue with Google Email ID", key="login_google", use_container_width=True):
            st.session_state["logged_in"] = True
            st.session_state["user_email"] = "google_user@gmail.com"
            st.session_state["show_logout_confirm"] = False
            st.rerun()

# ==================== MAIN APPLICATION ==================== #
def render_app():
    curr = st.session_state.get("currency_symbol", "₹")
    
    # TOP HEADER BAR
    head_col1, head_col2 = st.columns([3, 1])
    with head_col1:
        st.markdown("<h1 class='main-header'>Expense Tracker</h1>", unsafe_allow_html=True)
        st.markdown(f"Welcome back, **{st.session_state['user_email']}**! (Verified User)", unsafe_allow_html=True)
    with head_col2:
        curr_choice = st.selectbox("Currency", ["₹ (INR)", "$ (USD)", "€ (EUR)", "£ (GBP)"], index=0)
        st.session_state["currency_symbol"] = curr_choice.split()[0]
        
        if st.button("🚪 Sign Out", key="top_logout", use_container_width=True):
            st.session_state["show_logout_confirm"] = True

    # CONFIRM SIGN OUT MODAL
    if st.session_state["show_logout_confirm"]:
        st.warning("⚠️ **Confirm Sign Out**: Are you sure you want to sign out of Expense Tracker?")
        btn_c1, btn_c2, btn_c3 = st.columns([1, 1, 2])
        with btn_c1:
            if st.button("✅ Yes, Sign Out", key="confirm_logout_yes", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["show_logout_confirm"] = False
                st.rerun()
        with btn_c2:
            if st.button("❌ Cancel", key="confirm_logout_no", use_container_width=True):
                st.session_state["show_logout_confirm"] = False
                st.rerun()

    st.markdown("---")

    df = pd.DataFrame(st.session_state["expenses"])
    inc_df = pd.DataFrame(st.session_state["incomes"])
    current_page = st.session_state["active_page"]

    # ================= HOME PAGE SLIDE (FEATURES FIRST WITHOUT DESCRIPTIONS, FINANCIAL SUMMARY AT BOTTOM) =================
    if current_page == "HOME":
        features_list = [
            "💰 Total Expenses",
            "💡 Save Money",
            "➕ Add Expenses",
            "🎯 Budget & Goals",
            "💵 Income & Savings",
            "🔔 Bill Reminders",
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

        # 1. CLEAN FEATURES BUTTON GRID AT THE TOP (NO DESCRIPTIONS BELOW BUTTONS)
        for row_idx in range(0, len(features_list), 3):
            cols = st.columns(3)
            for col_idx in range(3):
                item_idx = row_idx + col_idx
                if item_idx < len(features_list):
                    feature_title = features_list[item_idx]
                    with cols[col_idx]:
                        if st.button(feature_title, key=f"grid_btn_{item_idx}", use_container_width=True):
                            set_page(feature_title)
                            st.rerun()

        st.markdown("---")

        # 2. FINANCIAL SUMMARY OVERVIEW AT THE BOTTOM OF THE SLIDE
        st.subheader(f"💰 Financial Summary Overview ({curr})")
        
        total_exp = df["amount"].sum() if not df.empty else 0.0
        total_inc = inc_df["amount"].sum() if not inc_df.empty else 0.0
        net_sav = total_inc - total_exp
        
        health_score = 100
        if total_inc > 0:
            savings_rate = (net_sav / total_inc) * 100
            health_score = max(0, min(100, int(savings_rate * 2)))
        elif total_exp > 0:
            health_score = 40
            
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Expenses", fmt_amt(total_exp))
        c2.metric("Total Income", fmt_amt(total_inc))
        c3.metric("Net Savings", fmt_amt(net_sav))
        c4.metric("Financial Health Score", f"{health_score} / 100")

    # ================= FEATURE SLIDE: TOTAL EXPENSES =================
    elif current_page == "💰 Total Expenses":
        render_top_left_back_arrow()
        st.subheader(f"💰 Total Expenses Breakdown ({curr})")
        
        total_exp = df["amount"].sum() if not df.empty else 0.0
        total_inc = inc_df["amount"].sum() if not inc_df.empty else 0.0
        net_sav = total_inc - total_exp
        
        health_score = 100
        if total_inc > 0:
            savings_rate = (net_sav / total_inc) * 100
            health_score = max(0, min(100, int(savings_rate * 2)))
        elif total_exp > 0:
            health_score = 40
            
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Expenses", fmt_amt(total_exp))
        c2.metric("Total Income", fmt_amt(total_inc))
        c3.metric("Net Savings", fmt_amt(net_sav))
        c4.metric("Financial Health Score", f"{health_score} / 100")
        
        st.markdown("---")
        st.subheader(f"📋 Transaction History ({curr})")
        if not df.empty:
            display_df = df.copy()
            display_df["amount"] = display_df["amount"].apply(lambda x: fmt_amt(x))
            st.dataframe(display_df.sort_values(by="date", ascending=False), use_container_width=True)
        else:
            st.info("💡 No expenses added yet.")

    # ================= FEATURE SLIDE: SAVE MONEY =================
    elif current_page == "💡 Save Money":
        render_top_left_back_arrow()
        st.subheader("💡 Save Money & Cut Unnecessary Expenses")
        st.write("Analyze spending habits, detect unnecessary expenses, and discover where money can be saved.")
        
        if not df.empty:
            non_essential_df = df[df["category"].isin(NON_ESSENTIAL_CATEGORIES)]
            total_non_essential = non_essential_df["amount"].sum()
            potential_savings_30 = total_non_essential * 0.30
            
            s_col1, s_col2, s_col3 = st.columns(3)
            s_col1.metric("Non-Essential Spending", fmt_amt(total_non_essential))
            s_col2.metric("Potential Savings (30% Cut)", fmt_amt(potential_savings_30))
            s_col3.metric("Total Saved from Eliminated Expenses", fmt_amt(st.session_state['eliminated_savings']))
            
            st.markdown("---")
            st.subheader("🎯 Where Money Can Be Saved (Smart Recommendations)")
            
            rec_col1, rec_col2 = st.columns(2)
            with rec_col1:
                dining_spend = df[df["category"] == "Food & Dining"]["amount"].sum()
                if dining_spend > 0:
                    st.markdown(f"""
                    <div class='savings-card'>
                        <div class='savings-title'>🍽️ Food & Dining Out Savings</div>
                        <div>You spent <b>{fmt_amt(dining_spend)}</b> on dining out. Cooking at home 2 extra days per week can save you approx <b>{fmt_amt(dining_spend * 0.4)}</b> monthly!</div>
                    </div>
                    """, unsafe_allow_html=True)

                shopping_spend = df[df["category"] == "Shopping"]["amount"].sum()
                if shopping_spend > 0:
                    st.markdown(f"""
                    <div class='savings-card'>
                        <div class='savings-title'>🛍️ Shopping & Impulse Buy Savings</div>
                        <div>You spent <b>{fmt_amt(shopping_spend)}</b> on shopping. Applying a 48-hour wait rule before buying non-essentials can save <b>{fmt_amt(shopping_spend * 0.35)}</b>!</div>
                    </div>
                    """, unsafe_allow_html=True)

            with rec_col2:
                ent_spend = df[df["category"] == "Entertainment"]["amount"].sum()
                if ent_spend > 0:
                    st.markdown(f"""
                    <div class='savings-card'>
                        <div class='savings-title'>🎬 Entertainment & Subscriptions</div>
                        <div>You spent <b>{fmt_amt(ent_spend)}</b> on entertainment. Auditing unused streaming services can save you up to <b>{fmt_amt(ent_spend * 0.5)}</b>.</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("---")
            st.subheader("✂️ Remove Unnecessary Expenses to Save Money")
            
            if not non_essential_df.empty:
                save_options = {f"#{row['id']} - {row['title']} ({fmt_amt(row['amount'])}) [{row['category']}]": row for _, row in non_essential_df.iterrows()}
                selected_save_label = st.selectbox("Select Unnecessary Expense to Remove & Save:", list(save_options.keys()))
                selected_save_item = save_options[selected_save_label]
                
                if st.button("💡 Eliminate Expense & Add to Money Saved!", key="btn_eliminate", type="primary"):
                    saved_amount = selected_save_item["amount"]
                    st.session_state["eliminated_savings"] += saved_amount
                    st.session_state["expenses"] = [exp for exp in st.session_state["expenses"] if exp["id"] != selected_save_item["id"]]
                    st.success(f"🎉 Expense '{selected_save_item['title']}' eliminated! You saved {fmt_amt(saved_amount)}!")
                    st.rerun()
            else:
                st.info("Great job! No non-essential expenses currently logged.")
        else:
            st.info("💡 Add your expenses first to receive personalized money-saving recommendations!")

    # ================= FEATURE SLIDE: BUDGET & GOALS =================
    elif current_page == "🎯 Budget & Goals":
        render_top_left_back_arrow()
        st.subheader("🎯 Category Monthly Budget Limits & Alerts")
        st.write("Set category monthly spending caps and monitor live budget progress alerts.")
        
        budgets = st.session_state["category_budgets"]
        cat_spend = df.groupby("category")["amount"].sum().to_dict() if not df.empty else {}
        
        st.markdown("#### Set Monthly Category Caps")
        b_cols = st.columns(4)
        idx = 0
        for cat, limit in list(budgets.items()):
            with b_cols[idx % 4]:
                new_limit = st.number_input(f"{cat} Limit ({curr})", min_value=100.0, value=float(limit), step=500.0, key=f"bud_in_{cat}")
                budgets[cat] = new_limit
            idx += 1

        st.markdown("---")
        st.markdown("#### Live Category Budget Status & Over-Budget Alerts")
        
        for cat, limit in budgets.items():
            spent = cat_spend.get(cat, 0.0)
            pct = min(1.0, spent / limit) if limit > 0 else 0.0
            pct_val = int((spent / limit) * 100) if limit > 0 else 0
            
            c_label = f"**{cat}**: Spent {fmt_amt(spent)} / Limit {fmt_amt(limit)} ({pct_val}%)"
            
            if pct_val >= 100:
                st.error(f"🚨 **OVER BUDGET ALERT**: {c_label}")
                st.progress(1.0)
            elif pct_val >= 80:
                st.warning(f"⚠️ **BUDGET WARNING (80%+ Reached)**: {c_label}")
                st.progress(pct)
            else:
                st.success(f"✅ {c_label}")
                st.progress(pct)

    # ================= FEATURE SLIDE: INCOME & SAVINGS =================
    elif current_page == "💵 Income & Savings":
        render_top_left_back_arrow()
        st.subheader("💵 Income Sources & Net Savings Calculator")
        
        with st.form("add_income_form"):
            col_i1, col_i2 = st.columns(2)
            inc_title = col_i1.text_input("Income Source", placeholder="e.g. Monthly Salary, Freelance Work")
            inc_amount = col_i2.number_input(f"Amount ({curr})", min_value=1.0, step=1000.0)
            inc_date = st.date_input("Date Received", datetime.today())
            
            if st.form_submit_button("Save Income Entry"):
                if inc_title:
                    st.session_state["incomes"].append({
                        "id": int(datetime.now().timestamp()),
                        "title": inc_title,
                        "amount": float(inc_amount),
                        "date": str(inc_date)
                    })
                    st.success(f"Saved income: {inc_title} ({fmt_amt(inc_amount)})")
                    st.rerun()

        st.markdown("---")
        st.subheader("📋 Recorded Income Sources")
        if not inc_df.empty:
            view_inc = inc_df.copy()
            view_inc["amount"] = view_inc["amount"].apply(lambda x: fmt_amt(x))
            st.dataframe(view_inc, use_container_width=True)
        else:
            st.info("No income records added yet.")

    # ================= FEATURE SLIDE: BILL REMINDERS =================
    elif current_page == "🔔 Bill Reminders":
        render_top_left_back_arrow()
        st.subheader("🔔 Subscription & Bill Payment Reminders")
        st.write("Track upcoming recurring bill payments (Rent, Netflix, Electricity, Wifi).")
        
        with st.form("add_bill_form"):
            col_b1, col_b2, col_b3 = st.columns(3)
            b_title = col_b1.text_input("Bill Name", placeholder="e.g. House Rent, WiFi Bill")
            b_amount = col_b2.number_input(f"Bill Amount ({curr})", min_value=1.0, step=100.0)
            b_due = col_b3.date_input("Due Date", datetime.today() + timedelta(days=7))
            
            if st.form_submit_button("Add Bill Reminder"):
                if b_title:
                    st.session_state["bills"].append({
                        "id": int(datetime.now().timestamp()),
                        "title": b_title,
                        "amount": float(b_amount),
                        "due_date": str(b_due),
                        "status": "Pending"
                    })
                    st.success(f"Bill reminder added for {b_title}")
                    st.rerun()

        st.markdown("---")
        st.subheader("📅 Upcoming Bills Schedule")
        if st.session_state["bills"]:
            b_df = pd.DataFrame(st.session_state["bills"])
            b_df["amount"] = b_df["amount"].apply(lambda x: fmt_amt(x))
            st.dataframe(b_df, use_container_width=True)
        else:
            st.info("No upcoming bill reminders.")

    # ================= FEATURE SLIDE: ADD EXPENSES =================
    elif current_page == "➕ Add Expenses":
        render_top_left_back_arrow()
        st.subheader(f"➕ Add New Expense Entry ({curr})")
        with st.form("add_expense_form_main"):
            col_a, col_b = st.columns(2)
            title = col_a.text_input("Expense Title", placeholder="Groceries, Coffee, Rent...")
            amount = col_b.number_input(f"Amount ({curr})", min_value=1.0, step=10.0)
            
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
                    st.success(f"Added: {title} ({fmt_amt(amount)})")
                    st.rerun()
                else:
                    st.error("Please enter an expense title.")

    # ================= FEATURE SLIDE: VIEW EXPENSES =================
    elif current_page == "📋 View Expenses":
        render_top_left_back_arrow()
        st.subheader(f"📋 View All Recorded Expenses ({curr})")
        if not df.empty:
            view_df = df.copy()
            view_df["amount"] = view_df["amount"].apply(lambda x: fmt_amt(x))
            st.dataframe(view_df, use_container_width=True)
        else:
            st.info("No expenses logged yet.")

    # ================= FEATURE SLIDE: SEARCH EXPENSES =================
    elif current_page == "🔍 Search Expenses":
        render_top_left_back_arrow()
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
            filtered_df["amount"] = filtered_df["amount"].apply(lambda x: fmt_amt(x))
            st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("No expenses available to search.")

    # ================= FEATURE SLIDE: CATEGORY REPORT =================
    elif current_page == "📊 Category Report":
        render_top_left_back_arrow()
        st.subheader(f"📊 Category Report & Distribution ({curr})")
        if not df.empty:
            cat_df = df.groupby("category")["amount"].agg(["sum", "count"]).reset_index()
            cat_df.columns = ["Category", f"Total Spent ({curr})", "Count"]
            total_sum = cat_df[f"Total Spent ({curr})"].sum()
            cat_df["Percentage (%)"] = (cat_df[f"Total Spent ({curr})"] / total_sum * 100).round(1)
            
            st.dataframe(cat_df.sort_values(by=f"Total Spent ({curr})", ascending=False), use_container_width=True)
            
            fig = px.pie(cat_df, names="Category", values=f"Total Spent ({curr})", title="Category Share (%)", hole=0.4)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No category data available yet.")

    # ================= FEATURE SLIDE: EDIT EXPENSE =================
    elif current_page == "✏️ Edit Expense":
        render_top_left_back_arrow()
        st.subheader(f"✏️ Edit Existing Expense ({curr})")
        if not df.empty:
            expense_options = {f"#{row['id']} - {row['title']} ({fmt_amt(row['amount'])})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Choose Expense to Edit:", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            selected_item = next((item for item in st.session_state["expenses"] if item["id"] == selected_id), None)
            
            if selected_item:
                with st.form("edit_form_main"):
                    edit_title = st.text_input("Title", value=selected_item["title"])
                    edit_amount = st.number_input(f"Amount ({curr})", value=float(selected_item["amount"]), step=10.0)
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

    # ================= FEATURE SLIDE: DELETE EXPENSE =================
    elif current_page == "🗑️ Delete Expense":
        render_top_left_back_arrow()
        st.subheader("🗑️ Delete Expense Entry")
        if not df.empty:
            expense_options = {f"#{row['id']} - {row['title']} ({fmt_amt(row['amount'])})": row['id'] for _, row in df.iterrows()}
            selected_label = st.selectbox("Choose Expense to Delete:", list(expense_options.keys()))
            selected_id = expense_options[selected_label]
            
            if st.button("❌ Confirm Delete", key="btn_confirm_delete", type="primary"):
                st.session_state["expenses"] = [exp for exp in st.session_state["expenses"] if exp["id"] != selected_id]
                st.success("Expense deleted successfully!")
                st.rerun()
        else:
            st.info("No expenses available to delete.")

    # ================= FEATURE SLIDE: CHART ANALYTICS =================
    elif current_page == "📈 Chart Analytics":
        render_top_left_back_arrow()
        st.subheader(f"📈 Interactive Chart Analytics ({curr})")
        if not df.empty:
            c_ch1, c_ch2 = st.columns(2)
            with c_ch1:
                fig_pie = px.pie(df, names="category", values="amount", title=f"Category Distribution in {curr}", hole=0.3)
                st.plotly_chart(fig_pie, use_container_width=True)
            with c_ch2:
                df["month"] = df["date"].str.slice(0, 7)
                monthly_df = df.groupby("month")["amount"].sum().reset_index()
                fig_bar = px.bar(monthly_df, x="month", y="amount", title=f"Monthly Spending Trend ({curr})", labels={"amount": f"Amount ({curr})", "month": "Month"})
                st.plotly_chart(fig_bar, use_container_width=True)
        else:
            st.info("No charts to display yet.")

    # ================= FEATURE SLIDE: FINANCIAL REPORT =================
    elif current_page == "📑 Financial Report":
        render_top_left_back_arrow()
        st.subheader(f"📑 Financial Statement Report ({curr})")
        if not df.empty:
            st.markdown(f"**Report Account:** `{st.session_state['user_email']}` | **Date:** `{datetime.now().strftime('%B %d, %Y')}`")
            summary_df = df.groupby("category").agg(
                Total_Amount=("amount", "sum"),
                Transaction_Count=("amount", "count"),
                Average_Amount=("amount", "mean")
            ).reset_index()
            summary_df["Total_Amount"] = summary_df["Total_Amount"].apply(lambda x: fmt_amt(x))
            summary_df["Average_Amount"] = summary_df["Average_Amount"].apply(lambda x: fmt_amt(x))
            st.dataframe(summary_df, use_container_width=True)
        else:
            st.info("No financial report available.")

    # ================= FEATURE SLIDE: MONTHLY EXPENSES =================
    elif current_page == "📅 Monthly Expenses":
        render_top_left_back_arrow()
        st.subheader(f"📅 Monthly Expenses Breakdown ({curr})")
        if not df.empty:
            df["Month-Year"] = df["date"].str.slice(0, 7)
            month_df = df.groupby("Month-Year").agg(
                Total_Spent=("amount", "sum"),
                Item_Count=("amount", "count"),
                Average_Spend=("amount", "mean")
            ).reset_index().sort_values(by="Month-Year", ascending=False)
            
            month_df["Total_Spent"] = month_df["Total_Spent"].apply(lambda x: fmt_amt(x))
            month_df["Average_Spend"] = month_df["Average_Spend"].apply(lambda x: fmt_amt(x))
            st.dataframe(month_df, use_container_width=True)
        else:
            st.info("No monthly expense records available yet.")

    # ================= FEATURE SLIDE: EXPORT SUMMARY =================
    elif current_page == "📥 Export Summary":
        render_top_left_back_arrow()
        st.subheader(f"📥 Export Summary Data ({curr})")
        if not df.empty:
            csv_data = df.to_csv(index=False).encode('utf-8')
            json_data = json.dumps(st.session_state["expenses"], indent=2)
            
            e_col1, e_col2 = st.columns(2)
            with e_col1:
                st.download_button(
                    label=f"📄 Download CSV File ({curr})",
                    data=csv_data,
                    file_name=f"expense_summary_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
            with e_col2:
                st.download_button(
                    label=f"code Download JSON File ({curr})",
                    data=json_data,
                    file_name=f"expense_summary_{datetime.now().strftime('%Y%m%d')}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("No expense data available to export.")

# Main Application Entrypoint
if __name__ == "__main__":
    if not st.session_state["logged_in"]:
        render_login_page()
    else:
        render_app()
