# 🌟 HBnB - Part 3: Authentication & Database Integration  

## 🔥 Main Objectives  
✅ Secure the API with **JWT (JSON Web Token)**  
✅ Implement **role-based access control (admin/user)**  
✅ Switch from in-memory storage to **SQLite (dev) / MySQL (prod)**  
✅ Ensure data persistence using **SQLAlchemy**  
✅ Design a **clear database schema** with **mermaid.js**  

---  

## 🏗️ Project Structure  
```bash
hbnb-3/
├── app/
│   ├── __init__.py         # App initialization
│   ├── api/
│   │   ├── v1/             # API endpoints
│   │   │   ├── auth.py     # JWT authentication
│   │   │   ├── users.py    # User management
│   │   │   ├── places.py   # Places management
│   │   │   ├── reviews.py  # Reviews management
│   │   │   └── amenities.py # Amenities management
│   ├── models/             # SQLAlchemy models
│   │   ├── base_model.py   # Base model
│   │   ├── user.py         # User model
│   │   ├── place.py        # Place model
│   │   ├── review.py       # Review model
│   │   └── amenity.py      # Amenity model
│   ├── security/           # API security
│   │   ├── jwt_manager.py  # JWT token handling
│   │   ├── password_utils.py # Password hashing
│   └── db/                 # Database
│       ├── setup.py        # SQLite / MySQL setup
│       ├── migrations/     # SQLAlchemy migrations
├── config.py               # Environment configurations
├── run.py                  # Start the application
└── requirements.txt        # Dependencies
```  

---  

## 🚀 Installation & Setup  

1️⃣ **Create a virtual environment**  
```bash
python3 -m venv env
source env/bin/activate  # (Windows: env\Scripts\activate)
```  

2️⃣ **Install dependencies**  
```bash
pip install -r requirements.txt
```  

3️⃣ **Run the application**  
```bash
python3 run.py
```  
🔗 API available at `http://127.0.0.1:5000`  

---  

## 🔑 JWT Authentication  
📌 **Login Process:**  

1. **Register a new user** (`/api/v1/auth/register`)  
2. **Login** (`/api/v1/auth/login`) → Get a **JWT token**  
3. **Use this token** to access protected endpoints  

🛡️ **Example JWT usage**:  
```http
GET /api/v1/users/
Authorization: Bearer <your_token_here>
```  

---  

## 🛢️ Database: SQLite (Dev) → MySQL (Prod)  
📌 **Switching between databases**  

1️⃣ **Development Mode (SQLite)**  
```python
SQLALCHEMY_DATABASE_URI = 'sqlite:///hbnb_dev.db'
```  

2️⃣ **Production Mode (MySQL)**  
```python
SQLALCHEMY_DATABASE_URI = 'mysql://user:password@localhost/hbnb_prod'
```  

📌 **Apply migrations**  
```bash
flask db init    # Initialize
flask db migrate # Generate migrations
flask db upgrade # Apply changes
```  

---  

## 📊 Database Schema  

```mermaid
erDiagram
    USER {
        string id PK
        string first_name
        string last_name
        string email UNIQUE
        string password_hash
        boolean is_admin
    }
    
    PLACE {
        string id PK
        string title
        float price
        float latitude
        float longitude
        string user_id FK
    }
    
    REVIEW {
        string id PK
        string text
        int rating
        string user_id FK
        string place_id FK
    }
    
    AMENITY {
        string id PK
        string name
    }
    
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : receives
    PLACE ||--o{ AMENITY : has
```  

---  

## ✅ Validation Rules  

### **User Model**  
✔️ **Unique & valid email**  
✔️ **Password hashed** (bcrypt)  

### **Place Model**  
✔️ **Price must be positive**  
✔️ **Valid latitude & longitude**  

### **Review Model**  
✔️ **Text is required**  
✔️ **Rating must be between 1 and 5**  

---  

## 🔍 Testing the API  

📌 **Test with `curl`**  
```bash
curl -X POST http://127.0.0.1:5000/api/v1/auth/login -d '{"email":"test@example.com", "password":"1234"}' -H "Content-Type: application/json"
```  

📌 **Test with Postman**  
1. Import API routes  
2. Add **JWT token** in **Authorization**  
3. Test **GET / POST / PUT / DELETE** requests  

---  

