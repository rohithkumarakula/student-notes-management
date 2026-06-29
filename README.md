# 📚 Student Notes Management System

A Flask-based web application that allows students to securely upload, manage, search, download, and delete PDF notes.

---
## 🌐 Live Demo

**Website:** https://student-notes-management-ngzi.onrender.com/

**GitHub Repository:** https://github.com/rohithkumarakula/student-notes-management

## ✨ Features

- 🔐 User Registration & Login
- 🔒 Password Hashing
- 👤 Session Management
- 📤 Upload PDF Notes
- 📥 Download Notes
- 🔍 Search Notes
- 🗑️ Delete Notes
- 📊 Dashboard with Total Notes
- 👥 Multi-user Support (Each user sees only their own notes)

---

## 🛠️ Tech Stack

- Python
- Flask
- SQLite
- HTML5
- Bootstrap 5
- Jinja2
- Git & GitHub

---

## 📁 Project Structure

```
student-notes-management/
│
├── app.py
├── database.py
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── index.html
│   ├── login.html
│   ├── notes.html
│   ├── register.html
│   └── upload.html
│
├── uploads/
├── README.md
├── requirements.txt
└── .gitignore
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/rohithkumarakula/student-notes-management.git
```

Move into the project folder:

```bash
cd student-notes-management
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create the database:

```bash
python database.py
```

Run the application:

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

> Screenshots will be added soon.

---

## 👨‍💻 Author

**Akula Rohith**

GitHub:
https://github.com/rohithkumarakula

---

## ⭐ Future Improvements

- Admin Panel
- Profile Page
- Email Verification
- Password Reset
- Cloud File Storage
- PostgreSQL Support
- Dark Mode
- Deploy on Render