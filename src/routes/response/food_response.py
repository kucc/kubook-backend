from datetime import datetime

from pydantic import BaseModel


class FoodResponse(BaseModel):
    id: int
    food_name: str
    food_type: str
    food_price: int
    food_description: str
    food_image_url: str
    created_at: datetime
    updated_at: datetime
