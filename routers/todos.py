from fastapi import APIRouter, Path, HTTPException
from dtos.todos_dto import TodoDTO
from modals.todos import Todos
from database import db_dependency
from starlette import status
from helper import user_dependency

router = APIRouter(prefix="/todos", tags=["Todos"])

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    return db.query(Todos).filter(Todos.owner_id==user.get("id")).all()

@router.get("/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
   current_todo = db.query(Todos).filter(Todos.id ==todo_id and Todos.owner_id==user.get("id")).first()
   if(current_todo is None): 
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
   return current_todo   

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoDTO):
   todo_modal = Todos(**todo_request.__dict__, owner_id=user.get('id'))
   db.add(todo_modal)
   db.commit()
   
@router.put("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependency, todo_request: TodoDTO, todo_id: int = Path(gt=0)):
   current_todo = db.query(Todos).filter(Todos.id ==todo_id and Todos.owner_id==user.get("id")).first()
   if(current_todo is None): 
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
   update_todo = Todos(**todo_request.__dict__, id=todo_id)
   db.add(update_todo)
   db.commit()


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):  
 current_todo = db.query(Todos).filter(Todos.id ==todo_id and Todos.owner_id==user.get("id")).first()
 if(current_todo is None): 
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')
 db.query(Todos).filter(Todos.id==todo_id).delete()
 db.commit()
