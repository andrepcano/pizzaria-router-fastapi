from fastapi import APIRouter, Depends, HTTPException
from src.model.models import Usuario
from src.dependencies import pegar_sessao
from main import bcrypt_context
from src.schemas import UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"]) # prefix= primeiro nome que ficará no endpoint, tags= nome geral na documentação


@auth_router.get("/")
async def home():
    # Explicação no inicio da rota
    """
    Essa é a rota padrão de autenticação do nosso sistema
    """
    return {"mensagem": "você acessou a rota padrão de autenticação"}

@auth_router.post("/criar_conta")
async def criar_conta(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)): # Normalmente coloca o tipo da variavel para bloquear outros
    # Busca
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first() # Consulta no db

    if usuario:
        """
        Já existe um usuário com esse email
        """
              # Esse HTTP serve para personalizar a mensagem de ERRO
        raise HTTPException(status_code=400, detail="Email do usuário já cadastrado") # raise = usado para exception na hora de mandar o ERRO
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso: {usuario_schema.email}"}






