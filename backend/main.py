from typing import Annotated

from fastapi import FastAPI, Request, Depends, HTTPException, Response
from pydantic import BaseModel

from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from authx import AuthX, AuthXConfig

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.get("/about")
# def about():
#     return {
#         "message": "Привет из FastAPI!"
#     }



config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)


class UserLoginSchema(BaseModel):
    username: str
    password: str


@app.post("/login")
def login(credentials: UserLoginSchema, response: Response):
    if credentials.username == "test" and credentials.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect username or password")

@app.get("/protected", dependencies=[Depends(security.access_token_required)])
def protected():
    return {"data": "TOP SECRET"}


engine = create_async_engine('sqlite+aiosqlite:///notes.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_session)]

class Base(DeclarativeBase):
    pass

class NoteModel(Base):
    __tablename__ = "notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    description: Mapped[str]


@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {'ok': True}


class NoteAddSchema(BaseModel):
    title: str
    description: str

@app.post("/notes")
async def add_note(data: NoteAddSchema, session: SessionDep):
    new_note = NoteModel(
        title=data.title,
        description=data.description
    )

    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)

    return new_note


@app.get("/notes/{note_id}")
async def get_note(note_id: int, session: SessionDep):
    query = select(NoteModel).where(NoteModel.id == note_id)

    result = await session.execute(query)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(status_code=404, detail="Note not found")

    return note


