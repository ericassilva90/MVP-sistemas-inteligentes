# models/predict_model.py
import joblib
import re
import os

# Caminhos para os arquivos do modelo e vetorizador
# __file__ é o caminho do arquivo atual. os.path.dirname(__file__) pega o diretório do arquivo.
# Assim, ele procura os arquivos .joblib na mesma pasta do predict_model.py
MODEL_PATH = os.path.join(os.path.dirname(__file__), 'model.joblib')
VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), 'vectorizer.joblib')

# Carregar o modelo e o vetorizador UMA VEZ quando este módulo for importado
try:
    loaded_model = joblib.load(MODEL_PATH)
    loaded_vectorizer = joblib.load(VECTORIZER_PATH)
    print("Model and vectorizer loaded successfully!")
except FileNotFoundError:
    print(f"ERROR: Model or vectorizer files not found at: {MODEL_PATH} or {VECTORIZER_PATH}")
    loaded_model = None
    loaded_vectorizer = None
except Exception as e:
    print(f"ERROR: Failed to load model or vectorizer: {e}")
    loaded_model = None
    loaded_vectorizer = None

def clean_text(text):
    """Função de limpeza de texto (a mesma usada no treinamento)."""
    text = str(text).lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def predict_genre(synopsis_text: str) -> str:
    """
    Faz a previsão do gênero para uma dada sinopse de texto.
    Retorna uma string com o gênero previsto.
    """
    if loaded_model is None or loaded_vectorizer is None:
        return "Error: Model or vectorizer not loaded."

    cleaned_synopsis = clean_text(synopsis_text)
    # O vetorizador espera uma lista de textos, por isso [cleaned_synopsis]
    synopsis_tfidf = loaded_vectorizer.transform([cleaned_synopsis])
    
    predicted_label = loaded_model.predict(synopsis_tfidf)
    return str(predicted_label[0]) # Retorna o primeiro (e único) elemento como string

# Teste simples (opcional, para verificar se a função de previsão funciona isoladamente)
if __name__ == "__main__":
    test_synopsis = "A chilling ghost story set in a deserted lighthouse with a dark past."
    genre = predict_genre(test_synopsis)
    print(f"Test Synopsis: '{test_synopsis}'")
    print(f"Predicted Genre: {genre}")