import random
import hashlib
from typing import Dict, Any, List
from datetime import datetime

class ABTestingService:
    def __init__(self):
        self.active_tests = {
            "generation_temperature": {
                "variants": {
                    "A": {"temperature": 0.7, "name": "Standard"},
                    "B": {"temperature": 0.9, "name": "Creative"}
                },
                "traffic_split": 50,  # 50/50 split
                "active": True
            },
            "review_strictness": {
                "variants": {
                    "A": {"threshold": 0.7, "name": "Standard"},
                    "B": {"threshold": 0.8, "name": "Strict"}
                },
                "traffic_split": 30,  # 30% for variant B
                "active": True
            }
        }
    
    def get_variant(self, test_name: str, user_id: str) -> str:
        """Determine which variant a user should see"""
        if test_name not in self.active_tests or not self.active_tests[test_name]["active"]:
            return "A"  # Default variant
        
        # Use consistent hashing to ensure same user always gets same variant
        hash_input = f"{test_name}_{user_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        
        traffic_split = self.active_tests[test_name]["traffic_split"]
        
        if (hash_value % 100) < traffic_split:
            return "B"
        return "A"
    
    def get_variant_config(self, test_name: str, variant: str) -> Dict[str, Any]:
        """Get configuration for a specific variant"""
        if test_name in self.active_tests:
            return self.active_tests[test_name]["variants"].get(variant, {})
        return {}
    
    def record_conversion(self, test_name: str, variant: str, user_id: str, outcome: str):
        """Record a conversion event for analytics"""
        # In a real implementation, this would store to a database
        conversion_data = {
            "test_name": test_name,
            "variant": variant,
            "user_id": user_id,
            "outcome": outcome,
            "timestamp": datetime.utcnow()
        }
        print(f"A/B Test Conversion: {conversion_data}")
        return conversion_data

# Global A/B testing service
ab_testing = ABTestingService()
