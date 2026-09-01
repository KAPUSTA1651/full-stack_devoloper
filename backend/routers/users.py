from fastapi import APIRouter


router = APIRouter()

@router.post("/register")
async def register():
    ...


@router.post("/login")
async def login():
    ...


@router.get("/me")
async def get_me():
    ...



# @app.post("/login")
# def login(credentials: UserLoginSchema, response: Response):
#     if credentials.username == "test" and credentials.password == "test":
#         token = security.create_access_token(uid="12345")
#         response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
#         return {"access_token": token}
#     raise HTTPException(status_code=401, detail="Incorrect username or password")

# @app.get("/protected", dependencies=[Depends(security.access_token_required)])
# def protected():
#     return {"data": "TOP SECRET"}
