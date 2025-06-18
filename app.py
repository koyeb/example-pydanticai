import uuid
from fastapi import FastAPI, Request, File, UploadFile, Form, BackgroundTasks
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
import pandas as pd
from contextlib import asynccontextmanager

from agent import get_exchange_rate, init_ollama, run_agent


# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("Initializing Ollama...")
    init_ollama()
    print("Ollama initialized successfully!")
    yield
    # Shutdown
    print("Shutting down...")

# Create the FastAPI app
app = FastAPI(lifespan=lifespan)

# Mount templates directory
templates = Jinja2Templates(directory="templates")

# Home route
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "upload.html",
        {"request": request}
    )

# Upload route
@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    try:
        # Validate file extension
        if not file.filename.endswith('.csv'):
            return templates.TemplateResponse(
                "upload.html",
                {
                    "request": request,
                    "message": "Please upload a CSV file",
                    "message_type": "danger"
                }
            )
        
        # Save the file, creating a random filename
        random_filename = str(uuid.uuid4())
        file_path = UPLOAD_DIR / random_filename
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Show the uploaded file and pass filename
        return templates.TemplateResponse(
            "upload.html",
            {
                "request": request,
                "message": f"File uploaded successfully!",
                "message_type": "success",
                "filename": random_filename
            }
        )
        
    except Exception as e:
        # Show the error
        return templates.TemplateResponse(
            "upload.html",
            {
                "request": request,
                "message": f"An error occurred: {str(e)}",
                "message_type": "danger"
            }
        )

# Process file endpoint
@app.post("/process", response_class=HTMLResponse)
async def process_file(request: Request, background_tasks: BackgroundTasks, filename: str = Form(...)):
    file_path = UPLOAD_DIR / filename
    if not file_path.exists():
        return templates.TemplateResponse(
            "upload.html",
            {
                "request": request,
                "message": "File not found. Please upload again.",
                "message_type": "danger"
            }
        )
    # Start background task
    LOG_FILE = UPLOAD_DIR / f"{filename}.log"
    background_tasks.add_task(run_agent, LOG_FILE, file_path)
    return templates.TemplateResponse(
        "upload.html",
        {
            "request": request,
            "message": f"Started processing. Log will update below.",
            "message_type": "info",
            "filename": filename,
            "show_log": True
        }
    )

# Log route
@app.get("/log/{filename}")
async def get_log(filename: str):
    LOG_FILE = UPLOAD_DIR / f"{filename}.log"
    if LOG_FILE.exists():
        with open(LOG_FILE, "r") as f:
            log_content = f.read()
        return PlainTextResponse(log_content)
    return PlainTextResponse("No log yet.")

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 