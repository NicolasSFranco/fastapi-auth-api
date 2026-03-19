from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from fastapi import FastAPI
from datetime import datetime, timedelta
from jose import jwt
from app.database.connection import SessionLocal, engine
from app.database.models import Base, User
from app.core.security import hash_password, verify_password
from app.database.models import User


app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "API rodando"}


@app.post("/register")
def register(email: str, password: str):
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == email).first()

        if existing_user:
            return {"error": "Usuário já existe"}

        print(">>> tentando criar usuário:", email)

        hashed = hash_password(password)

        user = User(email=email, password=hashed)
        db.add(user)
        db.commit()
        db.refresh(user)

        print(">>> usuário criado com ID:", user.id)

        return {"id": user.id, "email": user.email}
    finally:
        db.close()

SECRET_KEY = "segredo123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme)):
    db = SessionLocal()
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        user = db.query(User).filter(User.email == email).first()

        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")
    finally:
        db.close()

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")

        if email is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        return email

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == form_data.username).first()

        if not user:
            raise HTTPException(status_code=401, detail="Usuário não encontrado")

        if not verify_password(form_data.password, user.password):
            raise HTTPException(status_code=401, detail="Senha incorreta")

        access_token = create_access_token(data={"sub": user.email})

        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
    finally:
        db.close()

@app.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "email": current_user.email
    }

# uvicorn app.main:app --reload
# código pra rodar a API

