from datetime import date

import streamlit as st

from database import *

def login_page():
    # Two column layout (image + form)
    col1, col2 = st.columns([1.2, 1])

    # -------- LEFT SIDE (IMAGE) --------
    with col1:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.image("home.jpg", width=600)

    # -------- RIGHT SIDE (LOGIN UI) --------
    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 1rem 0 1rem;'>
            <h1 style='font-size:2rem; margin:0.2rem 0; color:#2FA4D7;'>Gyan Pustak</h1>
            <p style='color:#6b7280; font-size:0.9rem;'>Sabka Library Portal</p>
        </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs([" Sign In", " Sign Up"])

        with tab1:
            _login_form()

        with tab2:
            _register_form()

def _login_form():
    st.markdown("### Welcome back")
    st.caption("Sign in as Student, Employee, or Super Admin")

    with st.form("login_form"):
        role_label = st.selectbox("Login as", ["Student", "Employee", "Super Admin"])
        email = st.text_input("Email", placeholder="you@gmail.com")
        password = st.text_input("Password", type="password", placeholder="••••••••")
        submitted = st.form_submit_button("Sign In", use_container_width=True)

    role_map = {
        "Student": "student",
        "Employee": ["customer_support", "administrator"],
        "Super Admin": "super_admin"
    }

    if submitted:
        if not email or not password:
            st.error("Please fill in all fields.")
            return
        if role_label == "Employee" or role_label == "Super Admin":
            #st.warning("For Employee login, please select the appropriate role based on your account type.")
            user=get_employee_by_email(email)
        elif role_label == "Student":
            user=get_student_by_email(email)
        
        if not user:
            st.error("No account found with this email.")
            return
        if user["password"] != password:
            st.error("Incorrect password.")
            return

        expected = role_map[role_label]
        if role_label == "Employee":
             if user["role"] not in expected:
                st.error(f"This account is not an Employee account.")
                return
        elif role_label == "Super Admin":
                if user["role"] not in expected:
                    st.error(f"This account is not a Super Admin account.")
                    return  
        else:             
            if role_label != "Student" and user["role"] != expected:
                st.error(f"Please select the correct role for this account.")
                return
        
        st.session_state.user = user
        fullname=user["firstname"] + " " + user["lastname"]
        st.success(f"Welcome, {fullname}!")
        st.rerun()

    # Demo credentials
    with st.expander(" Demo Credentials"):
        st.markdown("""
        | Role | Email | Password |
        |---|---|---|
        | Student | rahul@gmail.com | pass123 |
        | Customer Support | ravi@gmail.com | support123 |
        | Administrator | neha@gmail.com | admin123 |
        | Super Admin | lokesh@gmail.com | super123 |
        """)

def _register_form():
    st.markdown("### Create Student Account")
    universities = get_universities()
    departments=get_departments()

    uni_options = {u["name"]: u["university_id"] for u in universities}
    dept_options={d["dept_name"]: d["dept_id"] for d in departments}
    #course_options = {f"{c['code']} – {c['name']}": c["course_id"] for c in courses}

    with st.form("register_form",clear_on_submit=True):
        firstname = st.text_input("First Name", placeholder="Your first name")
        lastname = st.text_input("Last Name", placeholder="Your last name")
        address = st.text_input("Address", placeholder="Your city")
        email = st.text_input("Email", placeholder="you@university.edu")
        phoneno = st.text_input("Phone Number", placeholder="+91-XXXXXXXXXX 10 digit number")
        dateofbirth = st.date_input("Date of Birth",min_value="1980-01-01", max_value=date.today())
        university = st.selectbox("University", list(uni_options.keys()))
        department = st.selectbox("Department", list(dept_options.keys()))
        status=st.selectbox("Status", ["undergraduate", "graduate"])
        curyear=st.number_input("Current Year of Study", min_value=1, max_value=4, step=1)
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Create Account", use_container_width=True)

    if submitted:
        if not all([firstname, lastname,address, email,phoneno, dateofbirth, university, department, status, curyear, password, confirm]):
            st.error("Please fill all fields.")
        elif password != confirm:
            st.error("Passwords do not match.")
        elif len(password) < 6:
            st.error("Password must be at least 6 characters.")
        else:
            ok, msg = register_student(
                firstname, lastname, address, email, phoneno, dateofbirth,
                uni_options[university], dept_options[department], status, curyear, password
            )
            if ok:
                st.success(msg)
            else:
                st.error(msg)
