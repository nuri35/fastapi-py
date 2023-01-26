from fastapi import FastAPI, Body, Depends, HTTPException, status
from app.model import PostSchema, AccountSchema, UserLoginSchema
from app.auth.auth_bearer import JWTBearer
from app.auth.auth_handler import decodeJWT, signJWT, verifyUrl
from app.auth.hash_password import check_password, get_password_hash
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
        if user.user.email == data.email:
            pass_control = check_password(user.user.password, data.password)
            if pass_control:
                if user.isverified == True:
                    return True    
    return False   



# auth testing  için yazılmıs bir endpoint
@app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def add_post(post: PostSchema):
    post.id = len(posts) + 1
    posts.append(post.dict())
    return {
        "data": "post added."
    }
    



@app.post("/user/signup", tags=["user"])
async def create_user(user: AccountSchema = Body(...)):
    hash_password = get_password_hash(user.password)
    user.password = hash_password
    new_obj = Object()
    new_obj.user = user
    new_obj.isverified = False
    users.append(new_obj)
    print("email sending")
    print("verfiy email link sent to user")
    urlToken =  verifyUrl(user.email) # bu lınkı normalde yolladıgı maılde buton ıcıne gömulecek sımule edıyorum.
    raise HTTPException(status_code=201, detail= { "url" : urlToken, "userStatus" : "user created"})
      



@app.post("/user/login", tags=["user"])
async def user_login(user: UserLoginSchema = Body(...)):
    if check_user(user):
        return signJWT(user.email)
    raise HTTPException(status_code=404, detail="Wrong login details")
    
    
    
@app.get("/user/verify", tags=["user"])
async def user_verify(token: str = None):
    if token is None:
        raise HTTPException(status_code=403, detail="Token is missing")
    decoded_token = decodeJWT(token)
    if decoded_token is None:
        raise HTTPException(status_code=403, detail="Token is invalid")
    for user in users:
        if user.user.email == decoded_token["user_id"]:
            if user.isverified == True:
                raise HTTPException(status_code=400, detail="Account already confirmed")
            else:
                user.isverified = True
                raise HTTPException(status_code=200, detail="Account confirmed")
    raise HTTPException(status_code=404, detail="User not found")