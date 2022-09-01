from fastapi import APIRouter, Depends, HTTPException, status, Response
from database import SessionLocal, get_db
from schema import SignUpModel, LoginUser
from models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from fastapi.encoders import jsonable_encoder

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

@auth_router.post("/login", status_code=status.HTTP_200_OK)
async def login_user(loginUser: LoginUser, Authorize: AuthJWT = Depends(), db: SessionLocal = Depends(get_db)):
    user = db.query(Users).filter(Users.username == loginUser.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with username: {user.username} does not exist")
    
    if not check_password_hash(user.password, loginUser.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Incorrect Credentials")

    access_token = Authorize.create_access_token(subject=user.username)
    refresh_token = Authorize.create_refresh_token(subject=user.username)

    response = {
        "access_token" : access_token,
        "refresh_token" : refresh_token
    }

    return jsonable_encoder(response)
    


