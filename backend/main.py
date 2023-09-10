from fastapi import FastAPI, APIRouter, Body, Request, HTTPException, status, Depends, File, UploadFile
import uvicorn
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from apps.server.routers import router as app_router
from apps.server.models import *
import apps.utils as utils
import apps.processor as processor
import uuid
import aiofiles
import asyncio
from fastapi.middleware.cors import CORSMiddleware

# Define your CORS settings
origins = [
    "http://localhost:3000",  # Replace with your React app's URL
]


app = FastAPI()

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(settings.DB_URL)
    app.mongodb = app.mongodb_client[settings.DB_NAME]
    asyncio.create_task(background_task( app.mongodb))


@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


#app.include_router(app_router, tags=["defects"], prefix="/defects")



@app.get("/coco-data-single/{document_id}")
async def get_coco_data( 
    document_id: str, request: Request
):
    collection_name: str = "coco_data"    
    data: dict = get_document_from_collection(document_id, collection_name, request.app.mongodb_client)
    return data

@app.get("/coco-data/all")
async def get_coco_data_all(request: Request):
    collection_name: str = "coco_data"    
    data: dict = get_all_documents_from_collection( collection_name, request.app.mongodb_client)
    return data


@app.get("/image-data/cracks/all", response_description="Images of cracks")
async def get_coco_data_all(request: Request):
    collection_name: str = "coco_data"    
    data: dict = await get_all_images( collection_name = collection_name, defect_class = settings.defects["crack"], mongodb_client=request.app.mongodb_client)
    return data


@app.get("/image-data/potholes/all", response_description="Images of potholes")
async def get_coco_data_all(request: Request):
    collection_name: str = "coco_data"    
    data: dict = await get_all_images( collection_name = collection_name, defect_class = settings.defects["pothole"], mongodb_client = request.app.mongodb_client)
    return data


@app.get("/image-data/rutting/all", response_description="Images of rutting")
async def get_coco_data_all(request: Request):
    collection_name: str = "coco_data"    
    data: dict = await get_all_images( collection_name = collection_name, defect_class = settings.defects["rutting"], mongodb_client=request.app.mongodb_client)
    return data

@app.get("/image-data/patches/all", response_description="Images of patches")
async def get_coco_data_all(request: Request):
    collection_name: str = "coco_data"    
    data: dict = await get_all_images( collection_name = collection_name, defect_class = settings.defects["patch"], mongodb_client=request.app.mongodb_client)
    return data

@app.post("/tasks/new", response_description="Add new Data")
async def create_task(request: Request, data: Tasks = Body(...)):
    data = jsonable_encoder(data)
    mongodb = request.app.mongodb_client[settings.DB_NAME]
    collection = mongodb["tasks"]
    new_Data = await collection.insert_one(data)
    created_Data = await collection.find_one(
        {"_id": new_Data.inserted_id}
    )

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_Data)

@app.post("/files/new")
async def post_endpoint(request: Request, files: List[UploadFile]=File(...)):
    # ...
    allowed_types = [
        "video/mp4", #MPEG-4 video format, a widely supported video codec.
        "video/webm", #WebM video format, an open and royalty-free video codec often used for web video.
        "video/ogg", #Ogg video format, commonly used for HTML5 video.
        "video/quicktime", #QuickTime video format, used for videos compatible with Apple's QuickTime player.
        "video/x-msvideo", #AVI (Audio Video Interleave) video format, a multimedia container format developed by Microsoft.
        "video/x-matroska" #Matroska video format (MKV), an open and free multimedia container format.
        ]

    for in_file in files:
        
        if False: #in_file.content_type not in allowed_types:
            raise HTTPException(status_code=404,  
            detail=f"Данный формат файла не поддерживается")
    
    tasks = []

    for in_file in files:

        file_uuid = uuid.uuid4()
        out_file_path = "./inputs/" + str(file_uuid) + '.data'

        async with aiofiles.open(out_file_path, 'wb') as out_file:
            while content := await in_file.read(50*1024*1024):  # async read chunk 50MB
                await out_file.write(content)  # async write chunk

        mongodb = request.app.mongodb_client[settings.DB_NAME]
        collection = mongodb["tasks"]
        data = {
            "video_file": str(file_uuid)+'.data',
            "file_type": in_file.content_type,
            "original_name": in_file.filename,
            "timestamp": utils.get_timestamp(),
            "status": "N"
        }
        new_Data = await collection.insert_one(data)
        created_Data = await collection.find_one(
            {"_id": new_Data.inserted_id}
        )

        tasks.append( utils.clean_up_results(created_Data))
    results = dict()
    for i, task in enumerate(tasks):
        results[i] = task
    return results



@app.get("/tasks/all")
async def get_tasks( 
    request: Request
):
    collection_name: str = "tasks"    
    
    data: list = await get_all_documents_from_collection(collection_name, request.app.mongodb_client)
    results = utils.clean_up_list_results(data)
    return results


# @app.put("/{id}", response_description="Update a Data")
# async def update_Data(id: str, request: Request, Data: UpdateDataModel = Body(...)):
#     Data = {k: v for k, v in Data.dict().items() if v is not None}

#     if len(Data) >= 1:
#         update_result = await request.app.mongodb["Datas"].update_one(
#             {"_id": id}, {"$set": Data}
#         )

#         if update_result.modified_count == 1:
#             if (
#                 updated_Data := await request.app.mongodb["Datas"].find_one({"_id": id})
#             ) is not None:
#                 return updated_Data

#     if (
#         existing_Data := await request.app.mongodb["Datas"].find_one({"_id": id})
#     ) is not None:
#         return existing_Data

#     raise HTTPException(status_code=404, detail=f"Data {id} not found")


# @app.delete("/{id}", response_description="Delete Data")
# async def delete_Data(id: str, request: Request):
#     delete_result = await request.app.mongodb["Datas"].delete_one({"_id": id})

#     if delete_result.deleted_count == 1:
#         return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Data {id} not found")



async def get_document_from_collection(
    document_id: str,
    collection_name: str,
    mongodb_client: AsyncIOMotorClient,  
):
    
    # Use the real MongoDB connection to fetch the data in production
    mongodb = mongodb_client[settings.DB_NAME]
    collection = mongodb[collection_name]
    data =  await collection.find_one({"_id": document_id})
    if data:
        return data
    else:
        raise HTTPException(status_code=404,  
        detail=f"Запись в коллекции {collection_name} с идентификатором {document_id} не найдена")




async def get_all_documents_from_collection(
    collection_name: str,
    mongodb_client: AsyncIOMotorClient,  # Pass the client as a parameter
):
    mongodb = mongodb_client[settings.DB_NAME]
    collection = mongodb[collection_name]
    cursor = collection.find({})
    data =  await cursor.to_list(length=None)
    if data:
        return data
    else:
        raise HTTPException(status_code=404,  
        detail=f"Записи в коллекции {collection_name} не найдены")

# defect classes
# 0 - crack
# 1 - pothole
# 2 - rutting
# 3 - patch

async def get_all_images( collection_name:  str, defect_class: int, mongodb_client: AsyncIOMotorClient):
    documents: dict = await get_all_documents_from_collection( collection_name, mongodb_client)

    for data in documents:
        filtered_annotations = [
        annotation for annotation in data["annotations"] if annotation["category_id"] == defect_class
    ]

        # Use a set to collect unique image IDs
        image_ids = set(annotation["image_id"] for annotation in filtered_annotations)
    
        filtered_images = [
        image for image in data["images"] if image["id"] in image_ids
    ]
    return {"images":filtered_images}



async def background_task(mongodb):
    while True:
        # Replace 'your_collection_name' with the actual name of your MongoDB collection
        collection = mongodb.tasks
        await processor.process_data(collection, mongodb)
        await asyncio.sleep(1)  # Sleep for 1 seconds





if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG_MODE,
        debug=True,
        port=settings.PORT,
    )