from pydantic import BaseModel

class NoteAddSchema(BaseModel):
    title: str
    description: str