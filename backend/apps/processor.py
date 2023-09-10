from bson import ObjectId
from config import settings
from typing import Any
from datetime import datetime
from apps.server.models import Info, ImageModel, Annotation, Category, COCOData, Tasks
import apps.utils as utils
from apps.preprocess import preprocess_data
from apps.postprocess import postprocess_data


async def process_data(collection: Any, mongodb: Any):
    data =  await collection.find_one({"status": "N"})
    if data is not None:
        if await utils.lock_document(collection, data["_id"]):
            try:
                # Perform operations on the locked document
                # Update the status field to 'P'
                try:
                    # now ds_pkey returned if preprocess_data, adapt output parameters
                    # if dataset will be written only at 2nd stage
                    ds_pkey, status, message = await preprocess_data(data, mongodb )
                    await collection.update_one(
                        {"_id": data["_id"]},
                        {"$set": {"status": status,"preprocess_text": message}}
                    )                      

                    ds_pkey, status, message = await postprocess_data(ds_pkey, data, mongodb )
                    await collection.update_one(
                        {"_id": data["_id"]},
                        {"$set": {"status": status,"postprocess_text": message}}
                    )                  
                               
                except Exception as e:
                    await collection.update_one(
                        {"_id": data["_id"]},
                        {"$set": {"status": "E","error_text": str(e)}}
                    )                    

                await collection.update_one(
                    {"_id": data["_id"]},
                    {"$set": {"status": "S"}}
                )


            finally:
                await utils.unlock_document(collection, data["_id"])