from fastapi import FastAPI, HTTPException, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import List, Dict, Any, Optional
import os
import logging

# Import API endpoints
from api.endpoints import governance, risk, monitoring, reporting

# Create FastAPI application
app = FastAPI(
    title="AI Governance API",
    description="API for AI Governance Dashboard with agentic workflows",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development - restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers from endpoints
app.include_router(governance.router, prefix="/governance", tags=["Governance"])
app.include_router(risk.router, prefix="/risk", tags=["Risk Assessment"])
app.include_router(monitoring.router, prefix="/monitoring", tags=["Monitoring"])
app.include_router(reporting.router, prefix="/reporting", tags=["Reporting"])

# Root endpoint
@app.get("/")
def read_root():
    return {
        "name": "AI Governance API",
        "version": "1.0.0",
        "description": "API for AI Governance Dashboard with agentic workflows"
    }

# Health check endpoint
@app.get("/health")
def health_check():
    return {"status": "healthy"}

# Run server if executed as script
if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    
    # Get port from environment or use default
    port = int(os.getenv("PORT", "8000"))
    
    # Run uvicorn server
    uvicorn.run("api.main:app", host="0.0.0.0", port=port, reload=True)
