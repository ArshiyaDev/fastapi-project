from pydantic import BaseModel
import datetime




class UserBase(BaseModel):
    email : str
    name : str
    phone : str
    
    
    
class UserRequest(BaseModel):
    password_hash:str
    
    class config:
        orm_mode = True

class UserResponse(BaseModel):
    id : int
    created_at : datetime.datetime
    class config:
        orm_mode = True

    


class PostBase(BaseModel):
    post_title:str
    post_description:str
    image:str
    

class PostRequest(BaseModel):
    pass


class Response(PostBase):
    id:int
    user_id:int
    created_at:datetime.datetime
    