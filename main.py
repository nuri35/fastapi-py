from fastapi import FastAPI, Body, Depends
from app.model import PostSchema, AccountSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import signJWT
from app.auth.hash_password import get_password_hash
from app.instance.object_instance import Object


posts = [
    {
        "id": 1,
        "title": "Penguins ",
        "text": "Penguins are a group of aquatic flightless birds."
    },
    {
        "id": 2,
        "title": "Tigers ",
        "text": "Tigers are the largest living cat species and a memeber of the genus panthera."
    },
    {
        "id": 3,
        "title": "Koalas ",
        "text": "Koala is arboreal herbivorous maruspial native to Australia."
    },
]

users = []

app = FastAPI()



def check_user(data: UserLoginSchema):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.get("/allUser", tags=["user"])
async def add_post():
    return users


@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }
    


# emaıl yolla link verify tokenı hesabı dogrulasın sonra logın olabılsın kısı
@app.post("/user/signup", tags=["user"])
async def create_user(user: AccountSchema = Body(...)):
    hash_password = get_password_hash(user.password)
    user.password = hash_password
    new_obj = Object()
    new_obj.user = user
    new_obj.isverified = True # similuate email verification
    # users.append(new_obj)
    # return signJWT(user.email)
    return new_obj


@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }