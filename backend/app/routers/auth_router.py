from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from .. import schemas, models, auth
from ..database import get_db

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/register", response_model=schemas.Token)
def register(u: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == u.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    user = models.User(
        email=u.email,
        hashed_password=auth.get_password_hash(u.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # ⭐ FIX — convert user.id to string
    token = auth.create_access_token(
        {"sub": str(user.id)},
        timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return schemas.Token(access_token=token)

@router.post("/login", response_model=schemas.Token)
def login(u: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == u.email).first()
    if not user or not auth.verify_password(u.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ⭐ FIX — convert user.id to string
    token = auth.create_access_token(
        {"sub": str(user.id)},
        timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return schemas.Token(access_token=token)
