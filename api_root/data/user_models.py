from bson import ObjectId
from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional

class User(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    
    id: Optional[str] = Field(alias='_id', default=None)
    username: str
    password: str
    admin: Optional[bool] = False


class UserAuth(BaseModel):
    username:str
    password:str

class UserCollection(BaseModel):
    users: List[User]

class UserQuery(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None

class UserUpdate(BaseModel):
    password:Optional[str]=None

class UserAuth(BaseModel):
    username: str
    password: str
