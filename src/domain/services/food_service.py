from sqlalchemy.orm import Session
from domain.schemas import food_schemas
from repositories.food_repository import FoodRepository


class FoodService:
    def __init__(self, food_repository: FoodRepository):
        self.food_repository = food_repository

    def create_food(self, db: Session, food: food_schemas.FoodCreate):
        return self.food_repository.create_food(db, food)

    def get_food(self, db: Session, food_id: int):
        return self.food_repository.get_food(db, food_id)

    def get_foods(self, db: Session, skip: int = 0, limit: int = 100):
        return self.food_repository.get_foods(db, skip, limit)

    def update_food(self, db: Session, food_id: int, food: food_schemas.FoodUpdate):
        return self.food_repository.update_food(db, food_id, food)

    def delete_food(self, db: Session, food_id: int):
        return self.food_repository.delete_food(db, food_id)
