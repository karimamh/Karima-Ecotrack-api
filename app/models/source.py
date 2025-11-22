u200B
 
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.core.db import Base


class Source(Base):
    __tablename__ = "sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    kind = Column(String, nullable=False)
    url = Column(String, nullable=True)
    last_sync = Column(DateTime, nullable=True)

    indicators = relationship("Indicator", back_populates="source")


