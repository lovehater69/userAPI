from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from app.db.mongodb import mongo_db
from app.model.user import User

router = APIRouter()
@router.get("/ping")
async def ping():
    try:
        mongo_db.client.server_info()  # Check if the MongoDB server is available
        return {"status": "Database connection OK"}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection error")
    
@router.get("/users/{user_id}")
async def get_user(user_id: str):
    user = mongo_db.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        return user
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.post("/create_user/")
async def create_user(user: User):
    user_dict = user.dict()
    result = mongo_db.db.users.insert_one(user_dict)
    return {"id": str(result.inserted_id)}

@router.put("/update_user/{user_id}")
async def update_user(user_id: str, user: User):
    user_dict = user.dict()
    result = mongo_db.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": user_dict})
    if result.modified_count == 1:
        return {"message": "User updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.delete("/delete_user/{user_id}")
async def delete_user(user_id: str):
    result = mongo_db.db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 1:
        return {"message": "User deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="User not found")

@router.get("/users/list_users")
async def list_users():
    users = []
    for user in mongo_db.db.users.find():
        users.append({
            "id": str(user["_id"]),
            "name": user["name"],
            "age": user["age"]
        })
    return users
