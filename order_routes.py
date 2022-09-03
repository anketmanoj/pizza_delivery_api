from fastapi import APIRouter, Depends, HTTPException, status
from fastapi_jwt_auth import AuthJWT
from database import SessionLocal, get_db
from models import Users, Orders
from schema import OrderModel
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(
    prefix="/orders",
    tags=['Orders']
)

@order_router.post("/", status_code= status.HTTP_201_CREATED)
async def place_order(order: OrderModel, Authorize: AuthJWT = Depends(), db: SessionLocal = Depends(get_db)):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not authorized")

    current_user = Authorize.get_jwt_subject()
    user = db.query(Users).filter(Users.username == current_user).first()

    new_order = Orders(
        pizza_size= order.pizza_size,
        quantity=order.quantity,
    )

    new_order.users = user

    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return new_order




    
        
    
    