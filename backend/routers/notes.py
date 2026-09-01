from fastapi import APIRouter, HTTPException
from sqlalchemy import select

from database import SessionDep
from models import NoteModel
from schemas import NoteAddSchema

router = APIRouter()


# @app.post('/setup_database')
# async def setup_database():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.drop_all)
#         await conn.run_sync(Base.metadata.create_all)
#     return {'ok': True}

@router.post("/notes")
async def add_note(data: NoteAddSchema, session: SessionDep):
    new_note = NoteModel(
        title=data.title,
        description=data.description
    )

    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)

    return new_note


@router.get("/notes")
async def get_notes():
    ...


@router.get("/notes/{note_id}")
async def get_note(note_id: int, session: SessionDep):
    query = select(NoteModel).where(NoteModel.id == note_id)

    result = await session.execute(query)
    note = result.scalar_one_or_none()

    if note is None:
        raise HTTPException(
            status_code=404,
            detail="Note not found"
        )

    return note


@router.put("/notes/{note_id}")
async def update_note():
    ...


@router.delete("/notes/{note_id}")
async def delete_note():
    ...








