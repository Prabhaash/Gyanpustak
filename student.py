import streamlit as st
from database import *
from collections import defaultdict

STATUS_COLORS = {
    "New": ("🟡", "badge-new", "New"),
    "Assigned": ("🔵", "badge-assigned", "Assigned"),
    "In-process": ("🟠", "badge-process", "In Process"),
    "Completed": ("✅", "badge-done", "Completed"),
}

def student_dashboard(user):

    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        st.markdown("""
        <div class='sidebar-brand'>
            <div style='font-weight:700; font-size:1.1rem;'>Gyan Pustak</div>
            <div style='font-size:0.8rem;'>Student Portal</div>
        </div>
        """, unsafe_allow_html=True)

        fullname = user['firstname'] + " " + user['lastname']
        st.markdown(f"**{fullname}**")
        st.caption("Student")

        st.markdown("---")

        pages = {
            " Home": "home",
            " Books": "books",
            " Cart": "cart",
            " My Orders": "orders",
            " Raise Ticket": "new_ticket",
            " Ticket History": "ticket_history",
            " My Profile": "profile",
        }

        if "student_page" not in st.session_state:
            st.session_state.student_page = "home"

        for label, key in pages.items():
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.student_page = key

        st.markdown("---")

        if st.button(" Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    # ---------------- CORE LOGIC ----------------
    student_id = get_student_id(user['email'])

    # FIXED CART LOGIC (NO DUPLICATES)
    cart_id = get_cart_id(student_id)
    if not cart_id:
        cart_id = get_cart_entry(student_id)

    # Navigation fix
    page = st.session_state.student_page

    if page == "home":
        _home(user)
    elif page == "books":
        _books(user)
    elif page == "cart":
        _cart(user)
    elif page == "orders":
        _orders(user)
    elif page == "new_ticket":
        _new_ticket(user)
    elif page == "ticket_history":
        _ticket_history(user)
    elif page == "profile":
        _profile(user)


# ================= HOME =================
def _home(user):
    student_id = get_student_id(user['email'])
    profile = get_student_profile(student_id)

    fullname = profile['firstname'] + " " + profile['lastname']

    st.markdown(f"""
    <div class='page-header'>
        <h1>Hello, {fullname}! </h1>
        <p>Welcome to Gyan Pustak</p>
    </div>
    """, unsafe_allow_html=True)

    orders = get_orders(student_id)
    tickets = get_tickets_by_student(student_id)

    # correct cart usage
    cart_id = get_cart_id(student_id)
    cart_items = get_cart_of_student(cart_id)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        active_orders = len([o for o in orders if o['order_status'] != 'canceled'])
        st.metric("Active Orders", active_orders)

    with c2:
        st.metric("Cart Items", len(cart_items))

    with c3:
        open_t = len([t for t in tickets if t["status"] != "Completed"])
        st.metric("Open Tickets", open_t)

    with c4:
        st.metric("Total Orders", len(orders))

    st.markdown("---")

    col1, col2 = st.columns(2)

    # -------- BOOKS --------
    with col1:
        st.markdown("#### Your Course Books")

        if profile and profile.get("course_id"):
            books = get_books_by_course(profile["course_id"])

            if books:
                for b in books[:4]:
                    st.markdown(f"""
                    <div class='book-card'>
                        <b>{b['title']}</b><br>
                        <small>{b.get('author','Unknown')}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No books found")
        else:
            st.info("Update profile")

    # -------- TICKETS --------
    with col2:
        st.markdown("####  Recent Tickets")

        if tickets:
            for t in tickets[:3]:
                icon, _, label = STATUS_COLORS.get(t["status"], ("⚪", "", t["status"]))

                st.markdown(f"""
                <div class='ticket-card'>
                    <b>{t['title']}</b>
                    <span style='float:right;'>{icon} {label}</span>
                    <br><small>{t['date_logged']}</small>
                    {f"<br><small><b>Solution:</b> {t['solution_description']}</small>" if t.get('solution_description') else ''}
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No tickets yet")


@st.cache_data
def get_books_cached(search, category_id):
    return get_books_by_category(search, category_id)


@st.cache_data
def get_cart_cached(cart_id):
    return get_cart_of_student(cart_id)


def _books(user):
    st.title(" Browse Books")
    st.caption("Search, borrow, and rate books")

    student_id = get_student_id(user['email'])

    # ---------- SESSION INIT ----------
    if "rate_book" not in st.session_state:
        st.session_state.rate_book = None

    # ---------- FILTERS ----------
    categories = get_categories()
    cat_options = {"All Categories": None}
    cat_options.update({c["category_name"]: c["category_id"] for c in categories})

    col1, col2 = st.columns([3, 1])
    with col1:
        search = st.text_input(" Search books")
    with col2:
        cat_sel = st.selectbox("Category", list(cat_options.keys()))

    # ---------- FETCH ----------
    books = get_books_cached(search, cat_options[cat_sel])
    books = books[:12]  # limit for speed

    st.caption(f"Showing {len(books)} books")

    # ---------- CART ----------
    cart_id = get_cart_id(student_id)
    cart = get_cart_cached(cart_id) if cart_id else []
    in_cart_ids = {item["isbn"] for item in cart}

    # ---------- GRID ----------
    cols = st.columns(3)

    for i, book in enumerate(books):
        with cols[i % 3]:

            # ---- BOOK CARD ----
            st.markdown(f"### {book['title']}")
            st.caption(f"⭐ {book.get('avg_rating', 0)} / 5")

            if book.get("description"):
                st.caption(book["description"][:80] + "...")

            # Availability
            if book["quantity"] > 0:
                st.success("Available")
            else:
                st.error("Out of stock")

            # ---------- CART BUTTON ----------
            if book["isbn"] in in_cart_ids:
                st.button("✓ In Cart", key=f"incart_{book['isbn']}", disabled=True)

            elif book["quantity"] <= 0:
                st.button("Out of Stock", key=f"oos_{book['isbn']}", disabled=True)

            else:
                if st.button(" Add to Cart", key=f"add_{book['isbn']}"):
                    ok, msg = add_to_cart(student_id, book["isbn"])
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.warning(msg)

            # ---------- RATE BUTTON ----------
            if st.button("Review", key=f"rate_btn_{book['isbn']}"):
                st.session_state.rate_book = book["isbn"]

            # ---------- RATING UI ----------
            if st.session_state.rate_book == book["isbn"]:

                rating = st.selectbox(
                    "Rating",
                    [1, 2, 3, 4, 5],
                    key=f"rating_{book['isbn']}"
                )

                review = st.text_input(
                    "Write review",
                    key=f"review_{book['isbn']}"
                )

                col_r1, col_r2 = st.columns(2)

                with col_r1:
                    if st.button("Submit", key=f"submit_{book['isbn']}"):
                        ok, msg = add_review(student_id, book["isbn"], rating, review)
                        if ok:
                            st.success("Review added")
                            st.session_state.rate_book = None
                            st.rerun()
                        else:
                            st.error(msg)

                with col_r2:
                    if st.button("Cancel", key=f"cancel_{book['isbn']}"):
                        st.session_state.rate_book = None
                        st.rerun()

            st.markdown("---")

def _cart(user):
    st.markdown("""
    <div class='page-header'>
        <h1> My Cart</h1>
        <p>Review and place your order request</p>
    </div>
    """, unsafe_allow_html=True)

    student_id = get_student_id(user['email'])

    cart_id = get_cart_id(student_id)
    
    if not cart_id:
        st.info("Your cart is empty.")
        return
   
    cart = get_cart_of_student(cart_id)
    if not cart:
        st.info("Your cart is empty. Browse books to add some!")
        return

    # ---------------- ITEMS ----------------
    for item in cart:
        col1, col2 = st.columns([5, 1])

        with col1:
            st.markdown(f"""
            <div class='card'>
                <b>{item['title']}</b>
                <br><small>ISBN: {item['isbn']}</small>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)

            # FIX remove key
            if st.button(" Remove", key=f"rem_{item['isbn']}"):
                remove_from_cart(cart_id, item["isbn"])
                st.rerun()

    # ---------------- SUMMARY ----------------
    st.markdown(f"**{len(cart)} item(s)** ")
    with st.form("login_form",clear_on_submit=True):
        shipping_type= st.selectbox("Shipping Type", ["standard", "2-day", "1-day"])
        credit_card_number = st.text_input("Credit Card Number", placeholder="1234 5678 9012 3456")
        expiry_date = st.text_input("Expiry Date", placeholder="MM/YY")
        cvv = st.text_input("CVV", type="password", placeholder="•••")
        Holder_name = st.text_input("Card Holder Name", placeholder="Apashyam kirkiri")
        submitted = st.form_submit_button("✅ Place order", use_container_width=True)
        
        if submitted:
          if not shipping_type or not credit_card_number or not expiry_date or not Holder_name:
              st.error("Please fill in all fields")
              return
          ok, msg = checkout_cart(
                     student_id,
                    shipping_type,
                    credit_card_number,
                    expiry_date,
                    Holder_name)

          if ok:
             st.success(msg)
             st.rerun()
          else:
            st.error(msg)



from collections import defaultdict

def _orders(user):
    st.title(" My Orders")
    st.caption("Track your borrowed books")

    rows = get_orders_by_student(user["student_id"])

    if not rows:
        st.info("No orders yet. Browse books and place a request!")
        return

    orders = defaultdict(list)
    for r in rows:
        orders[r["orders_id"]].append(r)

    status_map = {
        "new": ("🟡", "warning"),
        "processed": ("🔵", "info"),
        "awaiting shipping": ("🟠", "warning"),
        "shipped": ("🟢", "success"),
        "canceled": ("🔴", "error")
    }

    for order_id, items in orders.items():
        info = items[0]
        status = info["order_status"]

        icon, style = status_map.get(status, ("⚪", "secondary"))

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:
                st.subheader(f"Order #{order_id}")
                st.caption(f"Date: {info['date_created']}")

            with col2:
                st.markdown(f"### {icon} {status.capitalize()}")

            st.divider()

            # -------- BOOKS --------
            for item in items:
                st.write(f"• **{item['title']}** (ISBN: {item['isbn']})")

            # -------- CANCEL BUTTON --------
            if status not in [ "shipped","cancelled"]:
                if st.button("❌ Cancel Request", key=f"cancel_{order_id}"):
                    ok, msg = request_cancel_order(order_id, user["student_id"])
                    if ok:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)

def _new_ticket(user):
    st.markdown("""<div class='page-header'><h1> Raise a Ticket</h1><p>Submit a complaint or inquiry to our support team</p></div>""", unsafe_allow_html=True)

    with st.form("ticket_form"):
        subject = st.text_input("Subject *", placeholder="e.g. Book not available, Wrong order...")
        description = st.text_area("Describe your issue *", height=150,
                                   placeholder="Please provide as much detail as possible...")
        submitted = st.form_submit_button("Submit Ticket", use_container_width=True)

    if submitted:
        if not subject or not description:
            st.error("Please fill in both subject and description.")
        else:
            create_ticket_st(user["student_id"], subject, description)
            st.success("✅ Ticket submitted! Our support team will review it shortly.")


def _ticket_history(user):
    st.markdown("""<div class='page-header'><h1>Ticket History</h1><p>Track your complaints and support requests</p></div>""", unsafe_allow_html=True)

    tickets = get_tickets_by_student(user["student_id"])
    if not tickets:
        st.info("You haven't raised any tickets yet.")
        return

    for t in tickets:
        icon, badge, label = STATUS_COLORS.get(t["status"], ("⚪", "", t["status"]))
        st.markdown(f"""<div class='card'>
            <div style='display:flex; justify-content:space-between; align-items:flex-start;'>
                <div style='flex:1;'>
                    <b style='font-size:1rem;'>{t['title']}</b>
                    <span class='badge {badge}' style='margin-left:0.7rem;'>{icon} {label}</span>
                    <br><small style='color:#6b7280;'>Submitted: {t['date_logged']}</small>
                    <br><span style='color:#4b5563; font-size:0.9rem; display:block; margin-top:0.4rem;'>{t['problem_description']}</span>
                    {f"<div style='margin-top:0.7rem; padding:0.7rem; background:#f0fdf4; border-left:3px solid #16a34a; border-radius:4px;'><b style='color:#15803d;'>Support Reply:</b><br>{t['solution_description']}</div>" if t.get('solution_description') else '<div style=\"margin-top:0.4rem; color:#6b7280; font-size:0.85rem;\">⏳ Awaiting response...</div>'}
                </div>
            </div>
        </div>""", unsafe_allow_html=True)


def _profile(user):
    st.markdown("""<div class='page-header'><h1> My Profile</h1><p>Your academic details and account information</p></div>""", unsafe_allow_html=True)

    profile = get_student_profile(user["student_id"])
    if not profile:
        st.error("Could not load profile.")
        return

    col1, col2 = st.columns(2)
    with col1:
        fullname = profile['firstname'] + " " + profile['lastname']
        st.markdown("""<div class='card'>""", unsafe_allow_html=True)
        st.markdown("#### Personal Information")
        st.markdown(f"**Name:** {fullname}")
        st.markdown(f"**Email:** {profile['email']}")
        st.markdown(f"**Account Type:** Student")
        st.markdown(f"**Status:** {profile['status'].capitalize()}")
        st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""<div class='card'>""", unsafe_allow_html=True)
        st.markdown("####  Academic Information")
        st.markdown(f"**University:** {profile.get('university_name') or 'Not set'}")
        st.markdown(f"**Department:** {profile.get('department_name') or 'Not Set'}")
        st.markdown("</div>", unsafe_allow_html=True)

    if profile.get("course_id"):
        st.markdown("#### Recommended Books for Your Course")
        from database import get_books_by_course
        books = get_books_by_course(profile["course_id"])
        if books:
            cols = st.columns(3)
            for i, b in enumerate(books):
                with cols[i % 3]:
                    st.markdown(f"""<div class='book-card'>
                        <div class='book-title'>{b['title']}</div>
                        <div class='book-author'>by {b['author']}</div>
                        <span class='book-cat'>{b['category_name']}</span>
                    </div>""", unsafe_allow_html=True)
        else:
            st.info("No books linked to your course.")
