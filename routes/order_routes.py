from fastapi import APIRouter

order_router = APIRouter(prefix="/order", tags=["order"]) # prefix= primeiro nome que ficará no endpoint, tags= nome geral na documentação


@order_router.get("/") # decorator
async def pedidos():
    # Explicação no inicio da rota
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação
    """
    return {"mensagem: você acessou a rota de pedidos"}