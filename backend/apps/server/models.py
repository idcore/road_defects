from typing import Optional, List, Tuple
import uuid
from pydantic import BaseModel, Field, field_validator


# class DataModel(BaseModel):
#     id: str = Field(default_factory=uuid.uuid4, alias="_id")
#     name: str = Field(...)
#     completed: bool = False

class Info(BaseModel):
    description: Optional[str] = Field("")
    url: Optional[str] = Field("")
    version: Optional[str] = Field("")
    year: Optional[int] = Field(None)
    contributor: Optional[str] = Field("")
    date_created: Optional[str] = Field("")
    video_name: Optional[str] = Field("")
    video_height: Optional[int] = Field(None)
    video_width: Optional[int] = Field(None)
    video_fps: Optional[int] = Field(None)
    video_length: Optional[int] = Field(None)
    date_captured: Optional[str] = Field("")

class ImageModel(BaseModel):
    id: int
    license: Optional[int] = Field(None)
    file_name: str 
    width: Optional[int] = Field(None)
    height: Optional[int] = Field(None)
    frame_id: int
    gps_coord: List[float]
    date_captured: Optional[str] = Field("")

class Annotation(BaseModel):
    id: int
    category_id: Optional[int] = Field(None)
    iscrowd: Optional[int] = Field(0)
    segmentation: Optional[List[List[float]]] = Field(None)
    image_id: int
    area: Optional[float] = Field(None)
    bbox: Optional[List[float]] = Field(None)

class Category(BaseModel):
    supercategory: str
    id: int
    name: str

class COCOData(BaseModel):
    info: Optional[Info] = Field(None)
    images: Optional[List[ImageModel]] = Field(None)
    annotations: Optional[List[Annotation]] = Field(None)
    categories: Optional[List[Category]] = Field(None)


class COCODataMultiple(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id") # Include _id field with default value None
    datasets: COCOData

    @field_validator("id")
    def ensure_id_preserved(cls, v):
        if v is None:
            return str(uuid.uuid4())  # Initialize _id if it's None
        return v
    


class Tasks(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id") # Include _id field with default value None
    video_file: str
    file_type:str
    original_name: str
    timestamp: str
    status: str
    preprocess_text: Optional[str] = Field("")
    postprocess_text: Optional[str] = Field("")
    error_text: Optional[str] = Field("")
    lock: Optional[str] = Field(None)
    lock_timestapmp: Optional[str] = Field(None)

    @field_validator("id")
    def ensure_id_preserved(cls, v):
        if v is None:
            return str(uuid.uuid4())  # Initialize _id if it's None
        else:
            return str(v)
        
