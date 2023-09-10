import pytest
from fastapi.testclient import TestClient
from pathlib import Path
from time import sleep
from motor.motor_asyncio import AsyncIOMotorClient
from config import settings




@pytest.fixture
def test_client():
    import main
    application = main.app
    with TestClient(application) as test_client:
        yield test_client


@pytest.mark.asyncio
async def test_post_endpoint(test_client):
    # Simulate a multipart file payload (replace with your actual file data)
    file_str = "./assets/pad1.mp4"
    file_path = Path(file_str)
    file_name = str(file_path.name)

    with open(file_str, "rb") as file:
        file_data = file.read()

    # Create a dictionary with the file field name and data
    files = {"files": (file_name, file_data)}
    
    # Make a POST request to your endpoint
    response = test_client.post("/files/new", files=files)
    
    # Assert the response status code
    assert response.status_code == 200
    
    # Assert the response content (you may need to customize this based on your response structure)
    response_data = response.json()
    assert file_name == response_data['0']['original_name']
    task_id = response_data['0']['__id']
    print(task_id)
    
    sleep(1) #increase if processing will take much time

    response = test_client.get("/tasks/all")
    assert response.status_code == 200

    for k,v in response.json().items():
        if v['__id'] == task_id:
            assert 'status' in v and v['status'] == 'S'
    
    # Add more assertions as needed

    # Optionally, you can check the database for the inserted data
    # You may need to use the same database connection as your app
    # and fetch data from the "tasks" collection to verify the insertion
    
    # Example:
    # mongodb = app.mongodb_client[settings.DB_NAME]
    # collection = mongodb["tasks"]
    # inserted_data = await collection.find_one({"_id": response_data["results"][0]["_id"]})
    # assert inserted_data is not None

# Run the test with: pytest -k test_post_endpoint
