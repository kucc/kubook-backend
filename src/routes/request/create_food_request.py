from pydantic import BaseModel


class CreateFoodRequest(BaseModel):
    food_name: str
    food_type: str
    food_price: int
    food_description: str
    food_image_url: str
