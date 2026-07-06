from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

class TagBase(BaseModel):
    name: str
    
class TagRequest(TagBase):
    pass


class TagResponse(TagBase):
    id: UUID
    slug: str
    created_at: datetime
    updated_at: datetime
    
    
    model_config = ConfigDict(from_attributes=True)