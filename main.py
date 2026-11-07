import bcrypt
from fastapi import FastAPI
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from pydantic import deprecated

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACESS_TOKEN_EXPIRE_MINUTES =  int(os.getenv("ACESS_TOKEN_EXPIRE_MINUTES"))

app = FastAPI()

                            # schemes = validação de dados
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # deprecated="auto" = se a cryptografia se torenar obsoleta ele descarta


from src.routes.auth_routess import auth_router
from src.routes.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)








#    nome app / variavel
# uvicorn main:app --reload  # Para rodar o codigo executar no terminal
#  source venv/Scripts/activate # Para entrar no ambiente virtual