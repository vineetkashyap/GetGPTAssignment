from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from .tasks import fetch_and_process_data

app = FastAPI()

class ProcessRequest(BaseModel):
    user_email: str

@app.post("/process")
async def process_data(request: ProcessRequest, background_tasks: BackgroundTasks):
    background_tasks.add_task(fetch_and_process_data, request.user_email)
    return {"message": "Processing started"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
