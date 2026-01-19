# Backend Setup & Run Guide

I have successfully initialized the **Django + MySQL** backend for ScholarCash.

## 📂 Project Structure
- **[manage.py](file:///d:/New%20folder%20%283%29/Templates/manage.py)**: Command-line utility.
- **`scholarcash/`**: Project settings and configuration.
- **`core/`**: Main application logic (Models, Views, Admin).
- **`templates/`**: HTML files (migrated from `Templates/`).
- **`static/`**: CSS, JS, and Images.

## 🚀 How to Run

### 1. Database Setup
Ensure MySQL is running and execute:
```sql
CREATE DATABASE scholarcash_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'scholarcash_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON scholarcash_db.* TO 'scholarcash_user'@'localhost';
FLUSH PRIVILEGES;
```
*(Update [.env](file:///d:/New%20folder%20%283%29/Templates/.env) if you use different credentials)*

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Initialize Database
```bash
python manage.py makemigrations core
python manage.py migrate
```

### 4. Create Admin User
```bash
python manage.py createsuperuser
```

### 5. Start Server
```bash
python manage.py runserver
```

## ✅ what's Working in Backend
- **Models**: Users, Wallets, Transactions, and Inventory Items.
- **Views**:
    - `Login/Logout`: Session-based authentication.
    - `Student Dashboard`: Displays real wallet balance.
    - `Admin Panel`: Navigation links are hooked up.
- **Navigation**: Sidebar links now use dynamic Django routing.

## ⏭️ Next Steps
- Refactor templates to use a shared `base.html` layout.
- connect the "Buy" buttons in the shop to the [purchase_item](file:///d:/New%20folder%20%283%29/Templates/core/views.py#11-53) view.
