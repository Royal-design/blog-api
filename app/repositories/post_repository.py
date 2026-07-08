from sqlalchemy.orm import Session

from app.models.post import Post

class PostRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_post_by_id(self, post_id: str):
        return self.db.query(Post).filter(Post.id == post_id).first()
    
    def get_post_by_slug(self, slug: str):
        return self.db.query(Post).filter(Post.slug == slug).first()
    
    def create_post(self, post: Post):
        self.db.add(post)
        self.db.commit()
        self.db.refresh(post)
        return post
    
    def update_post(self, post: Post):
        self.db.commit()
        self.db.refresh(post)
        return post
    
    def delete_post(self, post: Post):
        self.db.delete(post)
        self.db.commit()
        return post