from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

import models, schemas
from database import SessionLocal, engine, get_db

models.Base.metadata.create_all(bind=engine)


def seed_demo_posts():
    db = SessionLocal()
    try:
        if db.query(models.Post).count() > 0:
            return
        samples = [
            models.Post(
                title="Designing for calm",
                excerpt="Why quiet interfaces help people think clearly.",
                category="UX Design",
                content="Whitespace is not empty space—it is breathing room.\n\nWhen we reduce noise, readers stay longer and remember more.",
            ),
            models.Post(
                title="Systems over screens",
                excerpt="Tokens, components, and the long game.",
                category="Design Systems",
                content="A design system is a product. Treat it like one: roadmap, owners, and measurable adoption.",
            ),
        ]
        db.add_all(samples)
        db.commit()
    finally:
        db.close()


seed_demo_posts()

app = FastAPI(title="InkBlog API")

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the actual origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/posts", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(**post.model_dump())
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/api/posts", response_model=List[schemas.Post])
def get_posts(
    skip: int = 0, 
    limit: int = 100, 
    category: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Post)
    
    if category and category != "All":
        query = query.filter(models.Post.category == category)
    
    if search:
        query = query.filter(
            models.Post.title.contains(search) | 
            models.Post.content.contains(search)
        )
        
    return query.order_by(models.Post.date.desc()).offset(skip).limit(limit).all()

@app.get("/api/posts/{post_id}", response_model=schemas.Post)
def get_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post

@app.delete("/api/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db)):
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(db_post)
    db.commit()
    return None

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
