import enum
class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"
    

class PostStatus(str, enum.Enum):
    DRAFT = "draft"
    PUBLISHED = "published"