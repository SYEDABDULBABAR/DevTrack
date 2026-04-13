# 🚀 DevTrack API - Project Management System

DevTrack aik professional **Project & Task Management API** hai jo FastAPI, SQLModel, aur PostgreSQL ke saath banayi gayi hai. Ismein complete User Authentication (JWT) aur Role-based Access Control shamil hai taake users apne projects aur tasks ko secure tareeqe se manage kar sakein.

## ✨ Key Features
* **Secure Auth:** JWT based Login/Register with Password Hashing (bcrypt).
* **Project Management:** Create, Update, aur Delete projects (Owner-only access).
* **Task System:** Tasks link hote hain projects se, jahan status aur priority set ki ja sakti hai.
* **Comments System:** Threaded comments for every task for team discussion.
* **Security:** Strict authorization checks—sirf project owner hi data modify kar sakta hai.

## 🛠️ Tech Stack
* **Framework:** [FastAPI](https://fastapi.tiangolo.com/)
* **Database/ORM:** [SQLModel](https://sqlmodel.tiangolo.com/) (PostgreSQL)
* **Env Management:** [uv](https://github.com/astral-sh/uv)
* **Security:** Passlib (Bcrypt), PyJWT

## 🚀 Installation & Setup

1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/your-username/devtrack.git](https://github.com/your-username/devtrack.git)
   cd devtrack