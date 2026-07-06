from sqlalchemy.orm import Session

from app.models.tag import Tag

class TagRepository:
    def __init__(self, db:Session):
        self.db = db
    
    def get_all_tags(self):
        return self.db.query(Tag).all()
    
    def get_tag_by_id(self, tag_id: str):
        return self.db.query(Tag).filter(Tag.id == tag_id).first()
    
    def get_tag_by_slug(self, slug: str):
        return self.db.query(Tag).filter(Tag.slug == slug).first()
    
    def create_tag(self, tag: Tag):
        self.db.add(tag)
        self.db.commit()
        self.db.refresh(tag)
        return tag
    
    def update_tag(self, tag: Tag):
        self.db.commit()
        self.db.refresh(tag)
        return tag
    
    def delete_tag(self, tag: Tag):
        self.db.delete(tag)
        self.db.commit()
        return tag