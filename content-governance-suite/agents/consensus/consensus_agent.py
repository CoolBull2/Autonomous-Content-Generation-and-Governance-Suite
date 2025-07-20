# agents/consensus/consensus_agent.py

from typing import Dict, Any, List
from datetime import datetime
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.base_agent import BaseAgent

class ConsensusAgent(BaseAgent):
    """
    Agent responsible for analyzing all review feedback and making a final decision.
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("ConsensusAgent", config)
        # Define the weight of each agent's score in the final decision
        self.weights = {
            "FactualityChecker": 0.5,  # Most important
            "StyleAnalyzer": 0.3,
            "MultimodalReviewer": 0.2
        }
        self.approval_threshold = 0.75  # Minimum score for automatic approval

    def process(self, review_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyzes a list of review results and computes a final consensus.
        """
        self.log_activity("Starting consensus calculation.")
        
        total_score = 0.0
        summary_points = []
        
        for review in review_results:
            agent_name = review.get("agent")
            result = review.get("result", {})
            
            # Extract score from each agent's output
            score = 0
            if agent_name == "FactualityChecker":
                score = result.get("overall_score", 0)
                if result.get("status") == "failed":
                    summary_points.append("CRITICAL: Failed factuality or compliance checks.")
            elif agent_name == "StyleAnalyzer":
                score = result.get("style_score", 0)
                if result.get("status") == "needs_revision":
                    summary_points.append("REVISION: Style or brand alignment issues detected.")
            elif agent_name == "MultimodalReviewer":
                # Only factor in if not skipped
                if result.get("status") != "skipped":
                    score = result.get("score", 0)
            
            # Apply weight
            weighted_score = score * self.weights.get(agent_name, 0)
            total_score += weighted_score

        # Determine final decision
        if "CRITICAL" in " ".join(summary_points):
            final_decision = "Rejected"
        elif total_score >= self.approval_threshold:
            final_decision = "Approved"
        else:
            final_decision = "Needs Revision"
            
        self.log_activity(f"Consensus calculated: Score={total_score:.2f}, Decision={final_decision}")

        return {
            "final_decision": final_decision,
            "final_score": round(total_score, 4),
            "summary": summary_points or ["All checks passed."],
            "agent_id": self.agent_id,
            "timestamp": datetime.now().isoformat()
        }
