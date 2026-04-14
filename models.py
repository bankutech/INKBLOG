from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime, timezone
from database import Base

def _utc_now():
    return datetime.now(timezone.utc)

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    excerpt = Column(String(200), nullable=True)
    category = Column(String(50), default="UX Design")
    content = Column(Text, nullable=False)
    image = Column(Text, nullable=True)  # Storing as Base64 for simplicity
    image_desc = Column(String(150), nullable=True)
    date = Column(DateTime, default=_utc_now)
