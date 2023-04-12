from fastapi import FastAPI , Depends , HTTPException , security
import schemas
import services
from sqlalchemy import orm

app = FastAPI()


@app.post('/api/v1/users')
async def register_user(
    user:schemas.UserRequest,db:orm.Session = Depends(services.get_db)):

    db_user = await services.GetUserByEmail(email=user.email,db=db)
    
    if db_user:
        raise HTTPException(status_code=400,detail="Email already in use")
    
    
    db_user = await services.create_user(user = user , db=db)
    return await services.create_token(user=db_user)



@app.post('/api/v1/login')
async def login_user(from_data:security.OAuth2PasswordRequestForm = Depends(),
                     db : orm.Session = Depends(services.get_db)
):
    db_user = await services.login(email=from_data.username,password=from_data.password,db=db)
    
    # invalid login then throw exception 
    if not db_user:
        raise HTTPException(status_code=401,detail='wrong login credentials')
    
    # create and return token
    return await services.create_token(db_user) 
    
    
    
    
@app.get('/api/users/current',response_model=schemas.UserResponse)
async def current_user(user:schemas.UserResponse = Depends(services.current_user)):
    
    return user
    
    
    
@app.post('/api/v1/posts',response_model=schemas.PostResponse)
async def create_post(post_request:schemas.PostRequest,
                      user:schemas.UserRequest=Depends(services.current_user),
                      db : orm.Session = Depends(services.get_db)
):
    
    return await services.create_post(user = user,db=db,post = post_request)