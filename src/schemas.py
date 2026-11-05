# schemas.py
# Aqui ficam os SCHEMAS (Pydantic): eles descrevem o formato dos dados que
# ENTRAM e SAEM da API (o JSON da requisição e da resposta).
# Não confundir com o models.py (SQLAlchemy), que descreve as TABELAS do banco.
#
# Para que serve:
# - Validar automaticamente o que o cliente envia (se faltar um campo ou o tipo
#   estiver errado, o FastAPI responde 422 sozinho).
# - Receber os dados no corpo (JSON) em vez de na URL, o que é mais seguro para senha.
# - Controlar o que o cliente pode enviar (ex.: "admin" fica de fora para ninguém
#   se criar como administrador pela API).
# - Gerar a documentação do Swagger (/docs) com os campos esperados.

from pydantic import BaseModel
from typing import Optional

class UsuarioSchema(BaseModel):

    nome: str
    email: str
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True