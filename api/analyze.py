import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from services.analysis import analyze_task
import asyncio
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Data Analyst Agent API",
    description="API for data analysis tasks using LLMs",
    version="1.0.0"
)

@app.post("/api/")
async def analyze_data(file: UploadFile = File(...)):
    try:
        # Read the task description with 2.5 minute timeout (allowing for 3 min total)
        task_description = (await file.read()).decode('utf-8')
        
        result = await asyncio.wait_for(
            analyze_task(task_description),
            timeout=150
        )
        
        return JSONResponse(content=result)
    
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Analysis timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}