from abc import ABC, abstractmethod
from typing import Dict, Any, List
from datetime import datetime
import uuid

class BaseAgent(ABC):
    """Base class for all content governance agents"""
    
    def __init__(self, agent_name: str, config: Dict[str, Any] = None):
        self.agent_name = agent_name
        self.config = config or {}
        self.agent_id = str(uuid.uuid4())
        self.created_at = datetime.now()
    
    @abstractmethod
    def process(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Process content and return results"""
        pass
    
    def log_activity(self, activity: str, details: Dict[str, Any] = None):
        """Log agent activity for monitoring"""
        log_entry = {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "activity": activity,
            "timestamp": datetime.now().isoformat(),
            "details": details or {}
        }
        print(f"[{self.agent_name}] {activity}")
        return log_entry
