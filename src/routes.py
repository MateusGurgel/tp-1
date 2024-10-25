
from fastapi import APIRouter
from pydantic import BaseModel
from database import users
from fastapi import HTTPException 
from database import items
from datetime import datetime, timedelta


app_router = APIRouter()

@app_router.get("/")
def read_root():
    return {"Hello": "FastAPI!"}


@app_router.get("/status")
def status():
    return {"status": "Ok!"}

# Exercício 3
#@app_router.get("/users/{username}")
#def hello_user(username: str):
#    return "Hello, " + username

@app_router.get("/users/{username}")
def get_user(username: str):

    print(users["admin"])

    if not users.get(username):
        raise HTTPException(status_code=404, detail="User not found")

    return {"username": username, "age": users.get(username)}

class CreateUserDTO(BaseModel):
    username: str
    age: int

@app_router.post("/users/{username}")
def create_user(dto: CreateUserDTO):

    if users.get(dto.username):
        raise HTTPException(status_code=400, detail="User already exists")

    users[dto.username] = dto.age
    return {"username": dto.username, "age": dto.age}


@app_router.get("/items/{item_id}")
def get_item(item_id: int):

    if not items.get(item_id):
        raise HTTPException(status_code=404, detail="Item not found")
    

    return {"item_id": item_id, "name": items.get(item_id)}

@app_router.delete("/items/{item_id}")
def delete_item(item_id: int):

    if not items.get(item_id):
        raise HTTPException(status_code=400, detail="Item not found")
    

    items.pop(item_id)

    return {"details": "ok"}


class BirthdayDTO(BaseModel):
    name: str
    birthday: str

@app_router.post("/birthday")
def calculate_birthday(dto: BirthdayDTO):
    try:
        birthday_date = datetime.strptime(dto.birthday, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    today = datetime.today()
    next_birthday = birthday_date.replace(year=today.year)

    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year + 1)

    days_until_birthday = (next_birthday - today).days

    return {"message": f"Hello {dto.name}, there are {days_until_birthday} days until your next birthday!"}