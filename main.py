from typing import Annotated

from fastapi import FastAPI, Request, Depends, HTTPException, Response
from pydantic import BaseModel

from datetime import datetime
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from authx import AuthX, AuthXConfig




app = FastAPI()

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


# app = FastAPI()

# notes = {}
# engine = create_async_engine('sqlite+aiosqlite:///notes.db')

# new_session = async_sessionmaker(engine, expire_on_commit=False)

# async def get_session():
#     async with new_session() as session:
#         yield session

# SessionDep = Annotated[AsyncSession, Depends(get_session)]

# class Base(DeclarativeBase):
#     pass

# class NoteModel(Base):
#     __tablename__ = 'notes'

#     id: Mapped[int] = mapped_column(primary_key=True)
#     title: Mapped[str]
#     discription: Mapped[str]

# @app.post('/setup_database')
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     return {'ok': True}

# class NoteAddSchema(BaseModel):
#     title: str | None
#     discription: str
#     datetime: datetime

# class NoteSchema(NoteAddSchema):
#     id: int

# @app.post("/notes")
# async def add_note(data: NoteSchema, session: SessionDep):
#     new_note = NoteModel(
#         title=data.title,
#         discription=data.discription,
#     )
#     session.add(new_note)
#     await session.commit()
#     return {'ok': True}

# @app.get("/notes{note_id}")
# async def get_note(note_id, session: SessionDep):
#     query = select(NoteModel)
#     result = await session.execute(query)
#     return result.scalars().all()






# @app.get(
#         '/note{note_id}',
#         tags=['Заметка по id'],
#         summary='Получаем конкретную заметку'
#         )
# async def get_note(note_id: str):
#     for note in notes:
#         if note == note_id:
#             return {notes[note]}


# @app.post(
#     '/task', 
#           tags=['Заметка'],
#           summary='Создание новой заметки'
#           )
# async def tasks(Task: Task):
#     new_id = str(uuid4)

#     new_note = {
#         'title': Task.title,
#         'discription': Task.discription,
#         'datetime': Task.datetime
#     }

#     notes[new_id] = new_note
#     return {'massege': notes}

