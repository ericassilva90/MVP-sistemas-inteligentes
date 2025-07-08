from sqlalchemy import Column, String, Integer
from typing import Union

from models import Base

# Criando a tabela "livro"

class Book(Base):
    __tablename__ = 'book'

    id = Column("pk_produto", Integer, primary_key=True)
    title = Column(String(100), unique=True)
    author = Column(String(100))
    synopsis = Column(String(5000))
    genre = Column(String(100))



    def __init__(self, title:str, author:str, synopsis:str, genre: str):
        """
        Cadastra um livro no banco de dados.
        
        """
        self.title = title
        self.author = author
        self.synopsis = synopsis
        self.genre = genre



