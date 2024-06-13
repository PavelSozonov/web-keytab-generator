import logging
import subprocess
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="Keytab generation application",
    description="Web application for Keytab generation",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/", summary="Root Endpoint", description="Returns the main web page with a download button.")
async def read_root(request: Request):
    logger.info("Root endpoint called")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/keytab", summary="Keytab File Download", description="Application accepts AD login and password of user and returns keytab file.")
async def post_keytab(login: str = Form(...), password: str = Form(...)):
    logger.info("Keytab endpoint called with login: %s", login)
    filename = "/app/" + login + ".keytab"
    try:
        subprocess.run(["/bin/sh", "/app/ktutil.sh", login, password, filename], check=True)
        return FileResponse(path=filename, filename=login + ".keytab", media_type='application/octet-stream')
    except subprocess.CalledProcessError as e:
        logger.error("Failed to generate keytab: %s", e)
        raise HTTPException(status_code=500, detail="Keytab generation failed")
    except PermissionError as e:
        logger.error("Permission denied: %s", e)
        raise HTTPException(status_code=500, detail="Permission denied")

@app.get("/health/readiness", summary="Readiness Check", description="Readiness check for the application.")
async def readiness_check():
    logger.debug("Readiness check endpoint called")
    return JSONResponse(status_code=200, content={"status": "ready"})

@app.get("/health/liveness", summary="Liveness Check", description="Liveness check for the application.")
async def liveness_check():
    logger.debug("Liveness check endpoint called")
    return JSONResponse(status_code=200, content={"status": "alive"})
