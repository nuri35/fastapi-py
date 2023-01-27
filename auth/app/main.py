from fastapi import FastAPI, Body, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from .schema_structure.model import PostSchema, AccountSchema, UserForgetPasswordSchema, UserLoginSchema, UserResetPasswordSchema
from .auth_process.auth_bearer import JWTBearer
from .auth_process.auth_handler import decodeJWT, resetLink, signJWT, verifyUrl
from .auth_process.hash_password import check_password, get_password_hash
from .instance.object_instance import Object



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
blocked_tokens = []
app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
async def add_post(post: PostSchema, authorization: str = Header(None)):
    bearer, token = authorization.split(" ")
    if token in blocked_tokens:
        raise HTTPException(status_code=403, detail="Token is Expired")
    
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
    for user in users:
        if user.user.email == decoded_token["user_id"]:
            if user.isverified == True:
                raise HTTPException(status_code=400, detail="Account already confirmed")
            else:
                user.isverified = True
                raise HTTPException(status_code=200, detail="Account confirmed")
    raise HTTPException(status_code=404, detail="User not found")



@app.post("/user/forgot-password")
async def forgot_password(data: UserForgetPasswordSchema = Body(...)):
    # Check if email exists in users
    for user in users: 
        if user.user.email ==  data.email:
            urlToken =  resetLink(data.email)
            raise HTTPException(status_code=200, detail= { "url" : urlToken, "state" : "Mail sent please check your mail and click the link for reset password"})
    raise HTTPException(status_code=404, detail="Account not found")
            
  

@app.post("/user/reset-password")
async def reset_password(data: UserResetPasswordSchema = Body(...)):
    # Check if email exists in users first docode token
    try:
        if data.token in blocked_tokens:
            raise HTTPException(status_code=403, detail="Token is invalid")
        decoded_token = decodeJWT(data.token)
        decoded_email = decoded_token["user_id"]
        for user in users: 
            if user.user.email ==  decoded_email:
                hash_password = get_password_hash(data.password)
                user.user.password = hash_password 
                users.append(user)
                blocked_tokens.append(data.token)
                raise HTTPException(status_code=200, detail="Password reset successfully")
        raise HTTPException(status_code=404, detail="Account not found")
        
    except Exception as e:
        raise e
       
  

    
@app.get("/user/logout", dependencies=[Depends(JWTBearer())], tags=["user"])
async def user_logout(authorization: str = Header(None)):
    bearer, token = authorization.split(" ")
    if token in blocked_tokens:
        raise HTTPException(status_code=403, detail="Token is Expired")
    blocked_tokens.append(token)
    raise HTTPException(status_code=200, detail="Logged out successfully")
   