from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
import os
import sys
import asyncio
import json
import io

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all necessary components
from agents.generator.content_generator import ContentGeneratorAgent
from workflows.review_workflow import ReviewWorkflow
from agents.consensus.consensus_agent import ConsensusAgent

# Only import database components if they exist
try:
    from database.models import create_tables, get_db, ContentHistory
    from services.analytics_service import AnalyticsService
    from services.export_service import export_service
    DATABASE_ENABLED = True
except ImportError as e:
    print(f"Database components not available: {e}")
    DATABASE_ENABLED = False

load_dotenv()

app = FastAPI(
    title="Autonomous Content Generation & Governance Suite",
    description="API for managing AI agents for content creation and review.",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
content_generator = ContentGeneratorAgent()
review_workflow = ReviewWorkflow()
consensus_agent = ConsensusAgent()

# Define request models
class ContentRequest(BaseModel):
    type: str = "blog_post"
    topic: str
    style_guide: Optional[Dict[str, Any]] = {}
    target_audience: str = "general"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Content Governance Suite API!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is healthy."}

@app.post("/generate-and-govern")
def generate_and_govern_content(request: ContentRequest):
    """
    A single endpoint to run the entire generation and governance pipeline.
    """
    try:
        # Step 1: Generate Content
        print("\n--- Step 1: GENERATING CONTENT ---")
        generated_content_data = content_generator.process(request.dict())
        if generated_content_data.get("status") == "failed":
            raise HTTPException(status_code=500, detail=f"Content generation failed: {generated_content_data.get('error')}")

        # Step 2: Run Review Workflow
        print("\n--- Step 2: EXECUTING REVIEW WORKFLOW ---")
        review_results = review_workflow.execute({"content_data": generated_content_data})

        # Step 3: Get Consensus
        print("\n--- Step 3: CALCULATING CONSENSUS ---")
        final_consensus = consensus_agent.process(review_results)

        # Step 4: Assemble the final response
        return {
            "success": True,
            "data": {
                "generated_content": generated_content_data,
                "review_pipeline": review_results,
                "final_decision": final_consensus
            }
        }
    except Exception as e:
        # Log the full exception for debugging
        print(f"An error occurred in the main pipeline: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/status")
def get_agent_status():
    """Get status of all agents"""
    return {
        "content_generator": {
            "agent_id": content_generator.agent_id,
            "status": "active",
            "created_at": content_generator.created_at.isoformat()
        }
    }

# Analytics endpoints (only if database is enabled)
if DATABASE_ENABLED:
    @app.get("/analytics/dashboard")
    def get_analytics_dashboard(days: int = 30, db: Session = Depends(get_db)):
        """Get comprehensive analytics data"""
        analytics_service = AnalyticsService(db)
        return analytics_service.get_dashboard_stats(days)

    @app.get("/analytics/trends")
    def get_content_trends(days: int = 30, db: Session = Depends(get_db)):
        """Get content generation trends"""
        analytics_service = AnalyticsService(db)
        return analytics_service.get_content_trends(days)

    @app.post("/export/pdf")
    async def export_content_pdf(content_data: Dict[str, Any]):
        """Export content analysis to PDF"""
        try:
            pdf_buffer = export_service.export_to_pdf(content_data)
            
            return StreamingResponse(
                io.BytesIO(pdf_buffer.read()),
                media_type="application/pdf",
                headers={"Content-Disposition": "attachment; filename=content_report.pdf"}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/export/word")
    async def export_content_word(content_data: Dict[str, Any]):
        """Export content analysis to Word document"""
        try:
            word_buffer = export_service.export_to_word(content_data)
            
            return StreamingResponse(
                io.BytesIO(word_buffer.read()),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": "attachment; filename=content_report.docx"}
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Initialize database tables
    try:
        create_tables()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")
else:
    print("Running without database features")

# Add a simple test endpoint that doesn't require database
@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint working", "database_enabled": DATABASE_ENABLED}
