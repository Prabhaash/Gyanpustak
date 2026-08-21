import streamlit as st
from database import *

STATUS_COLORS = {
    "New": ("🔘", "#f3f4f6", "#374151", "New"),
    "Assigned": ("🔵", "#dbeafe", "#1e40af", "Assigned"),
    "In-process": ("🟡", "#fef9c3", "#92400e", "In Progress"),
    "Completed": ("✅", "#d1fae5", "#065f46", "Completed"),
}

def customer_support_dashboard(user):
    with st.sidebar:
        st.markdown(f"""
        <div class='sidebar-brand'>
            <div style='font-weight:700; font-size:1.1rem;'>Gyan Pustak</div>
            <div style='font-size:0.8rem; opacity:0.7; margin-top:0.2rem;'>Customer Support</div>
        </div>
        """, unsafe_allow_html=True)
        fullname=user['firstname'] + " " + user['lastname']
        st.markdown(f"**{fullname}**")
        st.caption("Customer Support")
        st.markdown("---")

        pages = {" Dashboard": "home", " Raise Ticket": "new_ticket"," All Tickets": "tickets","Cancellation Requests": "cancellations"}
        if "cs_page" not in st.session_state:
            st.session_state.cs_page = "home"

        for label, key in pages.items():
            if st.button(label, key=f"cs_nav_{key}", use_container_width=True):
                st.session_state.cs_page = key

        st.markdown("---")
        if st.button(" Logout", use_container_width=True):
            st.session_state.user = None
            st.rerun()

    page = st.session_state.cs_page
    if page == "home":
        _cs_home(user)
    elif page == "new_ticket":
        _cs_raise_ticket(user)
    elif page == "tickets":
        _cs_tickets(user)
    elif page == "cancellations":
        _cs_cancel_orders(user)


def _cs_home(user):
    st.markdown("""<div class='page-header'><h1> Support Dashboard</h1><p>Manage and assign student complaints</p></div>""", unsafe_allow_html=True)

    tickets = get_all_tickets()

    new_tickets = [t for t in tickets if t["status"] == "New"]
    assigned = [t for t in tickets if t["status"] == "Assigned"]
    in_process = [t for t in tickets if t["status"] == "In-process"]
    completed = [t for t in tickets if t["status"] == "Completed"]

    c1, c2, c3, c4 = st.columns(4)

    with c1:
     st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{len(new_tickets)}</div>
        <div class='metric-label'>🔘 New</div>
    </div>
    """, unsafe_allow_html=True)

    with c2:
     st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{len(assigned)}</div>
        <div class='metric-label'> Assigned</div>
    </div>
    """, unsafe_allow_html=True)

    with c3:
     st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{len(in_process)}</div>
        <div class='metric-label'>In Process</div>
    </div>
    """, unsafe_allow_html=True)

    with c4:
     st.markdown(f"""
    <div class='metric-card'>
        <div class='metric-value'>{len(completed)}</div>
        <div class='metric-label'>Completed</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### Unassigned Tickets — Action Required")
    if not new_tickets:
        st.success("All tickets are assigned! Great work.")
    else:
        admins = get_administrators()
        admin_options = {a["firstname"] + " " + a["lastname"]: a["emp_id"] for a in admins}

        for t in new_tickets[:5]:
            with st.container():
             st.markdown(f"""<div class='ticket-card'>
            <b>#{t['ticket_id']} — {t['title']}</b>
            <br><small>👤 {t.get('student_name','N/A')} &nbsp;|&nbsp; {str(t['date_logged'])[:10]}</small>
            <br><span style='color:#9ca3af; font-size:0.88rem;'>
                {t['problem_description'][:120]}{'...' if t['problem_description'] and len(t['problem_description'])>120 else ''}
            </span>
        </div>
        """, unsafe_allow_html=True)

        if admin_options:
            col1, col2 = st.columns([3, 1])

            with col1:
                sel = st.selectbox(
                    "Assign to",
                    list(admin_options.keys()),
                    key=f"assign_sel_{t['ticket_id']}"
                )

            with col2:
                st.markdown("<br>", unsafe_allow_html=True)

                if st.button("Assign", key=f"assign_btn_{t['ticket_id']}"):
                    assign_ticket(t["ticket_id"], admin_options[sel])
                    st.success(f"Ticket #{t['ticket_id']} assigned to {sel}!")
                    st.rerun()
        else:
            st.warning("No administrators available.")

        st.markdown("---")


# Raise new ticket
def _cs_raise_ticket(user):
    st.markdown(" Raise a Ticket")

    with st.form("ticket_form"):

        subject = st.text_input("Subject *")
        description = st.text_area("Problem Description *")

        submitted = st.form_submit_button("Submit Ticket")

    if submitted:
        if not subject or not description:
            st.error("Please fill all required fields.")
        else:
            create_ticket_cs(
                user["emp_id"],subject,description
            )
            st.success("✅ Ticket submitted!")
            st.rerun()


# View and manage all tickets
def _cs_tickets(user):
    st.markdown("""
    <div class='page-header'>
        <h1> All Tickets</h1>
        <p>View and manage tickets</p>
    </div>
    """, unsafe_allow_html=True)

    tickets = get_all_tickets()

    #Status filter (matches DB constraint)
    filter_status = st.selectbox(
        "Filter by Status",
        ["All", "New", "Assigned", "In-process", "Completed"]
    )

    if filter_status != "All":
        tickets = [t for t in tickets if t["status"] == filter_status]

    st.caption(f"Showing {len(tickets)} tickets")

    # Status icons
    STATUS_ICONS = {
        "New": "🟡",
        "Assigned": "🔵",
        "In-process": "🟠",
        "Completed": "🟢"
    }

    # Ticket Cards
    for t in tickets:
        icon = STATUS_ICONS.get(t["status"], "⚪")

        title = t.get("title") or "No Title"
        desc = t.get("problem_description") or "No description provided"
        date = t.get("date_logged") or "N/A"
        status = t.get("status") or "Unknown"
        emp = t.get("emp_id")
        solution = t.get("solution_description")

        assigned_text = f"🔧 Assigned to: {emp}" if emp else "❗ Not Assigned"
        solution_text = f"✔ Solution: {solution}" if solution else ""

        solution_html = "" 
        if solution_text:
           solution_html = f"""
              <div style='margin-top:6px; color:#22c55e;'>
             <small>{solution_text}</small>
            </div>"""

        desc_text = desc[:150] + "..." if desc and len(desc) > 150 else (desc or "")

        st.markdown(f"### #{t['ticket_id']} — {title}")
        st.markdown(f"**{icon} {status}**")
        st.markdown(f" {date}")
        st.markdown(f"<span style='color:#9ca3af'>{desc_text}</span>", unsafe_allow_html=True)
        st.markdown(f"{assigned_text}")

        if solution_html:
           st.markdown(solution_html, unsafe_allow_html=True)
        st.markdown("---")
        
    # Assignment Section
    unassigned = [t for t in tickets if t["emp_id"] is None]

    if unassigned:
        st.markdown("---")
        st.markdown("### 🔧 Assign Tickets")

        admins = get_administrators()
        if not admins:
            st.warning("No administrators available")
            return

        admin_options = {
            f"{a['firstname']} {a['lastname']}": a["emp_id"]
            for a in admins
        }

        ticket_options = {
            f"#{t['ticket_id']} — {t['title']}": t["ticket_id"]
            for t in unassigned
        }

        col1, col2, col3 = st.columns(3)

        with col1:
            sel_ticket = st.selectbox("Select Ticket", list(ticket_options.keys()))

        with col2:
            sel_admin = st.selectbox("Assign To", list(admin_options.keys()))

        with col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✅ Assign Now", use_container_width=True):
                assign_ticket(
                    ticket_options[sel_ticket],
                    admin_options[sel_admin]
                )
                st.success("Assigned successfully!")
                st.rerun()

def _cs_cancel_orders(user):
    st.title("Cancel Requests")

    orders = get_cancel_requests()

    if not orders:
        st.info("No cancellation requests")
        return

    for o in orders:
        st.subheader(f"Order #{o['orders_id']}")
        st.caption(f"{o['student_name']} | {o['date_created']}")

        col1, col2 = st.columns(2)

        # APPROVE
        with col1:
            if st.button("Approve", key=f"approve_{o['orders_id']}"):
                update_order_status(o["orders_id"], "cancelled")
                st.success("Order canceled")
                st.rerun()

        # REJECT
        with col2:
            if st.button(" Reject", key=f"reject_{o['orders_id']}"):
                update_order_status(o["orders_id"], "processed")
                st.warning("Request rejected")
                st.rerun()

        st.markdown("---")