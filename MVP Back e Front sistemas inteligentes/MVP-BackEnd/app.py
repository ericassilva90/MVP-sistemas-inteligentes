from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from flask import Flask, request, jsonify, render_template
from models.predict_model import predict_genre
from models.predict_model import predict_genre 

from flask_cors import CORS
from schemas import *

info = Info(title="My Bookcase", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definindo as tags que separam as categorias
home_tag = Tag(name="Documentação", description="Seleção de documentação")
livro_tag = Tag(name="Livro", description="Adição, visualização e remoção de livros à base de dados")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


# --- Rota para a página inicial (servirá o HTML) ---
@app.route('/')
def index():
    return render_template('index.html')

# --- Rota POST para a previsão do gênero em lote ---
@app.route('/predict_batch', methods=['POST']) # Endpoint para processar um lote de livros
def predict_batch():
    if request.method == 'POST':
        data = request.get_json() # Pega os dados JSON enviados do frontend
        books_to_process = data.get('books', []) # Espera uma chave 'books' que contém a lista de livros

        if not books_to_process:
            return jsonify({'error': 'The book list can not be empty.'}), 400

        results = []
        for book in books_to_process:
            name = book.get('name', '').strip()
            author = book.get('author', '').strip()
            synopsis = book.get('synopsis', '').strip()

            if not synopsis:
                # Retorna um erro específico para este item no resultado, mas continua processando os outros.
                results.append({
                    'name': name,
                    'author': author,
                    'synopsis': synopsis,
                    'predicted_genre': 'Erro: Empty synopsis.'
                })
                continue # Pula para o próximo livro

            try:
                # Chama a função de previsão do seu modelo para a sinopse atual
                predicted_genre = predict_genre(synopsis)
                
                # Adiciona o resultado à lista
                results.append({
                    'name': name,
                    'author': author,
                    'synopsis': synopsis,
                    'predicted_genre': predicted_genre
                })
            except Exception as e:
                # Em caso de erro na previsão de um item, adiciona um erro no resultado.
                results.append({
                    'name': name,
                    'author': author,
                    'synopsis': synopsis,
                    'predicted_genre': f'Error in prediction: {str(e)}'
                })
        
        # Retorna a lista completa de resultados
        return jsonify({'results': results}), 200

if __name__ == '__main__':
    # Roda o aplicativo Flask em modo de depuração
    app.run(debug=True, port=5000)