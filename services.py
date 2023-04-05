import database as db
import models
import sqlalchemy.orm


def create_db():
    return db.Base.metadata.create_all(bind=db.engine)


def get_db():
    db = db.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def GetUserByEmail(email:str, db:orm.Session):
    return db.query(models.UserModel).filter(models.UserModel.email == email).first()

