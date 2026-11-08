from fastapi import Depends, HTTPException
from main import SECRET_KEY, ALGORITHM, oauth2_schema
from src.model.models import db
from sqlalchemy.orm import sessionmaker, Session
from src.model.models import Usuario
from jose import jwt, JWTError

def pegar_sessao():
    try: 
        # Criando sessão db
        SessionLocal = sessionmaker(bind=db)
        session: Session = SessionLocal()

        yield session # yield é um "return" sem ENCERRAR a função

    finally: # CERTEZA que vai fechar, é independente se o try der certou ou errado
        session.close()


def verificar_token(token: str = Depends(oauth2_schema), session: Session = Depends(pegar_sessao)): # Com Depends(oauth2_schema) o token vai ser passado pelo HEADER da requisição

    try: 
        dict_infos_usuario = jwt.decode(token, SECRET_KEY, ALGORITHM) # verificar se o token é valido
        id_usuario = int(dict_infos_usuario.get("sub")) # extrair o id do usuario do token
    except JWTError as erro:
        raise HTTPException(status_code=401, detail="Acesso Negado, verifique a validade do token") # 401 = Acesso Negado
    
    usuario = session.query(Usuario).filter(Usuario.id==id_usuario).first() # da o primeiro usuario do banco de dados
    if not usuario: # Se não existe no bd
        raise HTTPException(status_code=401, detail="Acesso Inválido!")
    return usuario
