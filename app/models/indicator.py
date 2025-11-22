u200B
u200B
 
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, UniqueConstraint, JSON
from sqlalchemy.orm import relationship
from app.core.db import Base


class Indicator(Base):
    __tablename__ = "indicators"
    __table_args__ = (
        UniqueConstraint("source_id", "type", "timestamp", "zone_id", name="uq_indicator_unique"),
    )

    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=False)
    type = Column(String, nullable=False, index=True)
    value = Column(Float, nullable=False)
    unit = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    zone_id = Column(Integer, ForeignKey("zones.id"), nullable=False)
    extra = Column(JSON, nullable=True)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    source = relationship("Source", back_populates="indicators")
    zone = relationship("Zone", back_populates="indicators")
    created_by = relationship("User", back_populates="indicators")



