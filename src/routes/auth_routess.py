from fastapi import APIRouter, Depends, HTTPException
from src.model.models import Usuario
from src.dependencies import pegar_sessao
from main import bcrypt_context
from src.schemas import LoginSchema, UsuarioSchema
from sqlalchemy.orm import Session

auth_router = APIRouter(prefix="/auth", tags=["auth"]) # prefix= primeiro nome que ficará no endpoint, tags= nome geral na documentação


def criar_token(email):

    token = f"wdajndnduawgd{email}" 
    return token



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


# login -> email e senha -> JWT token (JSON Web Token)
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):

    usuario = session.query(Usuario).filter(Usuario.email==login_schema.email).first()
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado!")
    else:
        acess_token = criar_token(usuario.id)
        return {"acess_token": acess_token,  # Token JWT gerado para autenticar o usuário nas próximas requisições.
                "token_type": "Bearer"       # Define o tipo de autenticação: Bearer indica que o token será enviado no cabeçalho Authorization.
                }
        # JWT Bearer
        # headers = {"Authorization": "Bearer token"}




