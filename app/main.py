from fastapi import FastAPI
from .models import Item

app = FastAPI(title="My FastAPI App")

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.post("/items/")
def create_item(item: Item):
    return {"received": item}
