import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.generator.content_generator import ContentGeneratorAgent

def test_content_generation():
    """Test basic content generation functionality"""
    agent = ContentGeneratorAgent()
    
    request = {
        "type": "blog_post",
        "topic": "The Future of AI in Content Creation",
        "style_guide": {
            "tone": "professional",
            "length": "medium"
        },
        "target_audience": "tech professionals"
    }
    
    result = agent.process(request)
    
    assert result["status"] == "generated"
    assert result["content"] is not None
    assert len(result["content"]) > 50
    assert result["quality_score"] > 0
    
    print("✅ Content Generator Agent test passed!")
    print(f"Generated content length: {len(result['content'])}")
    print(f"Quality score: {result['quality_score']}")

if __name__ == "__main__":
    test_content_generation()
