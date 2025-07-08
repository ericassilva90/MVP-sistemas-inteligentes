from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from schemas import *
import joblib
import numpy as np
from models import *
import os


info = Info(title="My Bookshelf", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Obtém o diretório base onde o app.py está sendo executado
# Obtém o diretório base onde o app.py está sendo executado
# Isso resultaria em algo como '/caminho/para/seu_projeto'
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define o caminho para a pasta 'machine_learning' que está DIRETAMENTE em BASE_DIR
MACHINE_LEARNING_DIR = os.path.join(BASE_DIR, 'machine_learning')

# Define o caminho para a pasta 'notebook' que está DENTRO de 'machine_learning'
NOTEBOOK_DIR = os.path.join(MACHINE_LEARNING_DIR, 'notebook')

# Agora, especifique os caminhos completos para os arquivos .joblib dentro da pasta 'notebook'
MODEL_PATH = os.path.join(NOTEBOOK_DIR, 'best_genre_classifier_svm.joblib')
VECTORIZER_PATH = os.path.join(NOTEBOOK_DIR, 'tfidf_vectorizer.joblib')

# Carregue o modelo e o vetorizador UMA ÚNICA VEZ quando a aplicação for iniciada.
# Isso economiza tempo e recursos, evitando recarregar a cada requisição.
try:
    classifier_model = joblib.load(MODEL_PATH)
    tfidf_vectorizer = joblib.load(VECTORIZER_PATH)
    print("Modelo SVM e TF-IDF Vectorizer carregados com sucesso.")
except Exception as e:
    print(f"Erro ao carregar os arquivos: {e}")
    # Se houver um erro no carregamento, defina como None e a API retornará um erro 500
    classifier_model = None
    tfidf_vectorizer = None

# Definindo as tags que separam as categorias
home_tag = Tag(name="Documentação", description="Seleção de documentação")
book_tag = Tag(name="Livro", description="Adição, visualização e remoção de livros à base de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# --- Rota para a página inicial (servirá o HTML) ---
@app.route('/')
def index():
    return render_template('index.html')



@app.post(
    "/predict",
    tags=[book_tag],
    responses={
        "200": BookViewSchema,
        "400": ErrorSchema,
        "409": ErrorSchema,
    },
)

def predict(form: BookSchema):  # Pode manter o esquema se estiver usando validação automática
    # Verifica se modelos estão carregados
    if classifier_model is None or tfidf_vectorizer is None:
        return jsonify({'error': 'Modelo ou vetorizador não carregados.'}), 500

    try:
        # Detecta se o conteúdo é JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form

        title = data.get('title', 'Não Informado')
        author = data.get('author', 'Não Informado')
        synopsis = data.get('synopsis', '')

        if not synopsis:
            return jsonify({'error': 'Campo "sinopse" é obrigatório.'}), 400

        text_features = tfidf_vectorizer.transform([synopsis])
        prediction = classifier_model.predict(text_features)
        predicted_genre = prediction[0]

        return jsonify({
            'title': title,
            'author': author,
            'synopsis': synopsis,
            'predicted_genre': predicted_genre
        })

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500

    
if __name__ == '__main__':
    # Execute a aplicação Flask.
    # Em ambiente de desenvolvimento, 'debug=True' é útil para ver erros.
    # Em produção, 'debug' deve ser 'False' por motivos de segurança.
    # 'host="0.0.0.0"' permite que a API seja acessível de outras máquinas na rede.
    app.run(debug=True, host='0.0.0.0')


@app.get('/books', tags=[book_tag],
         responses={"200": ListBookSchema, "404": ErrorSchema})
def get_livros():
    #faz a busca por todos os Livros cadastrados."""
    
     # criando conexão com a base
     session = Session()
     # fazendo a busca
     books = session.query(Book).all()

     if not books:
        # se não há produtos cadastrados
        return {"produtos": []}, 200
     else:
        # retorna a representação de produto
        print(books)
        return apresenta_livros(books), 200
