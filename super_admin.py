from unicodedata import name
import pandas as pd

import streamlit as st

from database import *

def super_admin_dashboard(user):
    with st.sidebar:
        st.markdown(f"""
        <div class='sidebar-brand'>
            <div style='font-weight:700; font-size:1.1rem;'>Gyan Pustak</div>
            <div style='font-size:0.8rem; opacity:0.7; margin-top:0.2rem;'>Super Admin</div>
        </div>
        """, unsafe_allow_html=True)
        fullname = f"{user['firstname']} {user['lastname']}"
        st.markdown(f"**{fullname}**")
        st.caption("Super Admin")
        st.markdown("---")

        pages = {
            " Dashboard": "home",
            " Employees": "employees",
            " Students": "students",
            " Books & Catalogue": "books",
            " Universities": "universities",
            " All Tickets": "tickets",
            " All Orders": "orders",
        }
        if "sa_page" not in st.session_state:
            st.session_state.sa_page = "home"

        for label, key in pages.items():
            if st.button(label, key=f"sa_nav_{key}", use_container_width=True):
                st.session_state.sa_page = key

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    page = st.session_state.sa_page
    if page == "home":
        _sa_home(user)
    elif page == "employees":
        _sa_employees(user)
    elif page == "students":
        _sa_students(user)
    elif page == "books":
        _sa_books(user)
    elif page == "universities":
        _sa_universities(user)
    elif page == "tickets":
        _sa_tickets(user)
    elif page == "orders":
        _sa_orders(user)


def _sa_home(user):
    st.title(" Super Admin Dashboard")

    stats = get_dashboard_stats()

    col1, col2, col3 = st.columns(3)
    col1.metric(" Books", stats["total_books"])
    col2.metric(" Students", stats["total_students"])
    col3.metric(" Employees", stats["total_employees"])

    col4, col5, col6 = st.columns(3)
    col4.metric(" Pending Orders", stats["pending_orders"])
    col5.metric(" Active Orders", stats["active_orders"])
    col6.metric(" Open Tickets", stats["open_tickets"])

    st.divider()

    col1, col2 = st.columns(2)

    # -------- TICKETS --------
    with col1:
        st.subheader(" Recent Tickets")

        tickets = get_all_tickets()

        for t in tickets[:5]:
            st.write(f"#{t['ticket_id']} - {t['title']}")
            st.caption(f"👤 {t.get('student_id','N/A')} | {t['date_logged']}")
            st.write(f"Status: {t['status']}")
            st.divider()

    # -------- ORDERS --------
    with col2:
        st.subheader(" Recent Orders")

        orders = get_all_orders()

        for o in orders[:5]:
            st.write(f"Order #{o['orders_id']}")
            st.caption(f"👤 {o['student_name']} ({o['email']})")
            st.write(f"📅 {o['date_created']}")
            st.write(f"Status: {o['order_status']}")

            # show books properly
            if o["books"]:
                books = o["books"].split(",")
                isbns = o["isbns"].split(",")

                for i in range(len(books)):
                    st.write(f"• {books[i]} (ISBN: {isbns[i]})")

            st.divider()


def _sa_employees(user):
    st.markdown("""<div class='page-header'><h1> Employee Management</h1>
    <p>Add and manage Customer Support and Administrator accounts</p></div>""", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["👥 All Employees", "➕ Add Employee"])

    # ── TAB 1: VIEW EMPLOYEES ──────────────────────────────
    with tab1:
        employees = get_employees()
        if not employees:
           st.info("No employees yet.")

        for emp in employees:
           role = " Customer Support" if emp["role"]=="customer_support" else " Administrator"

           st.markdown(f"""<div style='display:flex;justify-content:space-between;align-items:center;
                background:#F3E3D0;border-radius:10px;padding:8px 12px;margin:6px 0;'>
        <div style='width:25%;font-weight:600;color:#021A54;'>{emp['firstname']} {emp['lastname']}</div>
        <div style='width:30%;text-align:center;color:#021A54;'>{emp['email']}</div>
        <div style='width:25%;text-align:center;color:#021A54;'>{role}</div>
        <div style='width:20%;text-align:right;color:#021A54;'>ID: {emp['emp_id']}</div>
    </div>
    """, unsafe_allow_html=True)
            

    # ── TAB 2: ADD EMPLOYEE ──────────────────────────────
    with tab2:
        with st.form("add_emp",clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                 firstname = st.text_input("First Name *")
                 lastname = st.text_input("Last Name *")
                 email = st.text_input("Email *")
                 gender= st.selectbox("Gender *", ["Male", "Female", "Other"])
                 salary = st.number_input("Salary *", min_value=0)
                 aadhar= st.text_input("Aadhar Number *")
                 phoneno= st.text_input("Phone Number *")


            with col2:
                address = st.text_input("Address",placeholder="Enter city")
                role = st.selectbox(
                    "Role *",
                    ["customer_support", "administrator"],
                    format_func=lambda x: " Customer Support" if x == "customer_support" else " Administrator"
                )
                password = st.text_input("Password *", type="password")

            submitted = st.form_submit_button("➕ Create Employee", use_container_width=True)

        if submitted:
            if not all([firstname, lastname,gender,salary,aadhar, email,address,phoneno,role,password]):
                st.error("All fields are required.")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                ok, msg = create_employee(firstname, lastname,gender,salary,aadhar, email,address,phoneno,role,password)
                if ok:
                    st.success(f"✅ {msg}")
                    st.rerun()
                else:
                    st.error(msg)


def _sa_students(user):

    st.markdown("""<div class='page-header'><h1>🎓 Students</h1><p>View all registered students and their details</p></div>""", unsafe_allow_html=True)

    students = get_all_students()
    st.caption(f"{len(students)} students registered")

    if students:
        df = pd.DataFrame(students)[["firstname","lastname", "email", "university_name"]]
        df.columns = ["Firstname", "Lastname", "Email", "University"]
        df["Name"] = df["Firstname"] + " " + df["Lastname"]
        df=df[["Name", "Email", "University"]]
        #df["Joined"] = df["Joined"].str[:10]
        st.dataframe(df, use_container_width=True, hide_index=True)


def _sa_books(user):
    st.markdown("""<div class='page-header'><h1> Books & Catalogue</h1><p>Full library catalogue overview</p></div>""", unsafe_allow_html=True)

    books = get_all_books()
    categories = get_categories()
    courses = get_courses()

    tab1, tab2, tab3 = st.tabs([" Books", " Categories", " Courses"])

    with tab1:
        if books:
            df = pd.DataFrame(books)[["title", "isbn","quantity","options"]]
            df.columns = ["Title", "ISBN", "Quantity", "Option"]
            st.dataframe(df, use_container_width=True, hide_index=True)

    with tab2:
        cols = st.columns(4)
        for i, c in enumerate(categories):
            with cols[i % 4]:
                st.markdown(f"""<div style='background:#eff6ff; border-radius:8px; padding:0.6rem 1rem; margin-bottom:0.5rem; color:#1d4ed8; font-weight:500;'>🏷️ {c['category_name']}</div>""", unsafe_allow_html=True)

    with tab3:
       cols = st.columns(3)   # you can change to 4 if you want smaller boxes

       for i, c in enumerate(courses):
            with cols[i % 3]:
                st.markdown(f"""<div style='background:#f0fdf4;border-radius:10px;padding:0.8rem 1rem;margin-bottom:0.6rem;border:1px solid #bbf7d0;'>
                <div style='font-weight:600; font-size:1rem; color:#065f46;'>
                     {c['course_name']}
                </div>
                <div style='font-size:0.8rem; color:#6b7280; margin-top:2px;'>
                    Code: {c['course_id']}
                </div>
            </div>
            """, unsafe_allow_html=True)


def _sa_universities(user):
    st.markdown("""<div class='page-header'><h1> Universities & Departments</h1><p>Academic structure overview</p></div>""", unsafe_allow_html=True)

    universities = get_universities()
    for uni in universities:
        with st.expander(f" {uni['name']}"):
            depts = get_departments(uni["university_id"])
            if depts:
                for d in depts:
                    st.markdown(f"&nbsp;&nbsp;&nbsp;&nbsp;**{d['dept_name']}** Department")
            else:
                st.caption("No departments added yet.")


def _sa_tickets(user):
    st.markdown("""
    <div class='page-header'>
        <h1> All Tickets</h1>
        <p>System-wide ticket overview</p>
    </div>
    """, unsafe_allow_html=True)

    tickets = get_all_tickets()

    status_map = {
        "New": ("⚪", "#f3f4f6", "#374151"),
        "Assigned": ("🔵", "#dbeafe", "#1e40af"),
        "In-process": ("🟡", "#fef9c3", "#92400e"),
        "Completed": ("✅", "#d1fae5", "#065f46"),
    }

    filter_s = st.selectbox(
        "Filter by status",
        ["All", "New", "Assigned", "In-process", "Completed"]
    )

    if filter_s != "All":
        tickets = [t for t in tickets if t["status"] == filter_s]

    st.caption(f"{len(tickets)} tickets")

    for t in tickets:
        icon, bg, fg = status_map.get(t["status"], ("⚪", "#f3f4f6", "#374151"))

        with st.container():
        # Title + status
          col1, col2 = st.columns([4, 1])

          with col1:
            st.markdown(f"**#{t['ticket_id']} — {t['title']}**")

          with col2:
            st.markdown(
                f"<span style='background:{bg}; color:{fg}; padding:4px 8px; border-radius:10px; font-size:12px;'>"
                f"{icon} {t['status']}</span>",
                unsafe_allow_html=True
            )

        # Meta info
        st.caption(
            f"👤 {t.get('student_id','N/A')} |  {str(t['date_logged'])[:10]}"
        )

        if t.get("emp_id"):
            st.caption(f"🔧 Admin ID: {t['emp_id']}")

        # Description
        if t.get("problem_description"):
            desc = t["problem_description"]
            st.write(desc[:120] + ("..." if len(desc) > 120 else ""))

        # Solution
        if t.get("solution_description"):
            st.success(f"✔ Solution: {t['solution_description'][:100]}")

        st.divider()


def _sa_orders(user):
    st.title(" All Orders")

    orders = get_all_orders()

    if not orders:
        st.info("No orders found")
        return

    df = pd.DataFrame(orders)

    # -------- FILTER --------
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "new", "processed", "awaiting_shipping", "shipped", "canceled"]
    )

    if status_filter != "All":
        df = df[df["order_status"] == status_filter]

    # -------- FORMAT DATA --------
    df = df[[
        "orders_id",
        "student_name",
        "email",
        "books",
        "order_status",
        "date_created"
    ]]

    df.columns = [
        "Order ID",
        "Student",
        "Email",
        "Books",
        "Status",
        "Date"
    ]

    # format date
    df["Date"] = df["Date"].astype(str).str[:10]

    # format books (multi-line instead of comma)
    df["Books"] = df["Books"].apply(
        lambda x: "\n".join(x.split(",")) if x else ""
    )

    # -------- DISPLAY --------
    st.dataframe(df, use_container_width=True, hide_index=True)
