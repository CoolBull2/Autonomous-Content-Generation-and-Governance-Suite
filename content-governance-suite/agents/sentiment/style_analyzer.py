from transformers import pipeline
from typing import Dict, Any, List
import os
from datetime import datetime
from ..base_agent import BaseAgent

class StyleAnalyzerAgent(BaseAgent):
    """Agent responsible for style and sentiment analysis"""
    
    def __init__(self, config: Dict[str, Any] = None):
        super().__init__("StyleAnalyzer", config)
        
        # Initialize sentiment analysis pipeline
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        
        # Initialize other analyzers
        self.readability_analyzer = pipeline(
            "text-classification",
            model="martin-ha/toxic-comment-model"
        )
        
        self.brand_guidelines = self._load_brand_guidelines()
    
    def _load_brand_guidelines(self) -> Dict[str, Any]:
        """Load brand guidelines for consistency checking"""
        return {
            "tone": "professional",
            "avoid_words": ["awesome", "amazing", "incredible"],
            "required_elements": ["call_to_action", "brand_mention"],
            "max_sentence_length": 30,
            "preferred_style": "active_voice"
        }
    
    def process(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content style and sentiment"""
        try:
            self.log_activity("Starting style analysis")
            
            text_content = content.get("content", "")
            
            # Sentiment analysis
            sentiment_results = self._analyze_sentiment(text_content)
            
            # Readability analysis
            readability_results = self._analyze_readability(text_content)
            
            # Brand alignment check
            brand_alignment = self._check_brand_alignment(text_content)
            
            # Calculate overall style score
            style_score = self._calculate_style_score(
                sentiment_results, readability_results, brand_alignment
            )
            
            result = {
                "sentiment": sentiment_results,
                "readability": readability_results,
                "brand_alignment": brand_alignment,
                "style_score": style_score,
                "status": "approved" if style_score > 0.7 else "needs_revision",
                "agent_id": self.agent_id,
                "timestamp": datetime.now().isoformat()
            }
            
            self.log_activity("Style analysis completed", {
                "score": style_score,
                "status": result["status"]
            })
            
            return result
            
        except Exception as e:
            self.log_activity("Style analysis failed", {"error": str(e)})
            return {
                "error": str(e),
                "status": "error"
            }
    
    def _analyze_sentiment(self, content: str) -> Dict[str, Any]:
        """Analyze content sentiment"""
        # Split content into chunks for analysis
        chunks = [content[i:i+500] for i in range(0, len(content), 500)]
        
        sentiment_scores = []
        for chunk in chunks:
            result = self.sentiment_analyzer(chunk)
            sentiment_scores.append(result[0])
        
        # Aggregate results
        positive_count = sum(1 for s in sentiment_scores if s['label'] == 'POSITIVE')
        negative_count = sum(1 for s in sentiment_scores if s['label'] == 'NEGATIVE')
        neutral_count = len(sentiment_scores) - positive_count - negative_count
        
        return {
            "overall_sentiment": max(sentiment_scores, key=lambda x: x['score'])['label'],
            "confidence": max(sentiment_scores, key=lambda x: x['score'])['score'],
            "distribution": {
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count
            }
        }
    
    def _analyze_readability(self, content: str) -> Dict[str, Any]:
        """Analyze content readability"""
        # Simple readability metrics
        sentences = content.split('.')
        words = content.split()
        
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Check for toxic content
        toxicity_result = self.readability_analyzer(content[:500])  # Limit input size
        
        return {
            "average_sentence_length": avg_sentence_length,
            "total_words": len(words),
            "total_sentences": len(sentences),
            "toxicity_score": toxicity_result[0]['score'] if toxicity_result[0]['label'] == 'TOXIC' else 0,
            "readability_grade": "good" if avg_sentence_length < 20 else "needs_improvement"
        }
    
    def _check_brand_alignment(self, content: str) -> Dict[str, Any]:
        """Check alignment with brand guidelines"""
        violations = []
        
        # Check for avoided words
        content_lower = content.lower()
        for word in self.brand_guidelines["avoid_words"]:
            if word in content_lower:
                violations.append(f"Avoid word used: {word}")
        
        # Check sentence length
        sentences = content.split('.')
        long_sentences = [s for s in sentences if len(s.split()) > self.brand_guidelines["max_sentence_length"]]
        
        if long_sentences:
            violations.append(f"Long sentences detected: {len(long_sentences)}")
        
        alignment_score = 1.0 - (len(violations) * 0.2)
        
        return {
            "violations": violations,
            "alignment_score": alignment_score,
            "status": "aligned" if alignment_score > 0.8 else "needs_adjustment"
        }
    
    def _calculate_style_score(self, sentiment: Dict, readability: Dict, brand: Dict) -> float:
        """Calculate overall style score"""
        sentiment_score = sentiment['confidence'] if sentiment['overall_sentiment'] != 'NEGATIVE' else 0.5
        readability_score = 1.0 if readability['readability_grade'] == 'good' else 0.6
        brand_score = brand['alignment_score']
        
        return (sentiment_score + readability_score + brand_score) / 3
