from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token
from app.models.models import Admin
from app.schemas.schemas import AdminCreate, Token, AdminOut

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    admin = db.query(Admin).filter(Admin.username == username).first()
    if admin is None or not admin.is_active:
        raise credentials_exception

    return admin


@router.post("/register", response_model=AdminOut)
def register_admin(admin: AdminCreate, db: Session = Depends(get_db)):
    # Check if any admin exists — only allow first registration freely
    existing_count = db.query(Admin).count()
    if existing_count > 0:
        raise HTTPException(
            status_code=403,
            detail="Admin registration is closed. Contact the system owner.",
        )

    existing = db.query(Admin).filter(
        (Admin.username == admin.username) | (Admin.email == admin.email)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    hashed = get_password_hash(admin.password)
    db_admin = Admin(
        username=admin.username,
        email=admin.email,
        hashed_password=hashed,
    )
    db.add(db_admin)
    db.commit()
    db.refresh(db_admin)
    return db_admin


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    admin = db.query(Admin).filter(Admin.username == form_data.username).first()
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=AdminOut)
def get_me(current_admin: Admin = Depends(get_current_admin)):
    return current_admin
