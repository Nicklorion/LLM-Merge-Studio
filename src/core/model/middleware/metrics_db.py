from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from typing import Dict, Any, Optional

Base = declarative_base()

class OperationMetric(Base):
    __tablename__ = 'operation_metrics'
    
    id = Column(Integer, primary_key=True)
    operation_name = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    duration = Column(Float)
    cpu_percent = Column(Float)
    memory_usage = Column(Float)
    gpu_memory = Column(Float, nullable=True)
    cuda_available = Column(Boolean)
    success = Column(Boolean)
    error_message = Column(String, nullable=True)
    metadata = Column(JSON)

class MetricsDatabase:
    def __init__(self, db_url: str = "sqlite:///metrics.db"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    def store_metrics(
        self,
        operation_name: str,
        metrics: Dict[str, Any],
        success: bool,
        error_message: Optional[str] = None
    ):
        """Store operation metrics in database"""
        session = self.Session()
        try:
            metric = OperationMetric(
                operation_name=operation_name,
                duration=metrics.get('duration', 0),
                cpu_percent=metrics.get('cpu_percent', 0),
                memory_usage=metrics.get('memory_usage', 0),
                gpu_memory=metrics.get('gpu_memory'),
                cuda_available=metrics.get('cuda_available', False),
                success=success,
                error_message=error_message,
                metadata=metrics.get('metadata', {})
            )
            session.add(metric)
            session.commit()
        finally:
            session.close()
    
    def get_operation_history(
        self,
        operation_name: str,
        limit: int = 100
    ) -> list[OperationMetric]:
        """Retrieve operation history from database"""
        session = self.Session()
        try:
            return (session.query(OperationMetric)
                   .filter_by(operation_name=operation_name)
                   .order_by(OperationMetric.timestamp.desc())
                   .limit(limit)
                   .all())
        finally:
            session.close()