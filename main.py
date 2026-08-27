from fastapi import FastAPI, Request
from pydantic import BaseModel
from datetime import datetime
from uuid import uuid4

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

app = FastAPI()

notes = {}
engine = create_async_engine('sqlite+aiosqlite:///notes.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

async def get_session():
    async with new_session() as session:
        yield session

# class Task(BaseModel):
#     title: str | None
#     discription: str
#     datetime: datetime

class Base(DeclarativeBase):
    pass

class NoteModel(Base):
    __tablename__ = 'notes'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    discription: Mapped[str]

@app.post('/setup_database')
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

# @app.get(
#         '/', 
#          tags=['Все заметки'],
#          summary=''
#          )
# async def All_notes():
#     return {}


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

