import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from workflows.review_workflow import ReviewWorkflow
from agents.consensus.consensus_agent import ConsensusAgent

def test_full_pipeline():
    # Sample generated content to review
    sample_content = {
        "content": "AI in healthcare offers numerous benefits including improved diagnostics, personalized treatment plans, and enhanced patient care. Studies show that AI can reduce diagnostic errors by up to 30%.",
        "metadata": {
            "content_type": "blog_post",
            "topic": "AI in Healthcare"
        }
    }
    
    # Test workflow
    workflow = ReviewWorkflow()
    review_results = workflow.execute(sample_content)
    
    # Test consensus
    consensus_agent = ConsensusAgent()
    final_decision = consensus_agent.process(review_results)
    
    print(f"✅ Review Steps Completed: {len(review_results)}")
    print(f"✅ Final Decision: {final_decision.get('final_decision')}")
    print(f"✅ Final Score: {final_decision.get('final_score')}")
    
    return len(review_results) > 0 and final_decision.get('final_decision') is not None

if __name__ == "__main__":
    success = test_full_pipeline()
    print(f"Workflow Test: {'PASSED' if success else 'FAILED'}")
