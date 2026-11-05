from src.model.models import db
from sqlalchemy.orm import sessionmaker, Session

def pegar_sessao():
    try: 
        # Criando sessão db
        SessionLocal = sessionmaker(bind=db)
        session: Session = SessionLocal()

        yield session # yield é um "return" sem ENCERRAR a função

    finally: # CERTEZA que vai fechar, é independente se o try der certou ou errado
        session.close()