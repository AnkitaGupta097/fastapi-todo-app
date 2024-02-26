from fastapi import FastAPI
from routers import todos,users,admin

app = FastAPI()

@app.get("/health")
async def root():
 return {'status': 'Healthy'}

app.include_router(todos.router)
app.include_router(users.router)
app.include_router(admin.router)