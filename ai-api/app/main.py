import os
from typing import Optional, List

from fastapi import FastAPI, Body, HTTPException, status, File, UploadFile
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo import ReturnDocument

from imagebind import data
import torch
from imagebind.models import imagebind_model
from imagebind.models.imagebind_model import ModalityType


app = FastAPI(
    title="Resembler Deep learning API",
    summary="API for deep learning models.",
)

@app.get(
    "/health",
    response_description="Health check",
    status_code=status.HTTP_200_OK,
)
async def health_check():
    """
    Health check
    """
    return {"status": "ok"}

# Upload image and save to disk
@app.post(
    "/upload-image",
    response_description="Upload image",
    status_code=status.HTTP_200_OK,
)
async def upload_image(file: UploadFile = File(...)):
    """
    Upload image
    """
    try:
        contents = file.file.read()
        with open(f".assets/image/{file.filename}", 'wb') as f:
            f.write(contents)
        # create embedding
        embed = embed_image([file.filename])
        # save embedding to db
    except Exception:
        return {"message": "There was an error uploading the file."}
    finally:
        file.file.close()
    return {"message": f"Successfully uploaded {file.filename}"}

# Upload images and save to disk
@app.post(
    "/upload-images",
    response_description="Upload images",
    status_code=status.HTTP_200_OK,
)
async def upload_images(files: List[UploadFile] = File(...)):
    """
    Upload images
    """
    for file in files:
        try:
            contents = file.file.read()
            with open(f".assets/image/{file.filename}", 'wb') as f:
                f.write(contents)
        except Exception:
            return {"message": "There was an error uploading the file(s)."}
        finally:
            file.file.close()
    return {"message": f"Successfuly uploaded {[file.filename for file in files]}"}

# client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}:{os.environ['DB_PORT']}/{os.environ['DB_NAME']}?authSource=admin")

# uri = f"mongodb+srv://Maximilian:PPN4dUZinRDevX2W@semantic-search.xa3cf7t.mongodb.net/?retryWrites=true&w=majority"
uri = f"mongodb://{os.environ['DB_USER']}:{os.environ['DB_PASSWORD']}@{os.environ['DB_HOST']}/{os.environ['DB_NAME']}?authSource=admin"
# Create a new client and connect to the server
print(uri)
client = MongoClient(uri, server_api=ServerApi('1'))

# uri = f"mongodb+srv://{os.environ['MONGODB_ATLAS_USER']}:{os.environ['MONGODB_ATLAS_PASSWORD']}@cluster0.mtsesce.mongodb.net/?retryWrites=true&w=majority"
# # Create a new client and connect to the server
# client = MongoClient(uri, server_api=ServerApi('1'))
# # Send a ping to confirm a successful connection
# try:
#     client.admin.command('ping')
#     print("Pinged your deployment. You successfully connected to MongoDB!")
# except Exception as e:
#     print(e)



device = "mps" if torch.cuda.is_available() else "cpu"

# Instantiate model
# print("Loading model...")
# model = imagebind_model.imagebind_huge(pretrained=True)
# print("Model loaded.")
# model.eval()
# print("Model set to eval.")
# model.to(device)

# # Load data
# text_list=["The vehicle causing the accident is running a red light", "Accident type for lane change towards a middel lane"]
# image_paths=[".assets/image/red_light.png"]

# print("Loading data...")
# print(text_list, image_paths)

# inputs = {
#     ModalityType.TEXT: data.load_and_transform_text(text_list, device),
#     ModalityType.VISION: data.load_and_transform_vision_data(image_paths, device)
# }

# print("Data loaded.")
# with torch.no_grad():
#     print("Computing embeddings...")
#     embeddings = model(inputs)
#     print("Embeddings computed.")
#     print("Emb type: ", embeddings[ModalityType.VISION].type(), embeddings[ModalityType.TEXT].type())
# print("Embeddings size of dict: ", embeddings[ModalityType.VISION].shape, embeddings[ModalityType.TEXT].shape)


# print(
#     "Vision x Text: ",
#     torch.softmax(embeddings[ModalityType.VISION] @ embeddings[ModalityType.TEXT].T, dim=-1),
# )

def embed_text(text_list):
    inputs = {
        ModalityType.TEXT: data.load_and_transform_text(text_list, device),
    }
    with torch.no_grad():
        embeddings = model(inputs)
    return embeddings[ModalityType.TEXT].tolist()

def embed_image(image_paths):
    inputs = {
        ModalityType.VISION: data.load_and_transform_vision_data(image_paths, device)
    }
    with torch.no_grad():
        embeddings = model(inputs)
    return embeddings[ModalityType.VISION].tolist()

# @app.get(
#     "/embed-text",
#     response_description="Embed text",
#     status_code=status.HTTP_200_OK,
# )
# async def text_embedding(text: str):
#     pass

# @app.get(
#     "/embed-image",
#     response_description="Embed image",
#     status_code=status.HTTP_200_OK,
# )
# async def image_embedding(image_path: str): # image_path and/or image
#     pass


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
# PyObjectId = Annotated[str, BeforeValidator(str)]

# class SemanticModel(BaseModel):
#     """
#     Container for a single semantic record.
#     """

#     # The primary key for the SemanticModel, stored as a `str` on the instance.
#     # This will be aliased to `_id` when sent to MongoDB,
#     # but provided as `id` in the API requests and responses.
#     id: Optional[PyObjectId] = Field(alias="_id", default=None)
#     name: str = Field(...)
#     type: str = Field(...)
#     content: str = Field(...)
#     embedding: List[float] = Field(...)
#     model_config = ConfigDict(
#         populate_by_name=True,
#         arbitrary_types_allowed=True
#     )

# class UpdateSemanticModel(BaseModel):
#     """
#     A set of optional updates to be made to a document in the database.
#     """

#     name: Optional[str] = None
#     type: Optional[str] = None
#     content: Optional[str] = None
#     embedding: Optional[List[float]] = None
#     model_config = ConfigDict(
#         arbitrary_types_allowed=True,
#         json_encoders={ObjectId: str}
#     )

# @app.post(
#     "/students/",
#     response_description="Add new student",
#     response_model=StudentModel,
#     status_code=status.HTTP_201_CREATED,
#     response_model_by_alias=False,
# )
# async def create_student(student: StudentModel = Body(...)):
#     """
#     Insert a new student record.

#     A unique `id` will be created and provided in the response.
#     """
#     new_student = await student_collection.insert_one(
#         student.model_dump(by_alias=True, exclude=["id"])
#     )
#     created_student = await student_collection.find_one(
#         {"_id": new_student.inserted_id}
#     )
#     return created_student


# @app.get(
#     "/students/",
#     response_description="List all students",
#     response_model=StudentCollection,
#     response_model_by_alias=False,
# )
# async def list_students():
#     """
#     List all of the student data in the database.

#     The response is unpaginated and limited to 1000 results.
#     """
#     return StudentCollection(students=await student_collection.find().to_list(1000))


# @app.get(
#     "/students/{id}",
#     response_description="Get a single student",
#     response_model=StudentModel,
#     response_model_by_alias=False,
# )
# async def show_student(id: str):
#     """
#     Get the record for a specific student, looked up by `id`.
#     """
#     if (
#         student := await student_collection.find_one({"_id": ObjectId(id)})
#     ) is not None:
#         return student

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


# @app.put(
#     "/students/{id}",
#     response_description="Update a student",
#     response_model=StudentModel,
#     response_model_by_alias=False,
# )
# async def update_student(id: str, student: UpdateStudentModel = Body(...)):
#     """
#     Update individual fields of an existing student record.

#     Only the provided fields will be updated.
#     Any missing or `null` fields will be ignored.
#     """
#     student = {
#         k: v for k, v in student.model_dump(by_alias=True).items() if v is not None
#     }

#     if len(student) >= 1:
#         update_result = await student_collection.find_one_and_update(
#             {"_id": ObjectId(id)},
#             {"$set": student},
#             return_document=ReturnDocument.AFTER,
#         )
#         if update_result is not None:
#             return update_result
#         else:
#             raise HTTPException(status_code=404, detail=f"Student {id} not found")

#     # The update is empty, but we should still return the matching document:
#     if (existing_student := await student_collection.find_one({"_id": id})) is not None:
#         return existing_student

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")


# @app.delete("/students/{id}", response_description="Delete a student")
# async def delete_student(id: str):
#     """
#     Remove a single student record from the database.
#     """
#     delete_result = await student_collection.delete_one({"_id": ObjectId(id)})

#     if delete_result.deleted_count == 1:
#         return Response(status_code=status.HTTP_204_NO_CONTENT)

#     raise HTTPException(status_code=404, detail=f"Student {id} not found")