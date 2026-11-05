"""
Sempre que alterar os modelos (tabelas/colunas), gere e aplique a migração:

1. Gerar:   alembic revision --autogenerate -m "descrição da mudança"
2. Aplicar: alembic upgrade head
"""

from sqlalchemy import create_engine, Column, String, Boolean, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy_utils.types import ChoiceType

db = create_engine("sqlite:///banco.db") # Cria banco de dados

Base = declarative_base() # Cria a base do banco de dados

# Cria as classes/tabelas do banco de dados

#Usuarios

class Usuario(Base): 
    __tablename__ = "usuarios"

    id = Column("id", Integer, primary_key=True, autoincrement=True) # Chave primaria (UNICO), Adiciona o número sozinho
    nome = Column("nome", String) 
    email = Column("email", String, nullable=False, unique=True)
    senha = Column("senha", String)
    ativo = Column("ativo", Boolean)
    admin = Column("admin", Boolean, default=False) # Normalmente Falso

    def __init__(self, nome, email, senha, ativo=True, admin=False): # Sempre que iniciar a criação de um novo usuário (self)=próprio, por padrão ativo=True e admin=False
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

#Pedido

class Pedido(Base): 
    __tablename__ = "pedido"

    # STATUS_PEDIDO = [
    #     ("PENDENTE", "PENDENTE"),
    #     ("CANCELADO", "CANCELADO"),
    #     ("FINALIZADO", "FINALIZADO")
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) # pendente , finalizado, cancelado | Choicetypes garante a integridade e so vai ter textos padrões
    usuario = Column("usuario", ForeignKey("usuarios.id"), )
    preco_total = Column("preco_total", Float)
    # itens = Column()

    def __init__(self, usuario, status="PENDENTE", preco_total=0):
        self.usuario = usuario
        self.preco_total = preco_total
        self.status = status

#ItensPedido

class ItensPedido(Base): 
    __tablename__ = "itens_pedido"

    # TAMANHO_PIZZA = [
    #     ("PEQUENA", "PEQUENA"),
    #     ("MEDIA", "MEDIA"),
    #     ("GRANDE", "GRANDE")
    # ]

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column("quantidade", Integer)
    sabor = Column("sabor", String)
    tamanho = Column("tamanho", String)
    preco_unitario = Column("preco_unitario", Float)
    pedido = Column("pedido", ForeignKey("pedido.id")) # Pega da tabela "Pedido" e o campo "id"

    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido



# Executa a criação dos metadados do seu banco (cria efetivamente o bd)

