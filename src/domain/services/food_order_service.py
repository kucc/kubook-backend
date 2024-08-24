from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repositories.models import FoodOrder
from domain.services import food_order_service
from domain.schemas import food_order_schemas


def get_food_order(db: Session, order_id: int):
    order = db.query(FoodOrder).filter(FoodOrder.id == order_id, FoodOrder.is_deleted == False).first()
    if not order:
        raise HTTPException(status_code=404, detail="Food order not found")
    return order


def get_food_orders(db: Session, skip: int = 0, limit: int = 100):
    return db.query(FoodOrder).filter(FoodOrder.is_deleted == False).offset(skip).limit(limit).all()


def create_food_order(db: Session, order: food_order_schemas.FoodOrderCreate):
    db_order = FoodOrder(**order.dict(), created_at=datetime.utcnow(), updated_at=datetime.utcnow())
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def update_food_order(db: Session, order_id: int, order: food_order_schemas.FoodOrderUpdate):
    db_order = get_food_order(db, order_id)
    update_data = order.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_order, key, value)
    db_order.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_order)
    return db_order


def delete_food_order(db: Session, order_id: int):
    db_order = get_food_order(db, order_id)
    db_order.is_deleted = True
    db_order.updated_at = datetime.utcnow()
    db.commit()
    return db_order
