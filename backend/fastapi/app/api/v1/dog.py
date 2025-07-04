from fastapi import APIRouter, HTTPException, Depends
from typing import List, Dict

from app.schemas.dog import DogCreate, DogResponse, DogUpdate, DogAllResponse
from app.services.dog_service import DogService
from app.utils.logging import logger # Assuming logger exists as in bot.py

router = APIRouter(prefix="/dogs", tags=["dogs"])

@router.post("/", response_model=DogResponse)
async def create_dog_endpoint(dog: DogCreate):
    try:
        return await DogService.create_dog(dog)
    except Exception as e:
        logger.error(f"Dog creation error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=DogAllResponse)
async def get_all_dogs_endpoint():
    try:
        dogs = await DogService.get_all_dogs()
        return DogAllResponse(dogs=dogs, count=len(dogs))
    except Exception as e:
        logger.error(f"Error retrieving all dogs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{dog_id}", response_model=DogResponse)
async def get_dog_endpoint(dog_id: str):
    try:
        dog = await DogService.get_dog_by_id(dog_id)
        if dog is None:
            raise HTTPException(status_code=404, detail="Dog not found")
        return dog
    except ValueError as e:
        logger.error(f"Dog not found: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error retrieving dog: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{dog_id}", response_model=DogResponse)
async def update_dog_endpoint(dog_id: str, dog_update: DogUpdate):
    try:
        updated_dog = await DogService.update_dog(dog_id, dog_update)
        if updated_dog is None:
            raise HTTPException(status_code=404, detail="Dog not found for update")
        return updated_dog
    except ValueError as e:
        logger.error(f"Dog not found for update: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error updating dog: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{dog_id}", response_model=Dict[str, str])
async def delete_dog_endpoint(dog_id: str):
    try:
        result = await DogService.delete_dog(dog_id)
        if result is None: # Should be handled by ValueError in service
            raise HTTPException(status_code=404, detail="Dog not found for deletion")
        return result
    except ValueError as e:
        logger.error(f"Dog not found for deletion: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error deleting dog: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
