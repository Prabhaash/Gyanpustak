import streamlit as st
import pandas as pd
from database import *

def administrator_dashboard(user):
    with st.sidebar:
        st.markdown(f"""
        <div class='sidebar-brand'>
            <div style='font-weight:700; font-size:1.1rem;'>Gyaan Pustak</div>
            <div style='font-size:0.8rem; opacity:0.7; margin-top:0.2rem;'>Administrator</div>
        </div>
        """, unsafe_allow_html=True)
        fullname=user['firstname'] + " " + user['lastname']
        st.markdown(f"**{fullname}**")
        st.caption("Library Administrator")
        st.markdown("---")

        pages = {
            " Dashboard": "home",
            " My Tickets": "my_tickets",
            " Orders": "orders",
            " Manage Books": "books",
        }

        if "admin_page" not in st.session_state:
            st.session_state.admin_page = "home"

        for label, key in pages.items():
            if st.button(label, key=f"adm_nav_{key}", use_container_width=True):
                st.session_state.admin_page = key

        st.markdown("---")
        if st.button(" Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    page = st.session_state.admin_page
    if page == "home":
        _adm_home(user)
    elif page == "my_tickets":
        _adm_tickets(user)
    elif page == "orders":
        _adm_orders(user)
    elif page == "books":
        _adm_books(user)


def _adm_home(user):
    st.markdown("""<div class='page-header'><h1> Administrator Dashboard</h1><p>Manage tickets, orders, and library resources</p></div>""", unsafe_allow_html=True)

    my_tickets = get_tickets_assigned_to(user["emp_id"])
    all_orders = get_all_orders()
    books = get_all_books()

    pending_orders = [o for o in all_orders if o["order_status"] == "pending"]
    open_tickets = [t for t in my_tickets if t["status"] != "completed"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(open_tickets)}</div><div class='metric-label'>Open Tickets</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(pending_orders)}</div><div class='metric-label'>Pending Orders</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{len(books)}</div><div class='metric-label'>Total Books</div></div>""", unsafe_allow_html=True)
    with c4:
        total_avail = sum(b["quantity"] for b in books)
        st.markdown(f"""<div class='metric-card'><div class='metric-value'>{total_avail}</div><div class='metric-label'>Available Copies</div></div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
       st.markdown("####  Recent Assigned Tickets")

       if my_tickets:
          for t in my_tickets[:3]:

            status = t.get("status", "Unknown")

            # Status display
            if status == "Completed":
                color = "#16a34a"
                label = "Completed"
            elif status == "In-process":
                color = "#d97706"
                label = "In Process"
            elif status == "Assigned":
                color ="#2563eb"
                label = " Assigned"
            else:
                color = "#f59e0b"
                label = " New"

            title = t.get("title") or "No Title"
            date = t.get("date_logged") or "N/A"

            st.markdown(f"""
            <div class='ticket-card'>
                <b>#{t['ticket_id']} — {title}</b>
                <span style='color:{color}; float:right; font-size:0.82rem;'>{label}</span>
                <br><small> {date}</small>
            </div>
            """, unsafe_allow_html=True)
       else:
        st.info("No tickets assigned to you.")

    with col2:
        st.markdown("####  Pending Order Requests")
        if pending_orders:
            for o in pending_orders[:3]:
                st.markdown(f"""<div class='ticket-card'>
                    <b>{o['title']}</b><br>
                    <small>👤 {o['student_name']} &nbsp;|&nbsp; {o['borrowed_at'][:10]}</small>
                </div>""", unsafe_allow_html=True)
        else:
            st.success("No pending orders!")


def _adm_tickets(user):
    st.markdown("""
    <div class='page-header'>
        <h1> My Assigned Tickets</h1>
        <p>Reply to student complaints assigned to you</p>
    </div>
    """, unsafe_allow_html=True)

    tickets = get_tickets_assigned_to(user["emp_id"])

    if not tickets:
        st.info("No tickets assigned to you currently.")
        return

    # Correct status filter
    filter_status = st.selectbox(
        "Filter",
        ["All", "Assigned", "In-process", "Completed"]
    )

    if filter_status != "All":
        tickets = [t for t in tickets if t["status"] == filter_status]

    for t in tickets:
        status = t.get("status", "Unknown")
        completed = status == "Completed"

        title = t.get("title") or "No Title"
        desc = t.get("problem_description") or "No description"
        date = t.get("date_logged") or "N/A"
        solution = t.get("solution_description")

        # Status icon
        icon = "✅" if completed else "⏳"

        with st.expander(f"#{t['ticket_id']} — {title} {icon}"):

            st.markdown(f"** Submitted:** {date}")
            st.markdown("** Description:**")
            st.markdown(f"> {desc}")

            # Already resolved
            if solution:
                st.markdown(f"""
                <div style='padding:0.8rem; background:#052e16; border-left:3px solid #22c55e;
                            border-radius:4px; margin:0.5rem 0; color:#bbf7d0;'>
                    <b>✔ Solution:</b><br>{solution}
                </div>
                """, unsafe_allow_html=True)

                st.success("This ticket is completed.")

            # Not resolved → allow reply
            else:
                reply_text = st.text_area(
                    "Write Solution",
                    key=f"reply_{t['ticket_id']}",
                    height=100,
                    placeholder="Type your solution..."
                )

                col1, col2 = st.columns(2)

                # Mark In-process
                with col1:
                    if st.button("🔄 Mark In-process", key=f"process_{t['ticket_id']}"):
                        update_ticket_status(t["ticket_id"], "In-process")
                        st.success("Marked as In-process")
                        st.rerun()

                # Complete ticket
                with col2:
                    if st.button("✅ Submit & Complete", key=f"complete_{t['ticket_id']}"):
                        if not reply_text.strip():
                            st.error("Solution cannot be empty.")
                        else:
                            resolve_ticket(t["ticket_id"], reply_text.strip())
                            st.success("Ticket resolved successfully!")
                            st.rerun()


def _adm_orders(user):
    st.markdown("## Book Orders")

    orders = get_all_orders()

    tabs = st.tabs([" New Orders", " Processing", " All Orders"])

    status_map = {
        "new": "🟡",
        "processed": "🔵",
        "awaiting shipping": "🟠",
        "shipped": "🟢",
        "canceled": "🔴"
    }

    # 🔹 NEW ORDERS
    with tabs[0]:
        new_orders = [o for o in orders if o["order_status"] == "new"]

        if not new_orders:
            st.success("No new orders!")

        for o in new_orders:
            col1, col2, col3 = st.columns([4,1,1])

            with col1:
                st.markdown(f"""
                <div class='card'>
                    <b>Order #{o['orders_id']}</b><br>
                     {o['books']}<br>
                     {o['authors']}<br>
                     {o['student_name']}<br>
                     {o['date_created']}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button("⚙️ Process", key=f"proc_{o['orders_id']}"):
                    update_order_status(o["orders_id"], "processed")
                    st.rerun()

            with col3:
                if st.button("❌ Cancel", key=f"can_{o['orders_id']}"):
                    update_order_status(o["orders_id"], "canceled")
                    st.rerun()

    # PROCESSING / SHIPPING
    with tabs[1]:
        processing = [o for o in orders if o["order_status"] in ["processed", "awaiting shipping"]]

        if not processing:
            st.info("No orders in processing.")

        for o in processing:
            col1, col2 = st.columns([4,1])

            with col1:
                st.markdown(f"""
                <div class='card'>
                    <b>Order #{o['orders_id']}</b><br>
                     {o['books']}<br>
                     {o['student_name']}
                </div>
                """, unsafe_allow_html=True)

            with col2:
                if st.button(" Ship", key=f"ship_{o['orders_id']}"):
                    update_order_status(o["orders_id"], "shipped")
                    st.rerun()

    #  ALL ORDERS
    with tabs[2]:
        if not orders:
            st.info("No orders placed yet.")
        for o in orders:
            st.markdown(f"""
            <div class='card'>
                {status_map.get(o['order_status'],'⚪')} 
                <b>Order #{o['orders_id']}</b>
                <span style='float:right'>{o['order_status']}</span><br>
                 {o['books']}<br>
                {o['student_name']}<br>
                 {o['date_created']}
            </div>
            """, unsafe_allow_html=True)


def _adm_books(user):
    st.markdown("""<div class='page-header'><h1> Manage Books</h1><p>Add, view, and manage library catalogue</p></div>""", unsafe_allow_html=True)

    tab1, tab2, tab3,tab4 = st.tabs([" Book Catalogue", "➕ Add Book", " Manage Categories","Universities"])

    with tab1:
        books = get_all_books()
        st.caption(f"{len(books)} books in library")
        if books:
            
            df = pd.DataFrame(books)[["title", "category_id", "quantity"]]
            df["category_name"] = df["category_id"].map({c["category_id"]: c["category_name"] for c in get_categories()})
            df=df[["title", "category_name", "quantity"]]
            df.columns = ["Title", "Category", "Available"]
            st.dataframe(df, use_container_width=True, hide_index=True)

    
    with tab2:
      categories = get_categories()

      if not categories:
         st.warning("No categories available. Add one first.")
      else:
        cat_options = {c["category_name"]: c["category_id"] for c in categories}

        subcategories = get_subcategories()
        subcat_options = {s["subcategory_name"]: s["subcategory_id"] for s in subcategories}

        with st.form("add_book",clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                title = st.text_input("Book Title *", key="book_title")
                author = st.text_input("Author *", key="book_author")
                isbn = st.text_input("ISBN *", key="book_isbn")

                publisher = st.text_input("Publisher", key="book_publisher")
                publication_date = st.date_input("Publication Date", key="book_pub_date")
                edition_no = st.number_input("Edition No", min_value=1, value=1, key="book_edition")

            with col2:
                category = st.selectbox("Category *", list(cat_options.keys()), key="book_category")
                copies = st.number_input("Total Copies", min_value=1, value=5, key="book_copies")

                price = st.number_input("Price", min_value=0.0, key="book_price")
                language = st.text_input("Language", key="book_lang")
                format_ = st.selectbox("Format", ["Hardcover", "Softcover", "Electronic"], key="book_format")

                type_ = st.selectbox("Type", ["New", "Used"], key="book_type")
                option = st.selectbox("Condition", ["Rent", "Buy"], key="book_option")

            # Subcategories
            selected_subcats = st.multiselect(
                "Select Subcategories",
                list(subcat_options.keys()),
                key="book_subcats"
            )

            new_subcats = st.text_input(
                "Add New Subcategories (comma separated)",
                placeholder="e.g. AI, Data Science",
                key="new_subcats"
            )

            submitted = st.form_submit_button("➕ Add Book", use_container_width=True)

            if submitted:
              if not title or not author or not isbn:
                st.error("Title, Author, ISBN required.")
              else:
                # existing subcat ids
                selected_ids = [subcat_options[s] for s in selected_subcats]

                # new subcats
                new_ids = []
                if new_subcats:
                    for sub in [x.strip() for x in new_subcats.split(",") if x.strip()]:
                        row = run_query(
                            "SELECT subcategory_id FROM subcategory WHERE LOWER(subcategory_name)=%s",
                            (sub.lower(),),
                            fetch=True,
                            one=True
                        )

                        if row:
                            new_ids.append(row["subcategory_id"])
                        else:
                            run_query(
                                "INSERT INTO subcategory (subcategory_name) VALUES (%s)",
                                (sub.title(),),
                                fetch=True,
                            )
                            new_id = run_query("select max(subcategory_id) as id from subcategory", fetch=True, one=True)["id"]
                            new_ids.append(new_id)

                all_subcat_ids = list(set(selected_ids + new_ids))

                ok, msg = add_book(
                    title, author, isbn,
                    cat_options[category],
                    copies, publisher,
                    publication_date, edition_no,
                    language, format_, type_,
                    option, price,
                    all_subcat_ids
                )

                if ok:
                    st.success(msg)

                    st.rerun()
                else:
                    st.error(msg)

    with tab3:
        categories = get_categories()
        st.markdown("**Existing Categories:**")
        cols = st.columns(4)
        for i, c in enumerate(categories):
            with cols[i % 4]:
                st.markdown(f"<span class='book-cat'>{c['category_name']}</span>", unsafe_allow_html=True)

        st.markdown("---")
        with st.form("add_cat"):
            new_cat = st.text_input("New Category Name",placeholder="e.g. Science Fiction, History...",key="new_cat")
            if st.form_submit_button("Add Category"):
                if new_cat:
                    ok, msg = add_category(new_cat)
                    if ok:
                        st.success(msg)
                        st.session_state.new_cat = ""  # Clear input
                        st.rerun()
                    else:
                        st.error(msg)
                    
    with tab4:
        universities = get_universities()
        st.markdown("**Existing Universities:**")
        cols = st.columns(4)
        for i, c in enumerate(universities):
            with cols[i % 4]:
                st.markdown(f"<span class='book-cat'>{c['name']}</span>", unsafe_allow_html=True)

        st.markdown("---")

        with st.form("add_university", clear_on_submit=True):

         name = st.text_input("University Name", placeholder="e.g. IIT Madras")
         address = st.text_input("Address", placeholder="City, State")
    
         col1, col2 = st.columns(2)
         with col1:
           rep_first = st.text_input("Representative First Name")
         with col2:
           rep_last = st.text_input("Representative Last Name")

         email = st.text_input("Email", placeholder="uni@email.com")
         phoneno = st.text_input("Phone Number", placeholder="XXXXXXXXXX")
         submitted = st.form_submit_button("Add University")

         if submitted:
           if not name or not rep_first or not rep_last or not email or not phoneno:
            st.error("All fields are required")
           else:
             ok, msg = add_university(
                name, address, rep_first, rep_last, email, phoneno
             )
             if ok:
                st.success(msg)
                st.rerun()
             else:
                st.error(msg)
