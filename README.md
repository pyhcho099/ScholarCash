# 💰 ScholarCash

A **student token economy system** built with Django + MySQL. Designed for educational institutions to manage virtual currency, rewards, and a campus marketplace.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Django](https://img.shields.io/badge/Django-5.0-green?logo=django)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue?logo=mysql)
![Status](https://img.shields.io/badge/Status-In%20Development-yellow)

---

## 📋 Overview

ScholarCash enables schools to:
- **Reward students** with digital tokens for achievements, attendance, or good behavior
- **Manage a campus marketplace** where students can spend tokens on items/privileges
- **Track all transactions** with an immutable ledger
- **Provide dashboards** for both students and administrators

---

## ✅ Current Progress

### What's Working

| Feature | Status | Description |
|---------|--------|-------------|
| **User Authentication** | ✅ Complete | Login/logout with session-based auth |
| **Role-based Access** | ✅ Complete | Student vs Admin permissions |
| **Database Models** | ✅ Complete | Users, Wallets, Transactions, Inventory |
| **Student Dashboard** | ✅ Complete | View wallet balance & transaction history |
| **Admin Panel** | ✅ Complete | Django admin for user/inventory management |
| **Purchase System** | ✅ Complete | Atomic transactions with race condition protection |
| **Navigation Routing** | ✅ Complete | Dynamic Django URL routing |

### Core Models

```
CustomUser     → Extended user with roles (STUDENT/ADMIN), student_id, grade
Wallet         → Balance tracking with validation (no negative balance)
Transaction    → Immutable ledger (CREDIT, PURCHASE, REFUND, PENALTY)
InventoryItem  → Shop products with stock management
```

---

## 🚧 What's Left to Implement

### High Priority
- [ ] **User Registration** – Self-service signup for students
- [ ] **Admin Credit System** – UI for admins to award tokens to students
- [ ] **Shop Marketplace Page** – Student-facing product catalog with buy buttons
- [ ] **Passbook/Transaction History** – Full paginated history view

### Medium Priority
- [ ] **Base Template Refactor** – Shared `base.html` layout for DRY templates
- [ ] **Admin User Management** – UI to view/edit/suspend users
- [ ] **Admin Inventory Management** – UI to add/edit/remove products
- [ ] **Flash Messages Styling** – Better UI for success/error messages

### Nice to Have
- [ ] **Password Reset** – Email-based password recovery
- [ ] **Student Leaderboard** – Gamification with token rankings
- [ ] **Transaction Export** – CSV/PDF reports
- [ ] **API Endpoints** – REST API for mobile app integration
- [ ] **Audit Logs** – Track admin actions

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Django 5.0
- **Database**: MySQL 8.0
- **Frontend**: HTML, CSS, JavaScript (Django templates)
- **Authentication**: Django's built-in session auth

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- MySQL 8.0+
- pip

### 1. Clone & Setup
```bash
git clone https://github.com/pyhcho099/ScholarCash.git
cd ScholarCash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
```

### 2. Database Setup
Run in MySQL:
```sql
CREATE DATABASE scholarcash_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'scholarcash_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON scholarcash_db.* TO 'scholarcash_user'@'localhost';
FLUSH PRIVILEGES;
```

### 3. Configure Environment
Create `.env` file (copy from example or create new):
```env
SECRET_KEY=your-secret-key-here
DB_NAME=scholarcash_db
DB_USER=scholarcash_user
DB_PASSWORD=secure_password_here
DB_HOST=localhost
DB_PORT=3306
DEBUG=True
```

### 4. Initialize & Run
```bash
python manage.py makemigrations core
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit: http://127.0.0.1:8000

---

## 📁 Project Structure

```
ScholarCash/
├── manage.py              # Django CLI
├── requirements.txt       # Dependencies
├── .env                   # Environment variables (not committed)
├── scholarcash/           # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── core/                  # Main app
│   ├── models.py          # Database models
│   ├── views.py           # Request handlers
│   ├── admin.py           # Admin configuration
│   └── migrations/
├── templates/             # HTML templates
│   ├── admin/
│   └── student/
└── static/                # CSS, JS, images
```

---

## 👥 Contributing

1. Fork the repo
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is for educational purposes.

---

## 📞 Contact

**Project Link**: [https://github.com/pyhcho099/ScholarCash](https://github.com/pyhcho099/ScholarCash)
