from pydantic import BaseModel
from datetime import datetime


class FoodOrderBase(BaseModel):
    food_id: int
    user_id: int
    quantity: int


class FoodOrderCreate(FoodOrderBase):
    pass


class FoodOrderUpdate(BaseModel):
    quantity: int


class FoodOrderInDB(FoodOrderBase):
    id: int
    created_at: datetime
    updated_at: datetime
    is_deleted: bool

    class Config:
        orm_mode = True


class FoodOrder(FoodOrderInDB):
    pass
