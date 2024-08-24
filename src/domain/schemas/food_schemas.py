from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class FoodBase(BaseModel):
    food_name: str
    food_type: str
    food_price: int
    food_description: str
    food_image_url: Optional[str] = None


class FoodCreate(FoodBase):
    pass


class FoodUpdate(BaseModel):
    food_name: Optional[str] = None
    food_type: Optional[str] = None
    food_price: Optional[int] = None
    food_description: Optional[str] = None
    food_image_url: Optional[str] = None


class FoodInDB(FoodBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Food(FoodInDB):
    pass
