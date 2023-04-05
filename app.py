from fastapi import FastAPI 
import fastapi.security 
import sqlalchemy.orm 
import schemas
import services


app = FastAPI()


@app.post('/api/v1/users')
async def create_user(
    user:schemas.UserRequest,db:orm.Session = fastapi.Depends(services.get_db())
):

    pass
