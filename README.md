# Task Manager API
A REST API for managing tasks with user authentication.

## Tech Stack

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication

## Features

- User registration
- User login
- JWT authentication
- Create tasks
- List tasks
- Update tasks
- Delete tasks
- User-based access control

## Installation

```bash
git clone https://github.com/ioneli/task-manager-api
cd task-manager-api
pip install -r requirements.txt
uvicorn app.main:app --reload 
```
API Documentation
Swagger UI available at:


http://localhost:8000/docs
Example Request
Create task:
```
JSON
{
 "title": "Learn FastAPI",
 "description": "build backend project"
}
```
