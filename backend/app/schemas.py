from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ---------- Auth ----------

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ---------- Project & Section ----------

class SectionCreate(BaseModel):
    title: str
    order: int

class ProjectCreate(BaseModel):
    title: str
    topic: Optional[str] = None
    doc_type: str  # 'docx' or 'pptx'
    outline: List[SectionCreate]

class SectionOut(BaseModel):
    id: int
    title: str
    content: str
    order: int
    likes: int
    dislikes: int

    class Config:
        orm_mode = True

class ProjectOut(BaseModel):
    id: int
    title: str
    topic: Optional[str]
    doc_type: str
    sections: List[SectionOut] = []

    class Config:
        orm_mode = True

class RefineRequest(BaseModel):
    instruction: str

class FeedbackRequest(BaseModel):
    action: str  # 'like' or 'dislike'
    comment: Optional[str] = None

class TemplateRequest(BaseModel):
    topic: str
    doc_type: str
