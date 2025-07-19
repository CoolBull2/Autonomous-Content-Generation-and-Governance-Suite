import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.generator.content_generator import ContentGeneratorAgent
from agents.factcheck.factuality_agent import FactualityAgent
from agents.sentiment.style_analyzer import StyleAnalyzerAgent
from agents.multimodal.multimodal_reviewer import MultimodalReviewerAgent

def test_full_pipeline():
    """Test the complete content generation and review pipeline"""
    
    print("🚀 Testing Phase 2 Implementation")
    print("=" * 50)
    
    # Initialize agents
    generator = ContentGeneratorAgent()
    factuality = FactualityAgent()
    style = StyleAnalyzerAgent()
    multimodal = MultimodalReviewerAgent()
    
    # Test content generation
    print("\n1. Testing Content Generation...")
    content_request = {
        "type": "blog_post",
        "topic": "The Benefits of AI in Healthcare",
        "style_guide": {"tone": "professional", "length": "medium"},
        "target_audience": "healthcare professionals"
    }
    
    generated_content = generator.process(content_request)
    print(f"✅ Content generated: {generated_content}")
    
    # Test factuality checking
    print("\n2. Testing Factuality Checking...")
    fact_result = factuality.process(generated_content)
    print(f"✅ Factuality score: {fact_result}")
    
    # Test style analysis
    print("\n3. Testing Style Analysis...")
    style_result = style.process(generated_content)
    print(f"✅ Style score: {style_result}")
    
    # Test multimodal review
    print("\n4. Testing Multimodal Review...")
    multimodal_result = multimodal.process({"type": "text", "content": generated_content['content']})
    print(f"✅ Multimodal review: {multimodal_result}")
    
    # # Calculate overall score
    overall_score = (
        fact_result['overall_score'] +
        style_result['style_score']
    ) / 2
    
    print(f"\n🎯 Overall Content Score: {overall_score:.2f}")
    print(f"📊 Recommendation: {'APPROVED' if overall_score > 0.7 else 'NEEDS REVISION'}")
    
    print("\n✅ Phase 2 Testing Complete!")

if __name__ == "__main__":
    test_full_pipeline()
