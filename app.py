from fastapi import FastAPI , Depends , HTTPException
import schemas
import services
from sqlalchemy import orm

app = FastAPI()


@app.post('/api/v1/users')
async def register_user(
    user:schemas.UserBase,db:orm.Session = Depends(services.get_db)):

    db_user = await services.GetUserByEmail(email=user.email,db=db)
    
    if db_user:
        raise HTTPException(status_code=400,detail="Email already in use")
    
    
    db_user = await services.create_user(user = user , db=db)
    return await services.create_token(user=db_user)

