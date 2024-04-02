from fastapi import FastAPI, HTTPException, Depends
from odmantic import AIOEngine, Model, ObjectId
from typing import List
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

# Define the MongoDB database
async def get_database():
    client = AsyncIOMotorClient("mongodb://localhost:27017")
    engine = AIOEngine(client=client, database="test")
    return engine

# Define a model
class Item(Model):
    name: str
    description: str = ""
    price: float
    in_stock: bool = True

# Create item
@app.post("/items/", response_model=Item)
async def create_item(item: Item, engine: AIOEngine = Depends(get_database)):
    await engine.save(item)
    return item

# Read item by id
@app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: ObjectId, engine: AIOEngine = Depends(get_database)):
    item = await engine.find_one(Item, Item.id == item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Read all items
@app.get("/items/", response_model=List[Item])
async def read_items(engine: AIOEngine = Depends(get_database)):
    items = await engine.find(Item)
    return items

# Update item
@app.put("/items/{item_id}", response_model=Item)
async def update_item(item_id: ObjectId, update_data: Item, engine: AIOEngine = Depends(get_database)):
    item = await engine.find_one(Item, Item.id == item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    item.model_update(update_data.model_dump(exclude_unset=True))
    await engine.save(item)
    return item

# Delete item
@app.delete("/items/{item_id}", response_model=Item)
async def delete_item(item_id: ObjectId, engine: AIOEngine = Depends(get_database)):
    item = await engine.find_one(Item, Item.id == item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    await engine.delete(item)
    return item
