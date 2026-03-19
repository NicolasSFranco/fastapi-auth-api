FastAPI Auth API

API de autenticação desenvolvida com FastAPI, usando JWT para login e rotas protegidas.

🚀 Funcionalidades

- Registro de usuário
- Login com autenticação JWT
- Rota protegida (`/me`)
- Hash de senha com bcrypt

🛠️ Tecnologias

- FastAPI
- SQLite
- Uvicorn
- Passlib (bcrypt)

🔐 Endpoints

- POST /register
- POST /login
- GET /me (protegido)

📚 Docs

http://127.0.0.1:8000/docs

▶️ Como rodar o projeto

```bash
uvicorn app.main:app --reload
