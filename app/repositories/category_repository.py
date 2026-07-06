from sqlalchemy.orm import Session

from app.models.category import Category

class CategoryRepository:
    def __init__(self, db:Session):
        self.db = db
    
    def get_all_categories(self):
        return self.db.query(Category).all()
    
    def get_category_by_id(self, category_id: str):
        return self.db.query(Category).filter(Category.id == category_id).first()
    
    def get_category_by_slug(self, slug: str):
        return self.db.query(Category).filter(Category.slug == slug).first()
    
    def create_category(self, category: Category):
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def update_category(self, category: Category):
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def delete_category(self, category: Category):
        self.db.delete(category)
        self.db.commit()
        return category