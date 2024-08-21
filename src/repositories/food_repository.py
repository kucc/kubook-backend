from sqlalchemy.orm import Session
from sqlalchemy.future import select
from repositories import models
from domain.schemas import food_schemas


class FoodRepository:
    def create_food(self, db: Session, food: food_schemas.FoodCreate):
        db_food = models.Food(**food.model_dump())
        db.add(db_food)
        db.commit()
        db.refresh(db_food)
        return db_food

    def get_food(self, db: Session, food_id: int):
        return db.query(models.Food).filter(models.Food.id == food_id).first()

    def get_foods(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Food).offset(skip).limit(limit).all()

    def update_food(self, db: Session, food_id: int, food: food_schemas.FoodUpdate):
        db_food = db.query(models.Food).filter(models.Food.id == food_id).first()
        if db_food:
            for key, value in food.dict(exclude_unset=True).items():
                setattr(db_food, key, value)
            db.commit()
            db.refresh(db_food)
        return db_food

    def delete_food(self, db: Session, food_id: int):
        db_food = db.query(models.Food).filter(models.Food.id == food_id).first()
        if db_food:
            db.delete(db_food)
            db.commit()
        return db_food
