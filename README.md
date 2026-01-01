# NuraPropertyAPI 🏠🇳🇬

> An API-first Real Estate Marketplace Backend built for the Nigerian market.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Django](https://img.shields.io/badge/Django-5.0-green)
![DRF](https://img.shields.io/badge/DRF-3.14-red)
![License](https://img.shields.io/badge/License-MIT-yellow)

**NuraPropertyAPI** is a robust, scalable backend system designed to power modern real estate applications (Web & Mobile). It connects Agents, Buyers, and Admins through a secure, feature-rich API interface tailored for the Nigerian real estate sector.

---

## 🚀 Key Features

* **🔐 Advanced Authentication:** Custom User model (Email login), JWT Tokens, and Role-Based Access Control (Admin, Agent, Customer).
* **🏘️ Property Management:** Create, update, and manage listings with support for Nigerian currency (₦) and local address structures.
* **🖼️ Media Handling:** Multi-image uploads and gallery management for properties.
* **🔎 Search & Discovery:** Advanced filtering (Price range, Location, Bedrooms) and Saved Search functionality.
* **📅 Interactions:** Inspection scheduling, internal messaging system, and admin announcements.
* **💸 Finance Ledger:** Offline payment recording, transaction verification, and deal closures with commission tracking.
* **📊 Analytics:** Admin KPIs and Agent performance reports.
* **📚 Documentation:** Auto-generated Swagger and ReDoc documentation.

---

## 🛠️ Tech Stack

* **Framework:** Django & Django REST Framework
* **Database:** SQLite3 (Dev) / PostgreSQL (Prod)
* **Auth:** Djoser + SimpleJWT
* **Docs:** drf-spectacular (OpenAPI 3.0)
* **Utilities:** Django-Filter, Pillow, Cors-Headers

---

## ⚙️ Installation & Setup

Follow these steps to run the project locally.

### 1. Clone the repository
```bash
git clone [https://github.com/nuramustaphaali/NuraPropertyAPI.git](https://github.com/nuramustaphaali/NuraPropertyAPI.git)
cd NuraPropertyAPI
```

### 2. Create a Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser
```bash
python manage.py createsuperuser
```

### 6. Run the Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to see the **API Manual**.

---

## 📖 API Documentation

The API is fully documented. Once the server is running, visit:

* **Swagger UI:** `http://127.0.0.1:8000/api/docs/` (Best for testing)
* **ReDoc:** `http://127.0.0.1:8000/api/redoc/` (Best for reading)
* **Manual:** `http://127.0.0.1:8000/` (Quick Reference)

---

## 📂 Project Structure

```text
NuraPropertyAPI/
├── config/             # Project settings & URL configuration
├── apps/
│   ├── common/         # Shared utilities & Base models
│   ├── users/          # Auth & Custom User Model
│   ├── profiles/       # Agent & Customer Profiles
│   ├── properties/     # Listings, Search, & Media
│   ├── interactions/   # Messaging & Inspections
│   └── finance/        # Ledger, Deals & Analytics
├── media/              # User uploads (Images)
├── manage.py
└── db.sqlite3
```

## 🤝 Contact

**Maintainer:** Nura Mustapha Ali
**GitHub:** [nuramustaphaali](https://github.com/nuramustaphaali)
**WhatsApp:** [+2349164601810](https://wa.me/2349164601810)
**Email:** [nuramustali@gmail.com](mailto:nuramustali@gmail.com)