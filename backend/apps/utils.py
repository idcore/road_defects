from bson import ObjectId
from config import settings
from typing import Any
from datetime import datetime
from apps.server.models import Info, ImageModel, Annotation, Category, COCOData, Tasks

async def lock_document(collection: Any, document_id: str):
    # Attempt to lock the document
    result = await collection.update_one(
        {"_id": document_id, "lock": {"$exists": False}},
        {"$set": {"lock": settings.client_id}},
    )
    
    if result.modified_count == 1:
        # Lock acquired
        return True
    else:
        # Document is already locked or doesn't exist
        return False

async def unlock_document(collection: Any, document_id: str):
    # Release the lock
    await collection.update_one(
        {"_id": document_id, "lock": settings.client_id},
        {"$unset": {"lock": ""}},
    )

# Usage
# document_id = "your_document_id"
# client_id = "unique_client_identifier"

# if lock_document(collection, document_id, client_id):
#     try:
#         # Perform operations on the locked document
#     finally:
#         unlock_document(collection, document_id, client_id)





def clean_up_list_results( data: list):
    results = dict()
    for i, doc in enumerate(data):
      doc["__id"] = str(doc["_id"])
      truncated_doc = {k: v for k, v in doc.items() if k != '_id'}
      results[i] = truncated_doc
    return results

def clean_up_results( data: dict):
      data["__id"] = str(data["_id"])
      truncated_data = {k: v for k, v in data.items() if k != '_id'}
      return truncated_data


def get_timestamp():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    timestamp_str = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
    return timestamp_str

def get_date():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    date_str = current_datetime.strftime("%Y/%m/%d")
    return date_str


def get_year():
    # Get the current date and time
    current_datetime = datetime.now()

    # Format the date and time as a string
    year_str = current_datetime.strftime("%Y")
    return year_str


def set_info( video_name: str, video_height: int, video_width: int, video_fps: int, video_length: int):
    info = Info()
    info.date_captured = get_timestamp()
    info.year = get_year()
    info.description = 'Дефекты дорожного покрытия'
    info.date_created = get_date()
    info.contributor = 'Coffee time team'
    info.video_name = video_name
    info.video_height = video_height
    info.video_width = video_width
    info.video_length = video_length
    info.video_fps = video_fps
    info.url = ''
    info.version = '1.0'
    return info

def get_categories():
    cats = []

    cat1 = Category( id = 0, supercategory = 'defects', name = 'crack')
    cat2 = Category(id = 1, supercategory = 'defects', name = 'pothole')
    cat3 = Category(id = 2, supercategory = 'defects', name = 'rutting')
    cat4 = Category(id = 3, supercategory = 'defects', name = 'patch')

    cats.append(cat1)
    cats.append(cat2)
    cats.append(cat3)
    cats.append(cat4)
    
    return cats