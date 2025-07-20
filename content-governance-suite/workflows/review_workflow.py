# workflows/review_workflow.py

from typing import Dict, Any, List
from datetime import datetime
import sys
import os

# Ensure the root directory is in the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.factcheck.factuality_agent import FactualityAgent
from agents.sentiment.style_analyzer import StyleAnalyzerAgent
from agents.multimodal.multimodal_reviewer import MultimodalReviewerAgent

class ReviewWorkflow:
    """Orchestrates the entire content review process."""
    
    def __init__(self):
        """Initializes all the necessary review agents."""
        self.factuality_agent = FactualityAgent()
        self.style_agent = StyleAnalyzerAgent()
        self.multimodal_agent = MultimodalReviewerAgent()
        print("ReviewWorkflow initialized with all review agents.")

    def execute(self, generated_content: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Executes the full review pipeline on the generated content.
        
        Args:
            generated_content: The output from the ContentGeneratorAgent.
            
        Returns:
            A list of review results from each agent.
        """
        review_steps = []
        content_to_review = generated_content.get("content_data", generated_content)

        print("--- Starting Review Workflow ---")

        # Step 1: Factuality & Compliance Check (most critical)
        print("Executing Factuality Agent...")
        factuality_result = self.factuality_agent.process(content_to_review)
        review_steps.append({"agent": "FactualityChecker", "result": factuality_result})
        
        # Early exit if content fails critical checks
        if factuality_result.get("status") in ["failed", "error"]:
            print("Workflow halted: Content failed critical factuality check.")
            return review_steps

        # Step 2: Style & Sentiment Analysis
        print("Executing Style Analyzer Agent...")
        style_result = self.style_agent.process(content_to_review)
        review_steps.append({"agent": "StyleAnalyzer", "result": style_result})

        # Step 3: Multi-modal Review (if applicable)
        print("Executing Multimodal Reviewer Agent...")
        multimodal_result = self.multimodal_agent.process(content_to_review)
        review_steps.append({"agent": "MultimodalReviewer", "result": multimodal_result})

        print("--- Review Workflow Completed ---")
        return review_steps
