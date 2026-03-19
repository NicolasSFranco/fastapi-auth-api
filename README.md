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

▶️ Como rodar o projeto

```bash
uvicorn app.main:app --reload
