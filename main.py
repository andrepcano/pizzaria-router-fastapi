from fastapi import FastAPI


app = FastAPI()


from routes.auth_routess import auth_router
from routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)








#    nome app / variavel
# uvicorn main:app --reload  # Para rodar o codigo executar no terminal