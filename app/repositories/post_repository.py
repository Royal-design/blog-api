from sqlalchemy.orm import Session
from sqlalchemy.orm import selectinload

from app.models.post import Post

class PostRepository:
    def __init__(self, db: Session):
        self.db = db

    def _query_with_relationships(self):
        return self.db.query(Post).options(
            selectinload(Post.author),
            selectinload(Post.category),
            selectinload(Post.tags),
            selectinload(Post.images),
        )
        
    def get_all_posts(self):
        return self._query_with_relationships().all()
    
    def get_post_by_id(self, post_id: str):
        return self._query_with_relationships().filter(Post.id == post_id).first()
    
    def get_post_by_slug(self, slug: str):
        return self._query_with_relationships().filter(Post.slug == slug).first()
    
    def create_post(self, post: Post):
        self.db.add(post)
        self.db.commit()
        return self.get_post_by_id(post.id)
    
    def update_post(self, post: Post):
        self.db.commit()
        return self.get_post_by_id(post.id)
    
    def delete_post(self, post: Post):
        self.db.delete(post)
        self.db.commit()
        return post
