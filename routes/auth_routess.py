from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"]) # prefix= primeiro nome que ficará no endpoint, tags= nome geral na documentação


@auth_router.get("/")
async def auth():
    # Explicação no inicio da rota
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem: você acessou a rota padrão de autenticação"}
