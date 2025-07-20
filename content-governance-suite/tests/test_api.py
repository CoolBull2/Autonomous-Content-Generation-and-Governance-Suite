from fastapi.testclient import TestClient
import os 
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.main import app

client = TestClient(app)

def test_generate_and_govern():
    """Test the main pipeline endpoint"""
    request_payload = {
        "type": "blog_post",
        "topic": "The Future of AI in Content Creation",
        "style_guide": {
            "tone": "professional",
            "length": "medium"
        },
        "target_audience": "tech professionals"
    }
    
    response = client.post("/generate-and-govern", json=request_payload)
    
    if response.status_code == 200:
        data = response.json()["data"]
        print("✅ Main pipeline working")
        print(f"   - Generated content: {len(data['generated_content']['content'])} chars")
        print(f"   - Review steps: {len(data['review_pipeline'])}")
        print(f"   - Final decision: {data['final_decision']['final_decision']}")
        return True
    else:
        print(f"❌ Pipeline failed: {response.status_code} - {response.text}")
        return False

if __name__ == "__main__":
    test_generate_and_govern()
