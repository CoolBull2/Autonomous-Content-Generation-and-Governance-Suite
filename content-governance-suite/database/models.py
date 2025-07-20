from sqlalchemy import Column, Integer, String, DateTime, Text, Float, JSON, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import os

Base = declarative_base()

class ContentHistory(Base):
    __tablename__ = "content_history"
    
    id = Column(Integer, primary_key=True, index=True)
    content_type = Column(String(50), nullable=False)
    topic = Column(String(200), nullable=False)
    generated_content = Column(Text, nullable=False)
    target_audience = Column(String(100))
    style_guide = Column(JSON)
    
    # Review Results
    factuality_score = Column(Float)
    style_score = Column(Float)
    multimodal_score = Column(Float)
    final_score = Column(Float)
    final_decision = Column(String(50))
    
    # Metadata
    agent_ids = Column(JSON)
    generation_time = Column(Float)  # Time taken in seconds
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class AgentMetrics(Base):
    __tablename__ = "agent_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    agent_name = Column(String(100), nullable=False)
    operation_type = Column(String(50))  # generate, review, consensus
    execution_time = Column(Float)
    success = Column(Boolean, default=True)
    error_message = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class UserFeedback(Base):
    __tablename__ = "user_feedback"
    
    id = Column(Integer, primary_key=True, index=True)
    content_id = Column(Integer)
    user_rating = Column(Integer)  # 1-5 scale
    feedback_text = Column(Text)
    improvement_suggestions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

# Database setup
engine = create_engine(os.getenv("DATABASE_URL"))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
