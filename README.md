# 📚 Gyaan Pustak — Library Management System

A clean, multi-role library management system built with Streamlit and SQLite.

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501**

---

## 🔐 Demo Login Credentials

| Role | Email | Password |
|---|---|---|
| Student | arjun@student.du.ac.in | student123 |
| Customer Support | support@gyaanpustak.in | support123 |
| Administrator | libadmin@gyaanpustak.in | libadmin123 |
| Super Admin | admin@gyaanpustak.in | admin123 |

---

## 👤 Roles & Features

### 🎓 Student
- Browse & search books by title, author, category
- View course-linked books from their profile
- Add books to cart, checkout (borrow request)
- Track orders (pending / approved / returned)
- Raise support tickets (complaints)
- View ticket history & admin replies
- Profile page showing university, course, instructor

### 🎧 Customer Support
- View all tickets with their status
- Assign tickets to administrators
- Cannot reply or edit ticket content — read-only + assign only
- Status tracking: Not Assigned → Assigned → Solved

### 🔧 Administrator
- Resolve assigned tickets by writing replies (marks as solved)
- Approve / Reject student borrow orders
- Mark returned books
- Manage book catalogue (add books, categories)

### ⭐ Super Admin
- Add / deactivate employees (Customer Support & Administrator)
- View all students, orders, tickets
- Overview of universities, departments, courses
- Full system statistics dashboard

---

## 🏗️ Data Model

```
University → Department → Instructor → Course → Book
Student → (University, Course)
Order: Student borrows Book
Ticket: Student raises → CS assigns → Admin replies
```

---

## 📁 File Structure

```
gyaan_pustak/
├── app.py              # Entry point, CSS, routing
├── database.py         # SQLite DB, all queries, seed data
├── auth.py             # Login + Student registration
├── student.py          # Student dashboard (all pages)
├── customer_support.py # CS dashboard
├── administrator.py    # Admin dashboard
├── super_admin.py      # Super admin dashboard
├── requirements.txt
└── README.md
```

---

## 🗄️ Database

Uses **SQLite** (`gyaan_pustak.db`) — auto-created on first run.  
Delete the `.db` file to reset all data and re-seed.
