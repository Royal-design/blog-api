
from enum import StrEnum


class UserRole(StrEnum):
    USER = "user"
    ADMIN = "admin"
    

class PostStatus(StrEnum):
    DRAFT = "draft"
    PUBLISHED = "published"
    
class AuthProvider(StrEnum):
    CREDENTIALS = "credentials"
    GOOGLE = "google"

class TokenType(StrEnum):
    ACCESS = "access"
    REFRESH = "refresh"
    PASSWORD_RESET = "password_reset"