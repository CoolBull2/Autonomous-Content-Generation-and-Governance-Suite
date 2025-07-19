from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional
from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.generator.content_generator import ContentGeneratorAgent
from agents.factcheck.factuality_agent import FactualityAgent
from agents.sentiment.style_analyzer import StyleAnalyzerAgent
from agents.multimodal.multimodal_reviewer import MultimodalReviewerAgent

load_dotenv()

app = FastAPI(
    title="Autonomous Content Generation & Governance Suite",
    description="API for managing AI agents for content creation and review.",
    version="1.0.0"
)

# Initialize all agents
content_generator = ContentGeneratorAgent()
factuality_checker = FactualityAgent()
style_analyzer = StyleAnalyzerAgent()
multimodal_reviewer = MultimodalReviewerAgent()

class ContentRequest(BaseModel):
    type: str = "blog_post"
    topic: str
    style_guide: Optional[Dict[str, Any]] = {}
    target_audience: str = "general"

class ReviewRequest(BaseModel):
    content: str
    content_type: str = "text"

@app.get("/")
def read_root():
    return {"message": "Welcome to the Content Governance Suite API!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "message": "API is healthy."}

@app.post("/generate-content")
def generate_content(request: ContentRequest):
    """Generate content using the Content Generator Agent"""
    try:
        result = content_generator.process(request.dict())
        
        if result.get("status") == "failed":
            raise HTTPException(status_code=500, detail=result.get("error"))
        
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/review-content")
def review_content(request: ReviewRequest):
    """Review content using all review agents"""
    try:
        content_dict = request.dict()
        
        # Run all review agents
        factuality_result = factuality_checker.process(content_dict)
        style_result = style_analyzer.process(content_dict)
        multimodal_result = multimodal_reviewer.process(content_dict)
        
        # Aggregate results
        overall_score = (
            factuality_result.get("overall_score", 0) +
            style_result.get("style_score", 0) +
            multimodal_result.get("score", 0)
        ) / 3
        
        return {
            "success": True,
            "data": {
                "factuality": factuality_result,
                "style": style_result,
                "multimodal": multimodal_result,
                "overall_score": overall_score,
                "recommendation": "approved" if overall_score > 0.7 else "needs_revision"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/agents/status")
def get_agent_status():
    """Get status of all agents"""
    return {
        "content_generator": {
            "agent_id": content_generator.agent_id,
            "status": "active"
        },
        "factuality_checker": {
            "agent_id": factuality_checker.agent_id,
            "status": "active"
        },
        "style_analyzer": {
            "agent_id": style_analyzer.agent_id,
            "status": "active"
        },
        "multimodal_reviewer": {
            "agent_id": multimodal_reviewer.agent_id,
            "status": "active"
        }
    }
