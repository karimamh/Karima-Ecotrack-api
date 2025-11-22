u200B
u200B
 
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.core.db import Base


class Zone(Base):
    __tablename__ = "zones"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    postal_code = Column(String, index=True, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    indicators = relationship("Indicator", back_populates="zone")



