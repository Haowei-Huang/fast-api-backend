Feel free to read the [Deep Wiki](https://deepwiki.com/Haowei-Huang/fast-api-backend) generated for this project

# FastAPI Backend for Simplibook

This project is a FastAPI backend for the **Simplibook** hotel booking application. It supports features like user registration, login, hotel search, room booking, and admin management.

## System Architecture

![highlevel architecture](https://github.com/user-attachments/assets/05617d65-563e-4d67-a901-7782ab7938f7)

## 🏗️ Tech Stack

### Core Framework and Libraries
- **FastAPI:**: Primary web framework providing automatic API documentation, request/response validation, and dependency injection
- **Pydantic**: Data validation and serialization for all request/response models
- **MongoDB**: Primary database with async driver support through Motor
- **JWT**: Token-based authentication with RS256 algorithm support
- **bcrypt**: Password hashing for secure credential storage

### Infrastructure Components
- **Database Connection Management:** Centralized through DatabaseManager class with connection pooling
- **Configuration Management:** Environment-based configuration through Settings and AuthSettings classes
- **Dependency Injection:** Service and repository instances provided through a centralized dependency injection system
- **Exception Handling:** Structured error responses with custom exception hierarchy

## ⚙️ Features

- 🧑 **User Management**
  - Registration, login, profile editing
  - Role-based access control with JWT authentication

- 🏨 **Hotel and Room Management**
  - Search accommodations
  - Filter by city, availability, price, etc.
  - Book and cancel rooms

- 🛡️ **Admin Dashboard**
  - Manage users, rooms, bookings
  - View analytics

- 🔐 **Security**
  - Password hashing with `bcrypt`
  - Token-based authentication

## 🗂️ Request Processing Flow

![request_flow](https://github.com/user-attachments/assets/e012e690-77cd-49af-b358-f9cc3eb7ea08)

## 🚀 Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/Haowei-Huang/fast-api-backend.git
cd fast-api-backend
```

### 2. Install dependencies

You can follow the instructions provided by FAST API to create a virtual environment and install the packages: [virtual-environments](https://fastapi.tiangolo.com/virtual-environments/#__tabbed_2_3)

### 2. Set up environment variables

Create a `.env` file:

```env
DB_TYPE=mongodb
DB_NAME=FAST-API
DB_URL=mongodburl

ACCESS_PRIVATE_KEY="your base 64 key" 
ACCESS_PUBLIC_KEY="your base 64 key" 
REFRESH_PRIVATE_KEY="your base 64 key" 
REFRESH_PUBLIC_KEY="your base 64 key" 
FRONTEND_URL=http://localhost:3000
ALGORITHM=RS256
CORS_ORIGINS=["http://localhost:8000"]
```

### 3. Run the app

```bash
uvicorn main:app --reload
```

## 📫 Contact

Maintained by [Haowei Huang](https://github.com/Haowei-Huang).

---

> This documentation was generated with help from [DeepWiki](https://deepwiki.com).
