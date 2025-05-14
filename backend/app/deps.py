from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from .models import User
from .database import SessionLocal
from .security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    print(f"[DEBUG] Incoming token: {token}")

    try:
        print(f"[DEBUG] payload start")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"[DEBUG] Decoded payload: {payload}")

        # Извлекаем user_id из поля 'sub'
        user_id = payload.get("sub")

        # Проверка, если 'sub' не существует в токене
        if user_id is None:
            raise HTTPException(status_code=403, detail="Token is missing 'sub' field")

        # Если 'sub' не строка, пытаемся преобразовать в строку
        if not isinstance(user_id, str):
            user_id = str(user_id)

        print(f"[DEBUG] Extracted user_id: {user_id}")

        # Преобразуем user_id в целое число
        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(status_code=403, detail="Invalid user_id in token")

    except JWTError as e:
        print(f"[ERROR] JWT decode error: {e}")
        raise HTTPException(status_code=403, detail="Неверный токен")

    # Поиск пользователя в базе данных
    user = db.query(User).filter(User.id == user_id).first()
    print(f"[DEBUG] DB user found: {user}")

    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")

    return user

def is_admin(current_user: User = Depends(get_current_user)):
    if current_user.role.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user