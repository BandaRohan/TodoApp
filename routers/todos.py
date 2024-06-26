import sys
# sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from .auth import get_current_user
from starlette.responses import RedirectResponse
from starlette import status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates



router = APIRouter(
    prefix="/todos",
    tags=["todos"],
    responses={404: {"description": "Not found"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# In-memory list to track the order of completed tasks
completion_order = []

@router.get("/", response_class=HTMLResponse)
async def read_all_by_user(request: Request, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).filter(models.Todos.complete == False).order_by(models.Todos.priority.asc()).all()
    completed_todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).filter(models.Todos.complete == True).all()
    
    # Sort completed todos based on the order in the completion_order list
    sorted_completed_todos = sorted(completed_todos, key=lambda todo: completion_order.index(todo.id) if todo.id in completion_order else float('inf'))
    
    return templates.TemplateResponse("home.html", {"request": request, "todos": todos, "user": user, "completed_todos": sorted_completed_todos})


# @router.get("/", response_class=HTMLResponse)
# async def read_all_by_user(request: Request, db: Session= Depends(get_db)):
#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
#     # todos = db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).all()
  
#     # todos = db.query(models.Todos).filter(models.Todos.owner_id == user.get("id")).order_by(models.Todos.priority.asc()).all()
#     completed_todos = db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).filter(models.Todos.complete==True).all()

#     todos = db.query(models.Todos).filter(models.Todos.owner_id==user.get("id")).filter(models.Todos.complete==False).order_by(models.Todos.priority.asc()).all()
#     print(type(completed_todos))
    
#     return templates.TemplateResponse("home.html",{"request": request, "todos": todos,"user":user,"completed_todos":completed_todos})
#     # return templates.TemplateResponse("home.html",{"request": request, "todos": todos,"user":user})


@router.get("/add-todo", response_class=HTMLResponse)
async def add_new_todo(request: Request):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    return templates.TemplateResponse("add-todo.html",{"request":request,"user":user})


@router.post("/add-todo",response_class=HTMLResponse)
async def create_todo(request: Request, title:str = Form(...), description: str = Form(...),
                      priority: int = Form(...), db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = models.Todos()
    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority
    todo_model.complete = False
    todo_model.owner_id = user.get("id")
    db.add(todo_model)
    db.commit()

    return RedirectResponse(url = "/todos", status_code=status.HTTP_302_FOUND)


@router.get("/edit-todo/{todo_id}",response_class=HTMLResponse)
async def edit_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    return templates.TemplateResponse("edit-todo.html",{"request":request, "todo": todo,"user":user})




@router.post("/edit-todo/{todo_id}", response_class=HTMLResponse)
async def edit_tod_commit(request:Request,todo_id: int, title: str = Form(...),
                          description: str = Form(...),priority: int = Form(...),
                          db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id).first()

    todo_model.title = title
    todo_model.description = description
    todo_model.priority = priority

    db.add(todo_model)
    db.commit()

    return RedirectResponse(url = "/todos",status_code=status.HTTP_302_FOUND)


@router.get("/delete/{todo_id}")
async def delete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

    todo_model = db.query(models.Todos).filter(models.Todos.id == todo_id)\
    .filter(models.Todos.owner_id == user.get("id")).first()

    if todo_model is None:
        return RedirectResponse(url = "/todos", status_code=status.HTTP_302_FOUND)
    
    db.query(models.Todos).filter(models.Todos.id == todo_id).delete()
    db.commit()

    return RedirectResponse(url = "/todos",status_code=status.HTTP_302_FOUND)
    

# @router.get("/complete/{todo_id}", response_class=HTMLResponse)
# async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):

#     user = await get_current_user(request)
#     if user is None:
#         return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)

#     # todo = db.query(models.Todos).filter(models.Todos.id == todo_id)
#     todo = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()

#     todo.complete = not todo.complete

#     db.add(todo)
#     db.commit()

#     return RedirectResponse(url = "/todos", status_code = status.HTTP_302_FOUND)


@router.get("/complete/{todo_id}")
async def complete_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo is None:
        return RedirectResponse(url="/todos", status_code=status.HTTP_404_NOT_FOUND)
    
    todo.complete = True
    db.add(todo)
    db.commit()
    
    if todo.id not in completion_order:
        completion_order.append(todo.id)
    
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)

@router.get("/undo/{todo_id}")
async def undo_todo(request: Request, todo_id: int, db: Session = Depends(get_db)):
    user = await get_current_user(request)
    if user is None:
        return RedirectResponse(url="/auth", status_code=status.HTTP_302_FOUND)
    
    todo = db.query(models.Todos).filter(models.Todos.id == todo_id).filter(models.Todos.owner_id == user.get("id")).first()
    if todo is None:
        return RedirectResponse(url="/todos", status_code=status.HTTP_404_NOT_FOUND)
    
    todo.complete = False
    db.add(todo)
    db.commit()
    
    if todo.id in completion_order:
        completion_order.remove(todo.id)
    
    return RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
