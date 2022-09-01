from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import SessionLocal, get_db
from schema import SignUpModel
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash

auth_router = APIRouter(
    prefix="/auth",
    tags=['Auth']
)

@auth_router.post("/signup", response_model=SignUpModel)
async def sign_up_user(user: SignUpModel, response: Response, db: SessionLocal = Depends(get_db)):
    checkUserEmail = db.query(Users).filter(Users.email == user.email).first()
    if checkUserEmail:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f"User with email: {user.email} already exists")

    checkUserName = db.query(Users).filter(Users.username == user.username).first()
    if checkUserName:
        raise HTTPException(status_code=status.HTTP_302_FOUND, detail=f"User with username: {user.username} already exists")
    
    new_user = Users(
        username = user.username,
        email = user.email,
        password = generate_password_hash(user.password),
        is_staff = user.is_staff,
        is_active = user.is_active,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    response.status_code = status.HTTP_201_CREATED
    return new_user
    


