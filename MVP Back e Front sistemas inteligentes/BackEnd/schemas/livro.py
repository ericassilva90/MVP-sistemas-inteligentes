from pydantic import BaseModel
from typing import Optional, List
from models.livro import Book



class BookSchema(BaseModel):
    """ Define como um novo livro a ser inserido deve ser representado.
    """
    title: str = "Pride and Prejudice"
    author: str = 'Jane Austen'
    synopsis: str = 'A timeless tale of Elizabeth Bennets quest for love and understanding amidst societal pressures and misconceptions.'
 



class ListBookSchema(BaseModel):
    """ Define como uma listagem de livros será retornada.
    """
    books:List[BookSchema]


def apresenta_livros(books: List[Book]):
    """ Retorna uma representação do livro seguindo o schema definido em BookViewSchema.
    """
    result = []
    for book in books:
        result.append({
            "title": book.title,
            "author": book.author,
            "synopsis": book.synopsis,
            "genre": book.genre   
            })

    return {"books": result}


class BookViewSchema(BaseModel):
    """ Define como um livro será retornado.
    """
    id: int = 1
    title: str = "Pride and Prejudice"
    author: str = 'Jane Austen'
    synopisis: str = 'A timeless tale of Elizabeth Bennets quest for love and understanding amidst societal pressures and misconceptions.'
    genre: str = 'fantasy'
   


def apresenta_livro(book: Book):
    """ Retorna uma representação do livro seguindo o schema definido em BookViewSchema.
    """
    return {
        "id": book.id,
        "title": book.title,
        "author": book.author,
        "synopsis": book.synopsis,
        "genre": book.genre
    }
