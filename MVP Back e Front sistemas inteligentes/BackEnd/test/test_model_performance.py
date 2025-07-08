import pytest
from sklearn.metrics import accuracy_score, f1_score
from joblib import load
import pandas as pd

## O presente teste tem a finalidade de definir se o modelo aprovado atinge valores mínimos aceitaveis de acurácia e
## F1-score.

## Inicialmente é definido os paramentos de validacao do modelo, depois sao especificados os caminhos para modelos e dataset
##e por fim a funcao load_components carrega os recursos necessarios e a funcao test_model_performance faz os testes e exibe 
## resultado. Os parametros minimos podem ser alterados conforme for mais conveniente e também os modelos e dataset utilizados.

# Parametros mínimos de aceitacao
MIN_ACCURACY = 0.70
MIN_F1_SCORE = 0.70

# Local onde o modelo e vetorizador foram salvos
MODEL_PATH = 'machine_learning/notebook/best_genre_classifier_svm.joblib'
VECTORIZER_PATH = 'machine_learning/notebook/tfidf_vectorizer.joblib'

# Caminho para o dataset 
TEST_DATA_PATH = 'machine_learning/dataset/data.csv'


@pytest.fixture
def load_components():
    model = load(MODEL_PATH)
    vectorizer = load(VECTORIZER_PATH)
    df = pd.read_csv(TEST_DATA_PATH)
    return model, vectorizer, df

def test_model_performance(load_components):
    model, vectorizer, df = load_components

    X = vectorizer.transform(df['summary'])  
    y_true = df['genre']                     

    y_pred = model.predict(X)

    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='weighted')  

    print(f"Acurácia: {acc:.2f}")
    print(f"F1-score: {f1:.2f}")

    assert acc >= MIN_ACCURACY, f"Acurácia abaixo do limite: {acc:.2f} < {MIN_ACCURACY}"
    assert f1 >= MIN_F1_SCORE, f"F1-score abaixo do limite: {f1:.2f} < {MIN_F1_SCORE}"
