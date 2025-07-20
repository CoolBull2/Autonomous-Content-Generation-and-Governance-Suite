from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import uuid
import sys
import importlib

class BaseAgent(ABC):
    """Base class for all content governance agents with dynamic import support"""
    
    def __init__(self, agent_name: str, config: Dict[str, Any] = None):
        self.agent_name = agent_name
        self.config = config or {}
        self.agent_id = str(uuid.uuid4())
        self.created_at = datetime.now()
        
        # Track available modules
        self.available_modules = self._check_available_modules()
    
    def _check_available_modules(self) -> Dict[str, bool]:
        """Check which optional modules are available"""
        modules = {
            'torch': False,
            'diffusers': False,
            'transformers': False,
            'langchain': False,
            'langchain_community': False,
            'langchain_perplexity': False,
            'opencv': False,
            'reportlab': False,
            'sqlalchemy': False
        }
        
        # Check each module
        for module_name in modules:
            try:
                if module_name == 'opencv':
                    importlib.import_module('cv2')
                elif module_name == 'langchain_community':
                    importlib.import_module('langchain_community')
                elif module_name == 'langchain_perplexity':
                    importlib.import_module('langchain_perplexity')
                else:
                    importlib.import_module(module_name)
                modules[module_name] = True
            except ImportError:
                pass
        
        return modules
    
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
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Return agent capabilities based on available modules"""
        return {
            "agent_name": self.agent_name,
            "available_modules": self.available_modules,
            "capabilities": self._determine_capabilities()
        }
    
    def _determine_capabilities(self) -> List[str]:
        """Determine what this agent can do based on available modules"""
        capabilities = ["basic_processing"]
        
        if self.available_modules.get('langchain'):
            capabilities.append("text_generation")
        
        if self.available_modules.get('torch') and self.available_modules.get('diffusers'):
            capabilities.append("video_generation")
        
        if self.available_modules.get('transformers'):
            capabilities.append("ai_processing")
        
        return capabilities
