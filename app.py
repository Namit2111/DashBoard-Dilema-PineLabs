from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from threading import Lock
from datetime import datetime, timedelta
import asyncio
import logging
import sqlite3
import pandas as pd

from pipeline import run_nl_to_sql_pipeline  # Update this import path
from utils.db_utils import connect, run_query  # Add this import

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")

# Global agent call control
MAX_AGENT_CALLS_PER_MINUTE = 10
agent_call_count = 0
agent_call_lock = Lock()
reset_time = datetime.utcnow() + timedelta(minutes=1)


def allow_custom_agent_call():
    global agent_call_count, reset_time
    with agent_call_lock:
        now = datetime.utcnow()
        if now >= reset_time:
            agent_call_count = 0
            reset_time = now + timedelta(minutes=1)
        if agent_call_count < MAX_AGENT_CALLS_PER_MINUTE:
            agent_call_count += 1
            return True
        return False


@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "response": None})


@app.post("/", response_class=HTMLResponse)
async def process_query(request: Request, user_query: str = Form(...)):
    try:
        logger.info(f"Received query: {user_query}")
        
        if not allow_custom_agent_call():
            logger.warning("Rate limit exceeded")
            return templates.TemplateResponse("index.html", {
                "request": request,
                "response": "❌ Too many requests. Please wait a moment and try again.",
            })

        logger.info("Processing query through pipeline...")
        response = run_nl_to_sql_pipeline(user_query, debug=True)
        logger.info("Pipeline processing completed")
        
        return templates.TemplateResponse("index.html", {
            "request": request,
            "response": response,
        })
    except Exception as e:
        logger.error(f"Error processing query: {str(e)}", exc_info=True)
        return templates.TemplateResponse("index.html", {
            "request": request,
            "response": f"❌ Error: {str(e)}",
        })


@app.get("/monitor")
async def monitor():
    return {
        "agent_call_count": agent_call_count,
        "reset_time": reset_time.isoformat(),
    }


@app.head("/ping")
async def ping():
    return {"message": "pong"}


@app.get("/tables")
async def get_tables():
    """
    Get information about all tables in the database including their structure and sample data
    """
    try:
        # Get list of all tables
        tables_query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables_df = run_query(tables_query)
        tables = tables_df['name'].tolist()
        
        result = {}
        for table in tables:
            # Get table schema
            schema_query = f"PRAGMA table_info({table});"
            schema_df = run_query(schema_query)
            
            # Get sample data (first 5 rows)
            sample_query = f"SELECT * FROM {table} LIMIT 5;"
            sample_df = run_query(sample_query)
            
            result[table] = {
                "schema": schema_df.to_dict(orient='records'),
                "sample_data": sample_df.to_dict(orient='records')
            }
            
        return result
    except Exception as e:
        logger.error(f"Error getting table information: {str(e)}", exc_info=True)
        return {"error": str(e)}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)