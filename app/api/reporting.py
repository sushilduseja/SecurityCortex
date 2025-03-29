from fastapi import FastAPI, HTTPException
from fastapi.routing import APIRoute
from pydantic import BaseModel, Field

app = FastAPI()

class ReportCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    report_type: str = Field(..., regex="^(Comprehensive|Governance|Risk Assessment|Compliance)$")
    description: str = Field(..., min_length=1, max_length=500)

@app.post("/generate")
async def generate_report(report: ReportCreate):
    # Validate input
    if not report.title or not report.description:
        raise HTTPException(status_code=400, message="Title and description are required")

    try:
        # Generate report logic here
        return {"message": "Report generated", "report": report.dict()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))