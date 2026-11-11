from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.dependencies import pegar_sessao, verificar_token
from src.schemas import ItemPedidoSchema, PedidoSchema, ResponsePedidoSchema
from src.model.models import ItemPedido, Pedido, Usuario
from typing import List

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


@order_router.get("/listar")
async def listar_pedidos(session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    if not usuario.admin:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa operação.")
    else:
        pedidos = session.query(Pedido).all() # Pega todos os pedidos
        return {
            "pedidos": pedidos
        }


@order_router.post("/pedido/adicionar-item/{id_pedido}")
async def adicionar_item_pedido(id_pedido: int, 
                                item_pedido_schema: ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao), 
                                usuario: Usuario = Depends(verificar_token)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first() # Pegando o pedido

    if not pedido:
        raise HTTPException(status_code=400, detail="Não existe esse pedido")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    else:
        item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor, item_pedido_schema.tamanho,
                                  item_pedido_schema.preco_unitario, id_pedido)
        
        session.add(item_pedido)
        pedido.calcular_preco()
        session.commit()
        return {
            "mensagem": "Item criado com sucesso",
            "item_id": item_pedido.id,
            "preco_pedido": pedido.preco_total
        }


@order_router.post("/pedido/remover-item/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido: int, 
                                item_pedido_schema: ItemPedidoSchema, 
                                session: Session = Depends(pegar_sessao), 
                                usuario: Usuario = Depends(verificar_token)):

    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first() # Pegando o item_pedido
    pedido = session.query(Pedido).filter(Pedido.id==item_pedido.pedido).first() # pegando o pedido

    if not item_pedido:
        raise HTTPException(status_code=400, detail="Item no pedido não existente")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para fazer essa modificação")
    else:

        session.delete(item_pedido) # deletando o pedido
        pedido.calcular_preco()
        session.commit()
        return {
            "mensagem": "Pedido removido com sucesso",
            "quantidade_itens_pedido": len(pedido.itens), # mostra a quantidade de itens no pedido, (lazyload)
            "pedido": pedido
        }



@order_router.post("/pedido/finalizar/{id_pedido}") # rota de finalizar pedido
async def finalizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)): 

    # usuario.admin = True
    # usuario.id == pedido.usuario
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa modificação")
    else:
        pedido.status = "FINALIZADO"

        session.commit() # Como já tem o pedido no banco de dados nao precisa dar o (.add)
        return {
            "mensagem": f"Pedido {pedido.id} finalizado com sucesso", # pedido.id evita "LazyLoad"
            "pedido": pedido # Manda os campos do pedido
        }


@order_router.get("/pedido/{id_pedido}") # vizualziar um pedido
async def vizualizar_pedido(id_pedido: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido não encontrado")
    elif not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa vizualização")

    return {
        "quantidade_itens_pedido": len(pedido.itens),
        "pedido": pedido
    }
    # return pedido # retorna so so campos padronizados no "schema"


@order_router.get("/listar-pedidos-usuario/{id_usuario}", response_model=List[ResponsePedidoSchema]) # vizualizar todos os pedidos de um usuário; (ResponsePedidoSchema) = deixa padronizado no return
async def listar_pedidos_usuario(id_usuario: int, session: Session = Depends(pegar_sessao), usuario: Usuario = Depends(verificar_token)):

    if not usuario.admin and usuario.id != id_usuario:
            raise HTTPException(status_code=403, detail="Você não tem autorização para fazer essa vizualização")
    else:
        pedidos = session.query(Pedido).filter(Pedido.usuario==id_usuario).all() # Pega todos os pedidos
        return pedidos # vem formatado de acordo com o schema, e o (List) na linha do (/listar-pedidos-usuario) faz com que cada pedido venha separado no JSON


