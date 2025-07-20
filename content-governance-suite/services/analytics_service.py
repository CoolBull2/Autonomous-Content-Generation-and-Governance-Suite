from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from database.models import ContentHistory, AgentMetrics, UserFeedback
from typing import Dict, List, Any
from datetime import datetime, timedelta

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_dashboard_stats(self, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive dashboard statistics"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Content statistics
        total_content = self.db.query(ContentHistory).filter(
            ContentHistory.created_at >= cutoff_date
        ).count()
        
        approved = self.db.query(ContentHistory).filter(
            ContentHistory.final_decision == "Approved",
            ContentHistory.created_at >= cutoff_date
        ).count()
        
        needs_revision = self.db.query(ContentHistory).filter(
            ContentHistory.final_decision == "Needs Revision",
            ContentHistory.created_at >= cutoff_date
        ).count()
        
        rejected = self.db.query(ContentHistory).filter(
            ContentHistory.final_decision == "Rejected",
            ContentHistory.created_at >= cutoff_date
        ).count()
        
        # Average scores
        avg_scores = self.db.query(
            func.avg(ContentHistory.final_score).label('avg_final'),
            func.avg(ContentHistory.factuality_score).label('avg_factuality'),
            func.avg(ContentHistory.style_score).label('avg_style')
        ).filter(ContentHistory.created_at >= cutoff_date).first()
        
        # Performance metrics
        avg_generation_time = self.db.query(
            func.avg(ContentHistory.generation_time)
        ).filter(ContentHistory.created_at >= cutoff_date).scalar()
        
        return {
            "content_stats": {
                "total": total_content,
                "approved": approved,
                "needs_revision": needs_revision,
                "rejected": rejected,
                "approval_rate": (approved / total_content * 100) if total_content > 0 else 0
            },
            "quality_scores": {
                "average_final": float(avg_scores.avg_final or 0),
                "average_factuality": float(avg_scores.avg_factuality or 0),
                "average_style": float(avg_scores.avg_style or 0)
            },
            "performance": {
                "avg_generation_time": float(avg_generation_time or 0)
            }
        }
    
    def get_content_trends(self, days: int = 30) -> List[Dict[str, Any]]:
        """Get daily content generation trends"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        daily_stats = self.db.query(
            func.date(ContentHistory.created_at).label('date'),
            func.count(ContentHistory.id).label('total'),
            func.sum(func.case([(ContentHistory.final_decision == 'Approved', 1)], else_=0)).label('approved')
        ).filter(
            ContentHistory.created_at >= cutoff_date
        ).group_by(
            func.date(ContentHistory.created_at)
        ).order_by('date').all()
        
        return [
            {
                "date": stat.date.isoformat(),
                "total": stat.total,
                "approved": stat.approved or 0,
                "approval_rate": (stat.approved / stat.total * 100) if stat.total > 0 else 0
            }
            for stat in daily_stats
        ]
    
    def get_agent_performance(self) -> Dict[str, Any]:
        """Get individual agent performance metrics"""
        recent_metrics = self.db.query(AgentMetrics).filter(
            AgentMetrics.timestamp >= datetime.utcnow() - timedelta(days=7)
        ).all()
        
        agent_stats = {}
        for metric in recent_metrics:
            if metric.agent_name not in agent_stats:
                agent_stats[metric.agent_name] = {
                    "total_operations": 0,
                    "successful_operations": 0,
                    "avg_execution_time": 0,
                    "error_rate": 0
                }
            
            agent_stats[metric.agent_name]["total_operations"] += 1
            if metric.success:
                agent_stats[metric.agent_name]["successful_operations"] += 1
        
        # Calculate rates and averages
        for agent, stats in agent_stats.items():
            total = stats["total_operations"]
            stats["success_rate"] = (stats["successful_operations"] / total * 100) if total > 0 else 0
            stats["error_rate"] = ((total - stats["successful_operations"]) / total * 100) if total > 0 else 0
        
        return agent_stats
