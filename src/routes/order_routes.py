from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.dependencies import pegar_sessao
from src.schemas import PedidoSchema
from src.model.models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"]) # prefix= primeiro nome que ficará no endpoint, tags= nome geral na documentação


@order_router.get("/") # decorator
async def pedidos():
    # Explicação no inicio da rota
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação
    """
    return {"mensagem": "você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)): 
    # Criando novo pedido
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso: {novo_pedido.id}"}

