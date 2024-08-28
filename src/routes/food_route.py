from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from dependencies import get_db
from domain.schemas import food_schemas
from domain.services.food_service import FoodService
from repositories.food_repository import FoodRepository
from dependencies import get_current_active_user

router = APIRouter(
    prefix="/food",
    tags=["food"]
)


food_repository = FoodRepository()
food_service = FoodService(food_repository)


@router.post("", response_model=food_schemas.Food)
def create_food(
    food: food_schemas.FoodCreate,
    db: Session = Depends(get_db),
    get_current_active_user=Depends(get_current_active_user)
):
    print(get_current_active_user)
    return food_service.create_food(db, food)


@ router.get("/foods/", response_model=List[food_schemas.Food])
def read_foods(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    foods = food_service.get_foods(db, skip=skip, limit=limit)
    return foods


@ router.get("/foods/{food_id}", response_model=food_schemas.Food)
def read_food(food_id: int, db: Session = Depends(get_db)):
    food = food_service.get_food(db, food_id=food_id)
    if food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return food


@ router.put("/foods/{food_id}", response_model=food_schemas.Food)
def update_food(food_id: int, food: food_schemas.FoodUpdate, db: Session = Depends(get_db)):
    updated_food = food_service.update_food(db, food_id=food_id, food=food)
    if updated_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return updated_food


@ router.delete("/foods/{food_id}", response_model=food_schemas.Food)
def delete_food(food_id: int, db: Session = Depends(get_db)):
    deleted_food = food_service.delete_food(db, food_id=food_id)
    if deleted_food is None:
        raise HTTPException(status_code=404, detail="Food not found")
    return deleted_food
