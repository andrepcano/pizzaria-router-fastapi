from fastapi import APIRouter, Depends, HTTPException
from src.model.models import Usuario
from src.dependencies import pegar_sessao
from main import SECRET_KEY, bcrypt_context, ACESS_TOKEN_EXPIRE_MINUTES, ALGORITHM
from src.schemas import LoginSchema, UsuarioSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"]) # prefix= primeiro nome que ficará no endpoint, tags= nome geral na documentação


def criar_token(id_usuario, duracao_token=timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)):

    data_expiracao_token = datetime.now(timezone.utc) + duracao_token # data expiração token
    dict_info = {"sub": id_usuario, "exp": data_expiracao_token} # sub = id_usuario, exp = expire date do token
    jwt_codificado = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return jwt_codificado

def autenticar_usuario(email, senha, session):

    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False

    return usuario

def verificar_token(token, session: Session = Depends(pegar_sessao)):

    # verificar se o token é valido
    # extrair o id do usuario do token
    usuario = session.query(Usuario).filter(Usuario.id==1).first() # da o primeiro usuario do banco de dados
    return usuario



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
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha) # Cryptografando
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": f"Usuário cadastrado com sucesso: {usuario_schema.email}"}


# login -> email e senha -> JWT token (JSON Web Token)
@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):

    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException(status_code=400, detail="Usuário não encontrado ou credenciais inválidas!")
    else:
        acess_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {"acess_token": acess_token,  # Token JWT gerado para autenticar o usuário nas próximas requisições.
                "refresh_token": refresh_token, # Token de longa duração usado para obter um novo access token quando o atual expirar, sem exigir novo login.
                "token_type": "Bearer"       # Define o tipo de autenticação: Bearer indica que o token será enviado no cabeçalho Authorization.
                }
        # JWT Bearer
        # headers = {"Authorization": "Bearer token"}
        
@auth_router.get("/refresh")
async def use_refresh_token(token_usuario):
    # verificar o token
    usuario = verificar_token(token_usuario)
    acess_token = criar_token(usuario.id)
    return {
        "acess_token": acess_token,
        "token_type": "Bearer"
    }




