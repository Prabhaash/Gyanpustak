from asyncio.windows_events import NULL
from datetime import datetime
from datetime import date
import datetime
import streamlit as st
import mysql.connector
import time

# Connection reuse (HUGE PERFORMANCE BOOST)
@st.cache_resource
def get_conn():
    return mysql.connector.connect(
        host="192.168.249.237",
        user="root",
        password="root123",
        database="Gyanpustak",
        autocommit=True
    )

def run_query(query, values=None, fetch=False, one=False):
    conn = get_conn()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(query, values or ())

    if fetch:
        result = cursor.fetchone() if one else cursor.fetchall()
    else:
        conn.commit()
        result = None

    cursor.close()
    return result

# ── USERS ──────────────────────────────────────────────
def get_superadmin_by_email(email):
    return run_query(
        "SELECT * FROM employee WHERE email=%s and role='super_admin'",
        (email,), fetch=True, one=True
    )

def get_admin_by_email(email):
    return run_query(
        "SELECT * FROM administrator WHERE email=%s",
        (email,), fetch=True, one=True
    )

def get_student_by_email(email):
    return run_query(
        "SELECT * FROM student WHERE email=%s",
        (email,), fetch=True, one=True
    )

def get_student_profile(student_id):
    return run_query(
        """SELECT s.*, u.name as university_name, d.dept_name as department_name    
           FROM student s
           JOIN university u ON s.university_id=u.university_id
           JOIN department d ON s.dept_id=d.dept_id
           WHERE s.student_id=%s""",
        (student_id,), fetch=True, one=True
    )


def get_student_id(email):
    student = get_student_by_email(email)
    return student["student_id"] if student else None


def get_employee_by_email(email):
    return run_query(
        "SELECT * FROM employee WHERE email=%s",
        (email,), fetch=True, one=True
    )

def get_administrators():
    return run_query(
        "SELECT * FROM administrator",
        fetch=True
    )


def create_employee(firstname, lastname, gender, salary, aadhar, email, address, phoneno, role, password):
    try:
        # Step 1: Insert into employee
        run_query(
            """INSERT INTO employee 
               (firstname, lastname, gender, salary, aadhaar, email, phoneno, role, password) 
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (firstname, lastname, gender, salary, aadhar, email, phoneno, role, password)
        )
        emp_id =run_query("select emp_id from employee where email=%s", (email,), fetch=True, one=True)["emp_id"]

        # Step 2: Insert into role-specific table using SAME emp_id
        if role == "administrator":
            run_query(
                """INSERT INTO administrator 
                   (emp_id, firstname, lastname, gender, salary, aadhaar, email, address, password, phoneno) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (emp_id, firstname, lastname, gender, salary, aadhar, email, address, password, phoneno)
            )

        elif role == "customer_support":
            run_query(
                """INSERT INTO customer_support 
                   (emp_id, firstname, lastname, gender, salary, aadhaar, email, password, address, phoneno) 
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
                (emp_id, firstname, lastname, gender, salary, aadhar, email, password, address, phoneno)
            )

        return True, "Employee created"

    except Exception as e:
        return False, str(e)
    

#all employees
def get_employees():
    return run_query("SELECT * FROM employee", fetch=True)

#all categories
def get_categories():
    return run_query("SELECT * FROM category", fetch=True)

#universities info=get_universities()
def get_universities():
    return run_query("SELECT * FROM university", fetch=True)

#get subcategories
def get_subcategories():
    return run_query("SELECT * FROM subcategory", fetch=True)

#departments info=get_departments()
def get_departments(university_id=None): 
    if university_id:
        return run_query("SELECT * FROM department WHERE university_id=%s", (university_id,), fetch=True)
    return run_query("SELECT * FROM department", fetch=True)


def register_student(firstname, lastname, address, email, phoneno,
                     dateofbirth, university_id, department_id,
                     status, curyear, password):
    try:
        run_query(
            """INSERT INTO student 
               (firstname, lastname, address, email, phoneno, dob,
                university_id, dept_id, status, curyear, password)
               VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
            (firstname, lastname, address, email, phoneno,
             dateofbirth, university_id, department_id,
             status, curyear, password)
        )
        return True, "Registered successfully"

    except Exception as e:
        return False, str(e) 


def toggle_user(user_id, active):
    run_query(
        "UPDATE users SET is_active=%s WHERE id=%s",
        (active, user_id)
    )

# All books
def get_all_books(search=""):
    return run_query(
        """SELECT b.*
           FROM books b""",
        fetch=True
    )

#get books by category
def get_books_by_category(search, category_id):
    query = """
        SELECT 
            b.*,
            COALESCE(ROUND(AVG(r.rating),1),0) as avg_rating
        FROM books b
        LEFT JOIN review r ON b.isbn=r.isbn
        WHERE 1=1
    """

    params = []

    if category_id:
        query += " AND b.category_id=%s"
        params.append(category_id)

    if search:
        query += " AND b.title LIKE %s"
        params.append(f"%{search}%")

    query += " GROUP BY b.isbn"

    return run_query(query, tuple(params), fetch=True)

#get all students
def get_all_students():
    return run_query(
        """SELECT s.*, u.name as university_name, d.dept_name as department_name    
           FROM student s
           JOIN university u ON s.university_id=u.university_id
           JOIN department d ON s.dept_id=d.dept_id""",
        fetch=True
    )

#all the orders info
def get_all_orders():
    return run_query("""
        SELECT 
            o.orders_id,
            o.order_status,
            o.date_created,
            s.email,
            CONCAT(s.firstname, ' ', s.lastname) AS student_name,
            GROUP_CONCAT(DISTINCT b.title) AS books,
            GROUP_CONCAT(DISTINCT ob.isbn) AS isbns

        FROM orders o
        JOIN student s ON o.student_id = s.student_id
        JOIN orders_book ob ON o.orders_id = ob.orders_id
        JOIN books b ON ob.isbn = b.isbn
        GROUP BY o.orders_id
        ORDER BY o.orders_id DESC
    """, fetch=True)

#update ticket status
def update_ticket_status(ticket_id, status):
    run_query("""
        UPDATE trouble_ticket
        SET status=%s
        WHERE ticket_id=%s
    """, (status, ticket_id))


def get_cart_id(student_id):
    res = run_query(
        "SELECT cart_id FROM cart WHERE created_by=%s ORDER BY cart_id DESC LIMIT 1",
        (student_id,), fetch=True, one=True
    )
    return res["cart_id"] if res else None


def get_cart_entry(student_id):
    run_query(
        "INSERT INTO cart (date_created, date_last_updated, created_by) VALUES (CURDATE(), CURDATE(), %s)",
        (student_id,)
    )
    return run_query("SELECT LAST_INSERT_ID() as id", fetch=True, one=True)["id"]


def get_cart_of_student(cart_id):
    return run_query(
        """SELECT cb.cart_id, cb.isbn, b.title, b.quantity
           FROM cart_book cb
           JOIN books b ON cb.isbn=b.isbn
           WHERE cb.cart_id=%s""",
        (cart_id,), fetch=True
    )


def add_to_cart(student_id, isbn):
    try:
        cart_id = get_cart_id(student_id)

        if not cart_id:
            cart_id = get_cart_entry(student_id)

        exists = run_query(
            "SELECT 1 FROM cart_book WHERE cart_id=%s AND isbn=%s",
            (cart_id, isbn), fetch=True, one=True
        )

        if exists:
            return False, "Already in cart"

        run_query(
            "INSERT INTO cart_book (cart_id, isbn) VALUES (%s, %s)",
            (cart_id, isbn)
        )

        return True, "Added to cart"

    except Exception as e:
        return False, str(e)


def remove_from_cart(cart_id, isbn):
    run_query(
        "DELETE FROM cart_book WHERE cart_id=%s AND isbn=%s",
        (cart_id, isbn)
    )

def add_university(name, address, rep_first, rep_last, email, phoneno):
    try:
        # check duplicate
        exists = run_query(
            "SELECT * FROM university WHERE LOWER(name)=%s",
            (name.lower(),),
            fetch=True,
            one=True
        )

        if exists:
            return False, "University already exists"

        # generate ID manually (since no auto_increment)
        uni_id = run_query(
            "SELECT MAX(university_id) as id FROM university",
            fetch=True,
            one=True
        )["id"] or 0

        uni_id += 1

        run_query(
            """INSERT INTO university
               (university_id, name, address, rep_first_name,
                rep_last_name, email, phoneno)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (uni_id, name, address, rep_first, rep_last, email, phoneno)
        )

        return True, "University added successfully"

    except Exception as e:
        return False, str(e)

#add new book
def add_book(title, author, isbn, category_id, copies,publisher, publication_date, edition_no,language, format_, type_, option, price, subcat_ids):
    try:
        # check duplicate
        if run_query("SELECT 1 FROM books WHERE isbn=%s",
                     (isbn,), fetch=True, one=True):
            return False, "ISBN exists"

        # insert book
        run_query("""
            INSERT INTO books
            (isbn, title, quantity, category_id, publisher,
             publication_date, edition_no, language,
             format, type, options, price)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            isbn, title, copies, category_id,
            publisher, publication_date, edition_no,
            language, format_, type_, option, price
        ))

        # author handling
        row = run_query(
            "SELECT author_id FROM author WHERE author_name=%s",
            (author,), fetch=True, one=True
        )

        if row:
            author_id = row["author_id"]
        else:
            run_query(
                "INSERT INTO author (author_name) VALUES (%s)",
                (author,),
                fetch=True )
            author_id = run_query("SELECT MAX(author_id) as id FROM author", fetch=True, one=True)["id"]
        run_query(
            "INSERT INTO book_author (isbn, author_id) VALUES (%s,%s)",
            (isbn, author_id)
        )

        # subcategories
        for subcat_id in subcat_ids:
            run_query(
                "INSERT INTO book_subcategory (subcategory_id, isbn) VALUES (%s,%s)",
                (subcat_id, isbn)
            )

        return True, "Book added successfully"

    except Exception as e:
        return False, str(e)

# ── COURSES ──────────────────────────────────────────────
def get_courses():
    return run_query("SELECT * FROM course", fetch=True)

def get_books_by_course(course_id):
    return run_query(
        """SELECT b.*
           FROM books b
           JOIN book_course bc ON b.isbn=bc.isbn
           WHERE bc.course_id=%s""",
        (course_id,), fetch=True
    )


# ── ORDERS ──────────────────────────────────────────────
def checkout_cart(student_id, shipping_type, card_no, expiry_date, holder_name):
    try:
        today = datetime.date.today()

        # Get cart
        cart = run_query(
            "SELECT cart_id FROM cart WHERE created_by=%s ORDER BY cart_id DESC LIMIT 1",
            (student_id,), fetch=True, one=True
        )
        
        if not cart:
            return False, "Cart not found"

        cart_id = cart["cart_id"]


        # Get items
        items = run_query(
            "SELECT isbn FROM cart_book WHERE cart_id=%s",
            (cart_id,), fetch=True
        )

        if not items:
            return False, "Cart empty"

        # Create order
        run_query(
            """INSERT INTO orders 
               (student_id, date_created, shipping_type,
                credit_card_number, credit_card_expiry_date,
                credit_card_holder_name, order_status)
               VALUES (%s,%s,%s,%s,%s,%s,%s)""",
            (
                student_id,
                today,
                shipping_type,
                card_no,
                expiry_date,
                holder_name,
                "new"
            )
        )

        # Get latest order_id
        order_id = run_query(
            "SELECT MAX(orders_id) as id FROM orders",
            fetch=True, one=True
        )["id"]

        # Insert books into orders_book
        for item in items:
            run_query(
                "INSERT INTO orders_book (orders_id, isbn) VALUES (%s,%s)",
                (order_id, item["isbn"])
            )

        # Clear cart
        run_query(
            "DELETE FROM cart_book WHERE cart_id=%s",
            (cart_id,)
        )

        return True, "✅ Order placed successfully!"

    except Exception as e:
        return False, str(e)

#add new category
def add_category(category_name):
    try:
        category_name = category_name.strip().lower()

        checker = run_query(
            "SELECT * FROM category WHERE LOWER(category_name)=%s",
            (category_name,),fetch=True,one=True
        )

        if checker:
            return False, "Category exists"

        cat_id = run_query( "SELECT MAX(category_id) as c FROM category",fetch=True,one=True)["c"] or 0
        cat_id+= 1

        run_query(  "INSERT INTO category (category_id, category_name) VALUES (%s,%s)",(cat_id, category_name.title()))

        return True, "Category added"
    except Exception as e:
        return False, str(e)

#get cart of each student
def get_cart_of_student(cart_id):
    return run_query(
        """SELECT cb.*,b.*
           FROM cart_book cb
           join books b on cb.isbn=b.isbn
           WHERE cb.cart_id = %s""",
        (cart_id,), fetch=True
    )

#get all tickets for a student
def get_tickets_by_student(student_id):
    return run_query(
        """SELECT t.*
           FROM trouble_ticket t
           WHERE t.student_id=%s
           ORDER BY t.date_logged DESC""",
        (student_id,), fetch=True
    )

def get_orders(student_id):
    return run_query("""
        SELECT 
            o.orders_id,
            o.order_status,
            o.date_created
        FROM orders o
        WHERE o.student_id=%s
        ORDER BY o.orders_id DESC
    """, (student_id,), fetch=True)

#orders by each student with status not canceled
def get_orders_by_student(student_id):
    return run_query("""
        SELECT 
            o.orders_id,
            o.order_status,
            o.date_created,
            b.title,
            b.isbn
        FROM orders o
        JOIN orders_book ob ON o.orders_id = ob.orders_id
        JOIN books b ON ob.isbn = b.isbn
        WHERE o.student_id=%s
        ORDER BY o.orders_id DESC
    """, (student_id,), fetch=True)

def update_order_status(order_id, status):
    run_query(
        "UPDATE orders SET order_status=%s WHERE orders_id=%s",
        (status, order_id)
    )

#request caancellation
def request_cancel_order(order_id, student_id):
    try:
        today = date.today()

        run_query(
            "UPDATE orders SET order_status='order_cancellation' WHERE orders_id=%s AND student_id=%s",
            (order_id, student_id)
        )

        return True, "Cancel request sent to support"

    except Exception as e:
        return False, str(e)


def get_cancel_requests():
    return run_query(
        """SELECT 
               o.orders_id,
               o.order_status,
               o.date_created,
               CONCAT(s.firstname, ' ', s.lastname) AS student_name
           FROM orders o
           JOIN student s ON o.student_id = s.student_id
           WHERE o.order_status = 'order_cancellation'
           ORDER BY o.date_created DESC
        """,
        fetch=True
    )

def add_review(student_id, isbn, rating, description=""):
    try:
        run_query(
            """INSERT INTO review (isbn, student_id, rating, description)
               VALUES (%s,%s,%s,%s)
               ON DUPLICATE KEY UPDATE rating=%s, description=%s""",
            (isbn, student_id, rating, description, rating, description)
        )
        return True, "Review added"
    except Exception as e:
        return False, str(e)


def get_avg_rating(isbn):
    res = run_query(
        "SELECT AVG(rating) as avg_rating FROM review WHERE isbn=%s",
        (isbn,), fetch=True, one=True
    )
    return round(res["avg_rating"], 1) if res and res["avg_rating"] else 0

# ── TICKETS ──────────────────────────────────────────────
from datetime import date

#ticket by student
def create_ticket_st(student_id, subject, description):
    today = date.today()

    run_query("""
    INSERT INTO trouble_ticket(date_logged, createdby, title, problem_description,
     status, student_id, support_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s)""", (
    today,"student",subject,
    description,"New",student_id,None
    ))

    ticket_id = run_query("SELECT MAX(ticket_id) as id from trouble_ticket", fetch=True, one=True)["id"]
    # history
    run_query("""
        INSERT INTO ticket_history (ticket_id, change_date)
        VALUES (%s,%s)
    """, (ticket_id, today))


#ticket by customer support
def create_ticket_cs(support_id, title, description):
    today = date.today()

    run_query("""INSERT INTO trouble_ticket(date_logged, createdby, title, problem_description, status, student_id, support_id)
    VALUES (%s,%s,%s,%s,%s,%s,%s)""", (
    today,"customersupport",title,
    description,"New",None,support_id))

    ticket_id = run_query("SELECT MAX(ticket_id) as id from trouble_ticket", fetch=True, one=True)["id"]
    # history
    run_query("""
        INSERT INTO ticket_history (ticket_id, change_date)
        VALUES (%s,%s)
    """, (ticket_id, today))

# all tickets for admin view
def get_all_tickets():
    return run_query(
        """SELECT t.*
           FROM trouble_ticket t
           ORDER BY t.date_logged DESC""",
        fetch=True
    )

#gets tickets assigned to a particular admin
def get_tickets_assigned_to(emp_id):
    return run_query("""
        SELECT 
            ticket_id,
            title,
            problem_description,
            solution_description,
            date_logged,
            status
        FROM trouble_ticket
        WHERE emp_id = %s
        ORDER BY ticket_id DESC
    """, (emp_id,), fetch=True)

def assign_ticket(ticket_id, emp_id):
    run_query("""
        UPDATE trouble_ticket
        SET emp_id=%s,
            status='Assigned'
        WHERE ticket_id=%s
    """, (emp_id, ticket_id))

def resolve_ticket(ticket_id, solution):
    run_query("""
        UPDATE trouble_ticket
        SET solution_description=%s,
            completion_date=CURDATE(),
            status='Completed'
        WHERE ticket_id=%s
    """, (solution, ticket_id))

# ── STATS ──────────────────────────────────────────────
def get_dashboard_stats():
    stats = {}
    stats["total_books"] = run_query("SELECT COUNT(*) as c FROM books", fetch=True, one=True)["c"]
    stats["total_students"] = run_query("SELECT COUNT(*) as c FROM student", fetch=True, one=True)["c"]
    stats["total_orders"] = run_query("SELECT COUNT(*) as c FROM orders", fetch=True, one=True)["c"]
    stats["total_employees"] = run_query("SELECT COUNT(*) as c FROM employee", fetch=True, one=True)["c"]
    stats["active_orders"] = run_query("SELECT COUNT(*) as c FROM orders WHERE order_status!='cancelled'", fetch=True, one=True)["c"]
    stats["pending_orders"] = run_query("SELECT COUNT(*) as c FROM orders WHERE order_status='pending'", fetch=True, one=True)["c"]
    stats["open_tickets"] = run_query("SELECT COUNT(*) as c FROM trouble_ticket WHERE status='New'", fetch=True, one=True)["c"]
    return stats

