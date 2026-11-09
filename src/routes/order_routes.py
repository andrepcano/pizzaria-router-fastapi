from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import pegar_sessao, verificar_token
from src.schemas import PedidoSchema
from src.model.models import Pedido, Usuario

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)]) # prefix= primeiro nome que ficará no endpoint, tags= nome geral na documentação


@order_router.get("/") # decorator
async def pedidos():
    # Explicação no inicio da rota
    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas de pedidos precisam de autenticação
    """
    return {"mensagem": "você acessou a rota de pedidos"}

@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):
    
    # Criando novo pedido
    novo_pedido = Pedido(usuario=pedido_schema.usuario)
    if not usuario.admin and usuario.id != pedido_schema.usuario: # pedido_schema.usuario é para quem o pedido está sendo criado.
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer esse pedido")
    else:
        session.add(novo_pedido)
        session.commit()
        return {"mensagem": f"Pedido criado com sucesso: {novo_pedido.id}"}

@order_router.post("/pedido/cancelar/{id_pedido}") # Se voce passar um param na rota OBRIGATORIAMENTE precisa estar no param da função (NÃO SE APLICA AO CONTRATRIO)
async def cancelar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)): # Apenas usuarios ADMIn ou o proprietário do pedido pode cancelar

    # usuario.admin = True
    # usuario.id == pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa modificação")
    else:
        pedido.status = "CANCELADO"

        session.commit() # Como já tem o pedido no banco de dados nao precisa dar o (.add)
        return {
            "mensagem": f"Pedido {pedido.id} cancelado com sucesso", # pedido.id evita "LazyLoad"
            "pedido": pedido # Manda os campos do pedido
        }
