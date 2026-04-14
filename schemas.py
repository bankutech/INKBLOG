from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    excerpt: Optional[str] = None
    category: str = "UX Design"
    content: str
    image: Optional[str] = None
    image_desc: Optional[str] = None

class PostCreate(PostBase):
    pass

class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: datetime
