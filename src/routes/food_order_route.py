from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from domain.schemas import food_schemas, food_order_schemas
from domain.services import food_order_service
from dependencies import get_db

router = APIRouter(
    prefix="/food-orders",
    tags=["food-orders"]
)


@router.post("/food-orders/", response_model=food_order_schemas.FoodOrder)
def create_food_order(order: food_order_schemas.FoodOrderCreate, db: Session = Depends(get_db)):
    return food_order_service.create_food_order(db=db, order=order)


@router.get("/food-orders/", response_model=List[food_order_schemas.FoodOrder])
def read_food_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    orders = food_order_service.get_food_orders(db, skip=skip, limit=limit)
    return orders


@router.get("/food-orders/{order_id}", response_model=food_order_schemas.FoodOrder)
def read_food_order(order_id: int, db: Session = Depends(get_db)):
    order = food_order_service.get_food_order(db, order_id=order_id)
    return order


@router.put("/food-orders/{order_id}", response_model=food_order_schemas.FoodOrder)
def update_food_order(order_id: int, order: food_order_schemas.FoodOrderUpdate, db: Session = Depends(get_db)):
    return food_order_service.update_food_order(db=db, order_id=order_id, order=order)


@router.delete("/food-orders/{order_id}", response_model=food_order_schemas.FoodOrder)
def delete_food_order(order_id: int, db: Session = Depends(get_db)):
    return food_order_service.delete_food_order(db=db, order_id=order_id)
