from typing import List, Dict, Optional
import uuid

from fastapi import HTTPException

from app.schemas.dog import DogCreate, DogResponse, DogUpdate

# In-memory storage for dogs
db_dogs: Dict[str, Dict] = {}

class DogService:
    @staticmethod
    async def create_dog(dog_data: DogCreate) -> DogResponse:
        dog_id = str(uuid.uuid4())
        dog = dog_data.model_dump()
        dog["id"] = dog_id
        db_dogs[dog_id] = dog
        return DogResponse(**dog)

    @staticmethod
    async def get_all_dogs() -> List[DogResponse]:
        return [DogResponse(**dog) for dog in db_dogs.values()]

    @staticmethod
    async def get_dog_by_id(dog_id: str) -> Optional[DogResponse]:
        dog = db_dogs.get(dog_id)
        if not dog:
            raise ValueError("Dog not found")
        return DogResponse(**dog)

    @staticmethod
    async def update_dog(dog_id: str, dog_data: DogUpdate) -> Optional[DogResponse]:
        if dog_id not in db_dogs:
            raise ValueError("Dog not found")

        update_data = dog_data.model_dump(exclude_unset=True)
        db_dogs[dog_id].update(update_data)
        return DogResponse(**db_dogs[dog_id])

    @staticmethod
    async def delete_dog(dog_id: str) -> Optional[Dict]:
        if dog_id not in db_dogs:
            raise ValueError("Dog not found")
        del db_dogs[dog_id]
        return {"message": "Dog deleted successfully"}
