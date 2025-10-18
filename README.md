# BioTutor API

> **ALX Backend Engineering Capstone Project**  
> A RESTful API for managing biology education content aligned with Uganda's secondary school curriculum.

## 🌱 Overview

This project provides a structured backend for teachers to create and manage biology lessons, while students can securely access published content. It serves as the foundation for **BioTutor**, a future AI-powered educational platform for Ugandan students.

Built with **Django 4.2**, **Django REST Framework**, and **SQLite** (for development), this API follows REST conventions, role-based permissions, and clean URL design.

---

## ✅ Features Implemented (As of Week 3)

### 🔐 Authentication
- JWT-based authentication with access and refresh tokens
- User registration for both teachers and students
- Secure login endpoint
- Token-based authorization for protected routes

### 👥 User Management
- Custom `User` model with:
  - `role` (`teacher` or `student`)
  - `school` (e.g., "Kibuli SS")
  - `bio` (optional teacher bio)
  - Email validation
- Role-based permissions system
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
| `/api/auth/register/` | `POST` | Register new user (teacher/student) | Public |
| `/api/auth/login/` | `POST` | Get JWT token | Any active user |
| `/api/categories/` | `GET` | List all categories | Public |
| `/api/categories/{id}/` | `GET` | Retrieve one category | Public |
| `/api/categories/{id}/content/` | `GET` | List content in category | Public (published only) |
| `/api/content/` | `GET` | List content | Students: published only<br>Teachers: their own content |
| `/api/content/` | `POST` | Create new content | **Teachers only** |
| `/api/content/{id}/` | `GET` | Retrieve content | Public (published) / Teacher (own drafts) |
| `/api/content/{id}/` | `PUT`/`PATCH` | Update content | **Author only** |
| `/api/content/{id}/` | `DELETE` | Delete content | **Author only** |

### 🔍 Advanced Features
- **Filtering**:  
  - `?category=1` - Filter by category ID
  - `?author=1` - Filter by author ID
  - `?category__slug=cell-biology` - Filter by category slug
- **Search**:  
  `?search=mitochondria` (searches `title` and `content_body`)
- **Pagination & Ordering**:  
  Default: newest first (`?ordering=-created_at`)

### 🔒 Security & Permissions
- `IsTeacher`: Only teachers can create/edit content
- `IsAuthor`: Only the content author can update/delete
- Students **cannot** see unpublished (`is_published=False`) content
- JWT token expiration and refresh mechanism
- Password hashing with Django's built-in security

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 4.2, Django REST Framework
- **Authentication**: `djangorestframework-simplejwt`
- **Database**: SQLite (development) → PostgreSQL (production on PythonAnywhere)
- **Filtering**: `django-filter`
- **API Design**: RESTful, class-based views, serializers
- **URLs**: Clean, readable paths using Django's `path()` dispatcher

---

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- pip
- Virtual environment (recommended)

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
```

The API will be available at `http://127.0.0.1:8000/`

---

## 🧪 Testing the API

### Base URL (Development)
```
http://127.0.0.1:8000
```

### Authentication Flow

All authenticated endpoints require a JWT token in the Authorization header:
```
Authorization: Bearer <your_access_token>
```

---

### 1. Register a Teacher

**Endpoint:** `POST /api/auth/register/`

**Request:**
```http
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "username": "teacher1",
  "email": "trevour@biotutor.com",
  "password": "trevour256",
  "role": "teacher"
}
```

**Expected Response (201 Created):**
```json
{
  "id": 1,
  "username": "teacher1",
  "email": "trevour@biotutor.com",
  "role": "teacher",
  "school": null,
  "bio": null
}
```

---

### 2. Register a Student

**Endpoint:** `POST /api/auth/register/`

**Request:**
```http
POST http://127.0.0.1:8000/api/auth/register/
Content-Type: application/json

{
  "username": "student1",
  "email": "ali@biotutor.com",
  "password": "student@256!",
  "role": "student"
}
```

**Expected Response (201 Created):**
```json
{
  "id": 2,
  "username": "student1",
  "email": "ali@biotutor.com",
  "role": "student",
  "school": null,
  "bio": null
}
```

---

### 3. Login as Teacher

**Endpoint:** `POST /api/auth/login/`

**Request:**
```http
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username": "teacher1",
  "password": "trevour256"
}
```

**Expected Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**💡 Important:** Save the `access` token for authenticated requests!

---

### 4. Login as Student

**Endpoint:** `POST /api/auth/login/`

**Request:**
```http
POST http://127.0.0.1:8000/api/auth/login/
Content-Type: application/json

{
  "username": "student1",
  "password": "student@256!"
}
```

**Expected Response (200 OK):**
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

---

### 5. Get All Categories (Public)

**Endpoint:** `GET /api/categories/`

**Request:**
```http
GET http://127.0.0.1:8000/api/categories/
```

**Expected Response (200 OK):**
```json
[
  {
    "id": 1,
    "name": "Cell Biology",
    "slug": "cell-biology",
    "description": "Study of cells and their functions",
    "created_at": "2025-01-15T10:30:00Z"
  },
  {
    "id": 2,
    "name": "Ecology",
    "slug": "ecology",
    "description": "Study of organisms and their environment",
    "created_at": "2025-01-15T10:31:00Z"
  }
]
```

---

### 6. Get Content Under Category ID 1 (Public)

**Endpoint:** `GET /api/categories/{id}/content/`

**Request:**
```http
GET http://127.0.0.1:8000/api/categories/1/content/
```

**Expected Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Introduction to Cells",
    "slug": "introduction-to-cells",
    "summary": "Basic overview of cell structure and function",
    "content_body": "Cells are the basic unit of life...",
    "category": 1,
    "author": {
      "id": 1,
      "username": "teacher1"
    },
    "is_published": true,
    "created_at": "2025-01-16T09:00:00Z",
    "updated_at": "2025-01-16T09:00:00Z"
  }
]
```

---

### 7. List All Published Content (Public)

**Endpoint:** `GET /api/content/`

**Request:**
```http
GET http://127.0.0.1:8000/api/content/
```

**Expected Response (200 OK):**
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Introduction to Cells",
      "slug": "introduction-to-cells",
      "summary": "Basic overview of cell structure",
      "category": 1,
      "author": {
        "id": 1,
        "username": "teacher1"
      },
      "is_published": true,
      "created_at": "2025-01-16T09:00:00Z"
    }
  ]
}
```

---

### 8. Search Content by Keyword (Public)

**Endpoint:** `GET /api/content/?search={keyword}`

**Request:**
```http
GET http://127.0.0.1:8000/api/content/?search=cell
```

**Expected Response (200 OK):**
Returns all content where "cell" appears in the title or content_body.

---

### 9. Filter Content by Category Slug (Public)

**Endpoint:** `GET /api/content/?category__slug={slug}`

**Request:**
```http
GET http://127.0.0.1:8000/api/content/?category__slug=cell-biology
```

**Note:** Ensure a category with slug "cell-biology" exists in your database.

**Expected Response (200 OK):**
Returns all published content in the "Cell Biology" category.

---

### 10. Create New Biology Content (Teacher Only) 🔒

**Endpoint:** `POST /api/content/`

**Request:**
```http
POST http://127.0.0.1:8000/api/content/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "Mitochondria: The Powerhouse of the Cell",
  "slug": "mitochondria-the-powerhouse-of-the-cell",
  "summary": "Overview of mitochondrial structure and function in energy production.",
  "content_body": "Mitochondria are double-membrane organelles responsible for ATP production through cellular respiration. They contain their own DNA and replicate independently.",
  "category": 1,
  "is_published": true
}
```

**Expected Response (201 Created):**
```json
{
  "id": 3,
  "title": "Mitochondria: The Powerhouse of the Cell",
  "slug": "mitochondria-the-powerhouse-of-the-cell",
  "summary": "Overview of mitochondrial structure and function in energy production.",
  "content_body": "Mitochondria are double-membrane organelles responsible for ATP production through cellular respiration. They contain their own DNA and replicate independently.",
  "category": 1,
  "author": {
    "id": 1,
    "username": "teacher1",
    "email": "trevour@biotutor.com"
  },
  "is_published": true,
  "created_at": "2025-01-18T14:20:00Z",
  "updated_at": "2025-01-18T14:20:00Z"
}
```

**Error Response (403 Forbidden - if user is not a teacher):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 11. List Content as Authenticated Teacher 🔒

**Endpoint:** `GET /api/content/`

**Request:**
```http
GET http://127.0.0.1:8000/api/content/
Authorization: Bearer <your_access_token>
```

**Expected Response (200 OK):**
Shows all content authored by the authenticated teacher (both published and unpublished drafts).

---

### 12. Retrieve Specific Content by ID

**Endpoint:** `GET /api/content/{id}/`

**Request:**
```http
GET http://127.0.0.1:8000/api/content/1/
```

**Expected Response (200 OK):**
```json
{
  "id": 1,
  "title": "Introduction to Cells",
  "slug": "introduction-to-cells",
  "summary": "Basic overview of cell structure and function",
  "content_body": "Cells are the basic unit of life. They are the smallest units that can carry out all the processes of life...",
  "category": 1,
  "author": {
    "id": 1,
    "username": "teacher1",
    "email": "trevour@biotutor.com"
  },
  "is_published": true,
  "created_at": "2025-01-16T09:00:00Z",
  "updated_at": "2025-01-16T09:00:00Z"
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Not found."
}
```

---

### 13. Update Your Content (Teacher + Author Only) 🔒

**Endpoint:** `PUT /api/content/{id}/` or `PATCH /api/content/{id}/`

**Request:**
```http
PUT http://127.0.0.1:8000/api/content/3/
Authorization: Bearer <your_access_token>
Content-Type: application/json

{
  "title": "Mitochondria: Updated Overview",
  "slug": "mitochondria-updated-overview",
  "summary": "Updated details on oxidative phosphorylation",
  "content_body": "Updated details on oxidative phosphorylation and mitochondrial DNA inheritance. Mitochondria play a crucial role in cellular energy production through the electron transport chain.",
  "category": 1,
  "is_published": true
}
```

**Expected Response (200 OK):**
```json
{
  "id": 3,
  "title": "Mitochondria: Updated Overview",
  "slug": "mitochondria-updated-overview",
  "summary": "Updated details on oxidative phosphorylation",
  "content_body": "Updated details on oxidative phosphorylation and mitochondrial DNA inheritance. Mitochondria play a crucial role in cellular energy production through the electron transport chain.",
  "category": 1,
  "author": {
    "id": 1,
    "username": "teacher1"
  },
  "is_published": true,
  "created_at": "2025-01-18T14:20:00Z",
  "updated_at": "2025-01-18T15:30:00Z"
}
```

**Error Response (403 Forbidden - if not the author):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

### 14. Delete Your Content (Teacher + Author Only) 🔒

**Endpoint:** `DELETE /api/content/{id}/`

**Request:**
```http
DELETE http://127.0.0.1:8000/api/content/3/
Authorization: Bearer <your_access_token>
```

**Expected Response (204 No Content)**

No response body is returned on successful deletion.

**Error Response (403 Forbidden - if not the author):**
```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 📝 Using the API with Different Tools

### Using cURL

```bash
# Register a teacher
curl -X POST http://127.0.0.1:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"teacher1","email":"trevour@biotutor.com","password":"trevour256","role":"teacher"}'

# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"teacher1","password":"trevour256"}'

# Get all categories
curl http://127.0.0.1:8000/api/categories/

# Create content (replace YOUR_TOKEN with actual token)
curl -X POST http://127.0.0.1:8000/api/content/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Lesson","slug":"test-lesson","summary":"Test summary","content_body":"Test content","category":1,"is_published":true}'
```

---

### Using Postman

1. **Import requests** as a Postman collection
2. **Create environment variable** named `access_token`
3. **Login first** (Step 3 or 4) and copy the `access` token from response
4. **Set the variable**: Paste token into `access_token` environment variable
5. **Use in requests**: Add `{{access_token}}` in Authorization header as "Bearer Token"

**Setting up Authorization in Postman:**
- Go to the Authorization tab
- Select Type: "Bearer Token"
- Token: `{{access_token}}`

---

### Using Python Requests

```python
import requests

BASE_URL = "http://127.0.0.1:8000"

# 1. Register a teacher
register_data = {
    "username": "teacher1",
    "email": "trevour@biotutor.com",
    "password": "trevour256",
    "role": "teacher"
}
response = requests.post(f"{BASE_URL}/api/auth/register/", json=register_data)
print("Registration:", response.json())

# 2. Login
login_data = {
    "username": "teacher1",
    "password": "trevour256"
}
response = requests.post(f"{BASE_URL}/api/auth/login/", json=login_data)
tokens = response.json()
access_token = tokens['access']
print("Access Token:", access_token)

# 3. Set up headers with token
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}

# 4. Get all categories
response = requests.get(f"{BASE_URL}/api/categories/")
print("Categories:", response.json())

# 5. Create new content
content_data = {
    "title": "Photosynthesis Process",
    "slug": "photosynthesis-process",
    "summary": "Overview of photosynthesis in plants",
    "content_body": "Photosynthesis is the process by which plants convert light energy into chemical energy...",
    "category": 1,
    "is_published": True
}
response = requests.post(f"{BASE_URL}/api/content/", json=content_data, headers=headers)
print("New Content:", response.json())

# 6. Get all content
response = requests.get(f"{BASE_URL}/api/content/", headers=headers)
print("All Content:", response.json())

# 7. Search content
response = requests.get(f"{BASE_URL}/api/content/?search=photosynthesis")
print("Search Results:", response.json())
```

---

### Using JavaScript (Fetch API)

```javascript
const BASE_URL = "http://127.0.0.1:8000";

// Login and get token
async function login() {
  const response = await fetch(`${BASE_URL}/api/auth/login/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      username: 'teacher1',
      password: 'trevour256'
    })
  });
  const data = await response.json();
  return data.access;
}

// Create content
async function createContent(token) {
  const response = await fetch(`${BASE_URL}/api/content/`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: 'Cell Division',
      slug: 'cell-division',
      summary: 'Overview of mitosis and meiosis',
      content_body: 'Cell division is the process by which cells reproduce...',
      category: 1,
      is_published: true
    })
  });
  return await response.json();
}

// Use the functions
(async () => {
  const token = await login();
  console.log('Token:', token);
  
  const content = await createContent(token);
  console.log('Created Content:', content);
})();
```

---

## 📂 Project Structure

```
biotutor-api/
├── biotutor/                  # Main Django project config
│   ├── __init__.py
│   ├── settings.py            # Project settings
│   ├── urls.py                # Root URL configuration
│   ├── wsgi.py                # WSGI config for deployment
│   └── asgi.py                # ASGI config
│
├── api/               # Core API app
│   ├── migrations/            # Database migrations
│   ├── __init__.py
│   ├── models.py              # User, Category, BiologyContent models
│   ├── serializers.py         # DRF serializers
│   ├── views.py            # API views and viewsets
|   |__filters.py             
│   ├── permissions.py         # Custom permission classes (IsTeacher, IsAuthor)
│   ├── urls.py                # App-level URL routing
│   ├── admin.py               # Django admin configuration
│   ├── apps.py                # App configuration
│   └── tests.py               # Unit tests
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── db.sqlite3                 # SQLite database (development)
├── .gitignore                 # Git ignore file
└── README.md                  # This file
```


---

## 🧪 Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test api

# Run specific test class
python manage.py test api.tests.TestCategoryAPI

# Run with verbose output
python manage.py test --verbosity=2

# Run with coverage
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html  # Generate HTML report
```

---

## 🐛 Common Issues and Troubleshooting

### Issue: "Invalid token" error
**Solution:** 
- Ensure token is not expired
- Check that you're using the `access` token, not `refresh`
- Verify Authorization header format: `Bearer <token>`

### Issue: "Permission denied" when creating content
**Solution:**
- Verify user has `role='teacher'`
- Check that token is valid and not expired
- Ensure Authorization header is included

### Issue: Cannot see unpublished content
**Solution:**
- Unpublished content is only visible to:
  - The author (teacher who created it)
  - Not visible to students or other teachers


## 📊 API Response Codes

| Code | Status | Description |
|------|--------|-------------|
| 200 | OK | Request successful |
| 201 | Created | Resource created successfully |
| 204 | No Content | Resource deleted successfully |
| 400 | Bad Request | Invalid request data |
| 401 | Unauthorized | Missing or invalid authentication |
| 403 | Forbidden | No permission to access resource |
| 404 | Not Found | Resource not found |
| 500 | Internal Server Error | Server error |

---

## 🗓️ Project Roadmap

### ✅ Week 1-2: Foundation
- [x] Django project setup
- [x] Custom User model
- [x] Basic models (Category, BiologyContent)
- [x] Django Admin integration

### ✅ Week 3: API Development
- [x] JWT authentication
- [x] User registration endpoint
- [x] RESTful API endpoints
- [x] Permissions and filtering
- [x] Search functionality

### 🔄 Week 4: Testing & Frontend
- [ ] Comprehensive unit tests
- [ ] Student portal frontend (Bootstrap)
- [ ] Enhanced search & filtering
- [ ] User profile management
- [ ] API documentation with Swagger

### 🚀 Week 5: Deployment & Polish
- [ ] Final documentation
- [ ] Demo video

### What is Pending
- [ ] Deploy backend on PythonAnywhere
- [ ] Host static frontend
- [ ] Performance optimization

### 🔮 Future Enhancements
- [ ] AI-powered content recommendations
- [ ] Quiz and assessment system
- [ ] Progress tracking for students
- [ ] Mobile app (React Native)
- [ ] Real-time notifications
- [ ] File upload for images/diagrams
- [ ] Comment system on lessons

---

## 📖 API Documentation

For interactive API documentation:
- Swagger UI: `/api/docs/`
- ReDoc: `/api/redoc/`

---

## 🤝 Contributing

This is an ALX Capstone Project (individual work). However, feedback and suggestions are welcome!

If you'd like to contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is created for educational purposes as part of the ALX Backend Engineering program.

---

## 👨‍💻 Author

**Kiiza Trevour**  
- GitHub: [@KIIZA-TREVOUR](https://github.com/KIIZA-TREVOUR)
- Email: kiizatrevour@gmail.com
- Project: BioTutor API - ALX Backend Capstone
- Location: Gulu City, Uganda 🇺🇬

---

## 🙏 Acknowledgments

- **ALX Africa** for the Backend Engineering program
- **Django & DRF** communities for excellent documentation
- **Ugandan Secondary School Curriculum** for content inspiration
- All teachers and students who will benefit from this platform

---

## 📞 Support & Contact

For issues, questions, or suggestions:

1. **Check Documentation**: Review this README and Django REST Framework docs
2. **Common Issues**: See the Troubleshooting section above
3. **GitHub Issues**: Open an issue on the repository
4. **Email**: kiizatrevour@gmail.com

### Quick Help Checklist
- [ ] Are you using the correct endpoint URL?
- [ ] Is your JWT token valid and not expired?
- [ ] Do you have the correct permissions (teacher/student)?
- [ ] Is your request body formatted correctly as JSON?
- [ ] Are you including the Authorization header for protected routes?


**Built with ❤️ for Ugandan students learning biology**

---

### 🌟 Star This Project

If you find this project useful, please consider giving it a star on GitHub!

```bash
# Quick start command
git clone https://github.com/KIIZA-TREVOUR/biotutor-api && cd biotutor-api && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py migrate && python manage.py runserver
```

---

*Last Updated: October 2025*  
*Version: 3.0.0*
