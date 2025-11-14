from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI(
    title= "FastAPI with PostgreSQL",
    description= "Quiz App with FastAPI and PostgreSQL Database",
    version= "1.0.0",
    docs_url= "/docs",
    redoc_url= "/redoc"
    
)

models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool
    
class QuestionBase(BaseModel):
    question_text:str
    choices: List[ChoiceBase]    
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


@app.post('/questions/')
async def create_questions(question: QuestionBase, db: db_dependency):
    pass