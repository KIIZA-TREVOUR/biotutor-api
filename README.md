# BioTutor API

> **ALX Backend Engineering Capstone Project – Week 3 of 5**  
> A RESTful API for managing biology education content aligned with Uganda’s secondary school curriculum.

## 🌱 Overview

This project provides a structured backend for teachers to create and manage biology lessons, while students can securely access published content. It serves as the foundation for **BioTutor**, a future AI-powered educational platform for Ugandan students.

Built with **Django 4.2**, **Django REST Framework**, and **SQLite** (for development), this API follows REST conventions, role-based permissions, and clean URL design.

---

## ✅ Features Implemented (As of Week 3)

### 🔐 Authentication
- JWT-based login via `POST /api/auth/login/`
- Secure token issuance (`access` + `refresh`)
- Works for both **teachers** and **students**

### 👥 User Management
- Custom `User` model with:
  - `role` (`teacher` or `student`)
  - `school` (e.g., "Kibuli SS")
  - `bio` (optional teacher bio)
- Fully integrated with Django Admin

### 📚 Content Models
- **`Category`**: Biology topics (e.g., "Cells", "Ecology")
  - Fields: `name`, `slug`, `description`, `created_at`
- **`BiologyContent`**: Full lessons/notes
  - Fields: `title`, `slug`, `summary`, `content_body`, `is_published`, `author`, `category`
  - Linked to `User` (author) and `Category`

### 🌐 RESTful API Endpoints

| Endpoint | Method | Description | Permissions |
|--------|--------|-------------|-------------|
| `/api/auth/login/` | `POST` | Get JWT token | Any active user |
| `/api/categories/` | `GET` | List all categories | Public (no auth needed) |
| `/api/categories/{id}/` | `GET` | Retrieve one category | Public |
| `/api/content/` | `GET` | List content | Students: published only<br>Teachers: their own content |
| `/api/content/` | `POST` | Create new content | **Teachers only** |
| `/api/content/{id}/` | `GET` | Retrieve content | Public (published) / Teacher (own drafts) |
| `/api/content/{id}/` | `PUT`/`PATCH` | Update content | **Author only** |
| `/api/content/{id}/` | `DELETE` | Delete content | **Author only** |

### 🔍 Advanced Features
- **Filtering**:  
  `?category=cells`, `?author=1`
- **Search**:  
  `?search=mitochondria` (searches `title` and `content_body`)
- **Pagination & Ordering**:  
  Default: newest first (`?ordering=-created_at`)

### 🔒 Security & Permissions
- `IsTeacher`: Only teachers can create/edit content
- `IsAuthor`: Only the content author can update/delete
- Students **cannot** see unpublished (`is_published=False`) content

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 4.2, Django REST Framework
- **Authentication**: `djangorestframework-simplejwt`
- **Database**: SQLite (development)
- **Filtering**: `django-filter`
- **API Design**: RESTful, class-based views, serializers
- **URLs**: Clean, readable paths using Django’s `path()` dispatcher

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12
- pip

### Installation
```bash
# Clone the repo
git clone https://github.com/KIIZA-TREVOUR/biotutor-api
cd biotutor-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (optional, for admin access)
python manage.py createsuperuser

# Start the server
python manage.py runserver

Test the API
Use Postman or curl to:

Log in:
POST /api/auth/login/ with { "username": "...", "password": "..." }
Create content (as teacher):
Include Authorization: Bearer <token> header
Browse content (as student or teacher)
💡 Add test categories and users via Django Admin at http://127.0.0.1:8000/admin/ 

```
# 📂 Project Structure
```
biotutor-api/
├── biotutor/               # Main Django project config
├── biology_api/            # Core app
│   ├── models.py           # User, Category, BiologyContent
│   ├── serializers.py      # CategorySerializer, BiologyContentSerializer
│   ├── views.py            # API views with permissions
│   ├── permissions.py      # IsTeacher, IsAuthor
│   └── urls.py             # App-level routes
├── manage.py
├── requirements.txt
└── README.md
```
# 🗓️ Roadmap
## Week 4:
- Unit tests
- Student portal frontend (Bootstrap)
- Enhanced search & filtering
## Week 5:
- Deploy backend on PythonAnywhere
- Host static frontend
- Final demo video
🤝 Contributing
This is an ALX Capstone Project (individual work). However, feedback is welcome!