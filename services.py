import database as db
import models
import sqlalchemy.orm
import schemas
import email_validator 
from fastapi import HTTPException
import passlib.hash
import jwt


JWT_SECRET_KEY ='djfihfeijheigo123gmerikgjikrj4'

def create_db():
    return db.Base.metadata.create_all(bind=db.engine)


def get_db():
    databese = db.SessionLocal()
    try:
        yield databese
    finally:
        db.close()


async def GetUserByEmail(email:str, db:sqlalchemy.orm.Session):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()


async  def create_user(user:schemas.UserRequest, db:sqlalchemy.orm.Session):
    
    #check for validation email
    try:
        invalid_email = email_validator.validate_email(email=user.email)
        # email = isValid(email)
    except email_validator.EmailNotValidError:
        raise HTTPException(status_code=400,detail="PROVIDE valid email")
    
    #create hash password
    hashed_password = passlib.hash.bcrypt.hash(user.password)
    user_obj = models.UserModel(email=user.email,name = user.name,phone = user.phone,password_hash = hashed_password,)
    
    # save and commit user
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj    
    
    
async def create_token(user:models.UserModel):
    
    
    user_shema = schemas.UserBase.from_orm(user)
    # convert object to dictinaory
    user_dict = user_shema.dict()
    del user_dict['created_at']
    
    token = jwt.encode(user_dict,JWT_SECRET_KEY)
    return dict(access_token=token,token_type='bearer')

    
    
    
    