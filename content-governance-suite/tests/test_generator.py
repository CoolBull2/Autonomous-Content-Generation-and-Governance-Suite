import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.generator.content_generator import ContentGeneratorAgent

def test_content_generation():
    agent = ContentGeneratorAgent()
    
    request = {
        "type": "blog_post",
        "topic": "Benefits of AI in Healthcare",
        "style_guide": {"tone": "professional", "length": "medium"},
        "target_audience": "healthcare professionals"
    }
    
    result = agent.process(request)
    
    print(f"✅ Status: {result.get('status')}")
    print(f"✅ Content Length: {len(result.get('content', ''))}")
    print(f"✅ Quality Score: {result.get('quality_score')}")
    
    return result.get('status') == 'generated'

if __name__ == "__main__":
    success = test_content_generation()
    print(f"Generator Test: {'PASSED' if success else 'FAILED'}")
