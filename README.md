# 💼 Backend Developer Portfolio – Built with Python & Flask

This is my personal portfolio project built to demonstrate real-world backend development skills using Python and Flask. The architecture follows clean coding principles, the MVC design pattern, and includes security features, automated testing, and structured logging. This project is part of my journey to land a backend developer role in the UK tech industry.

---

## 🚀 Demo

**Home Page:** Coming soon  
**Admin Panel:** Protected route for managing portfolio projects and viewing contact submissions

---

## ✨ Features

- ✅ **MVC Architecture** – Cleanly separated Models, Views, and Controllers
- 🔐 **Admin Authentication** – Secure login with password hashing using `bcrypt`
- 📁 **Project Management** – Full CRUD for adding and updating portfolio projects
- 📬 **Contact Form** – Users can send messages, stored securely in the database
- 🔐 **Security Best Practices** – Password hashing, session handling, `.env` secrets
- 🪵 **Structured Logging** – Logs with timestamps, file location, and rotation
- 🧪 **Automated Testing** – Unit and integration testing (WIP)
- 🔄 **REST API Ready** – Built with Flask routes, designed for future REST conversion

---

## 📦 Tech Stack

| Category       | Tech                                     |
|----------------|------------------------------------------|
| Backend        | Python, Flask                            |
| Database       | SQLite (easy to upgrade to PostgreSQL)   |
| Security       | bcrypt, flask session, python-dotenv     |
| Frontend (View)| HTML, CSS (Jinja templates)              |
| Testing        | `unittest` or `pytest` (in progress)     |
| Logging        | Python `logging` with rotating handler   |
| Version Control| Git + GitHub                             |

---

## 🗂 Folder Structure

```
portfolio/
├── app.py
├── controllers/              # Flask blueprints (routes)
├── models/                   # Business logic (classes)
├── views/                    # HTML templates (Jinja2)
├── static/                   # CSS/JS assets
├── database/                 # DB connection and schema
├── tests/                    # Unit/integration tests
├── logging_config.py         # Logging setup
├── .env                      # Secrets (not tracked)
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🧱 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/Yanis101k/My-Portfolio-.git portfolio
   cd portfolio
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` file**
   ```bash
   FLASK_SECRET_KEY=your-secret-key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

---

## 🧪 Run Tests

Tests coming soon...

```bash
pytest   # or python -m unittest
```

---

## 📈 Roadmap

- [x] Project scaffolding with Flask
- [x] Logging configuration with rotating file handler
- [x] Admin authentication (password hashing with bcrypt)
- [x] Project CRUD (create, read, update, delete)
- [x] Contact form
- [ ] Automated testing for all modules
- [ ] REST API conversion
- [ ] Dockerize for deployment
- [ ] Deploy to Render / Railway / Fly.io
- [ ] Add GitHub Actions for CI/CD

---

## 👨‍💻 Author

**Yanis Kaced**  
📍 Backend Developer based in London  
📫 [yaniskaced41@gmail.com](mailto:yaniskaced41@gmail.com)  
🌐 [GitHub Profile](https://github.com/Yanis101k)

---

## 🎯 Purpose

This portfolio project was created to demonstrate my backend development capabilities in a structured, secure, and production-ready way. It is part of my path toward landing a backend developer role in the UK, and showcases real-world software engineering principles including clean architecture, OOP, security, testing, and deployment readiness.

---

## 🛡️ License

This project is open source and free to use under the MIT License.
