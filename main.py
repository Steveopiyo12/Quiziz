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


@app.get('/question/{id}')
async def get_question(id: int, db: db_dependency):
  result =  db.query(models.Questions).filter(models.Questions.id == id).first()
  if not result:
      raise HTTPException(status_code=404, detail="Message not found")
  return result

@app.get('/choices/{id}')
async def get_choices(id: int, db: db_dependency):
    result = db.query(models.Choices).filter(models.Choices.question_id == id).all()
    if not result:
        raise HTTPException(status_code=404, detail="choices not found")
    return result

@app.post('/questions/')
async def create_questions(question: QuestionBase, db: db_dependency):
    new_question = models.Questions(question_text = question.question_text)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    for choice in question.choices:
        new_choice = models.Choices(
            choice_text= choice.choice_text,
            is_correct = choice.is_correct,
            question_id= new_question.id)
        db.add(new_choice)
        db.commit()
         
    
    