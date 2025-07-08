*Projeto MVP - Back End - *My Bookshelf*

Esse projeto faz parte do trabalho da Sprint: Qualidade de Software, Segurança e Sistemas Inteligentes do Curso de Engenharia de Software da PUC-Rio.

Inicialmente esclareco que foi aproveitado e editado o projeto apresentado na disciplina de FullStack Basico, porem, em razão do dataset utilizado apresentar dados em inglês o idioma do projeto também foi alterado (nas partes visiveis ao utilizador).

O projeto consiste em criar um modelo de machine learning que possa prever o gênero de um livro a partir da sinopse disponibilizada. Para isso sao comparados os algoritmos KNN, Árvore de Classificação, Naive Bayes e SVM para chegar ao melhor modelo, que entao pode ser utilizado para previsao de gêneros literários pelo utilizador.

Foi feita a apresentacao do projeto no video https://youtu.be/d4eEKGMrZzQ .

# Objetivo e Funcionalidades

O presente projeto tem por objetivo criar uma API para que o usuário possa inserir os dados dos livros que leu ou está lendo. Tem objetivo pessoal e não comercial.

# Documentos

Compõem esse projeto os arquivos abaixo:
- app.py -> Arquivo principal, onde a aplicacão é inciada. Define configuracões e rotas da API.
- Pasta schemas e arquivos -> Definem a estrutura e os tipos de dados que devem ser enviados e recebidos via requisição HTTP.
- Pasta models e arquivos -> Projeto e criacao do banco de dados
- Pasta test -> teste automatizado
- Pasta machine_learning -> Dataset e notebook com o modelo de machine learning.


# Como executar 


É necessário ter todas as bibliotecas python listadas no `requirements.txt` instaladas.

Clicar com o botão direito do mouse na pasta principal e abrir o Terminal Integrado.

Colcar o código abaixo para instalar as bibliotecas listadas em requirements.txt. 

pip install -r requirements.txt



Para executar a API  basta executar:


flask run --host 0.0.0.0 --port 5000

Após isso basta abrir o link http://localhost:5000 no navegador e executar o Swagger.

Para testar a rota POST a partir do frontend basta abrir o arquivo após a execucao da API que o mesmo deve ser capaz de funcionar
e utilizar o modelo de machine learning criado.

# Modelo Machine Learning

Na pasta machine_learning estão os notebook com modelagem do modelo a ser utilizado na API, e o dataset, em pastas separadas.

# Teste

Foi criado um teste simples para testar a qualidade do modelo selecionado. Para utilizá-lo basta digital no terminal pytest test/test_model_performance.py. O resultado será exibido no próprio terminal.

Para executar a API  basta executar:


flask run --host 0.0.0.0 --port 5000

Após isso basta abrir o link http://localhost:5000 no navegador e executar o Swagger.


