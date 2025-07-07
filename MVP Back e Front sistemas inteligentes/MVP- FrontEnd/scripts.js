/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
 const getList = async () => {
  
    fetch('http://localhost:5000/books', {method: 'GET',})

      .then(response => response.json())
      .then(data => {data.books.forEach(item => insertList(item.name, item.author, item.synopsis, item.genre))})
      .catch(error => {console.error('Error:', error)});
  }
 

  /*
    --------------------------------------------------------------------------------------
    Chamada da função para carregamento inicial dos dados presente no banco.
    --------------------------------------------------------------------------------------
  */  
  getList()
  
  /*
    --------------------------------------------------------------------------------------
    Função para colocar um livro na lista do servidor via requisição POST
    --------------------------------------------------------------------------------------
  */

  const postItem = async (inputName, inputAuthor, inputSynopsis) => {
    const formData = new FormData();
    formData.append('name', inputName);
    formData.append('author', inputAuthor);
    formData.append('synopsis', inputSynopsis);
  
    
    fetch('http://localhost:5000/book', {method: 'POST', body: formData})

      .then(response => response.json())
      .then((data) => {
        return data;
      })
      .catch(error => {console.error('Error:', error)});
  }





  /*
    --------------------------------------------------------------------------------------
    Função para adicionar um novo livro ao clicar em 'Salvar'
    --------------------------------------------------------------------------------------
  */
  const newItem = () => {
    let inputName = document.getElementById("name").value;
    let inputAuthor = document.getElementById("author").value;
    let inputSynopsis = document.getElementById("synopsis").value;

    if (inputName === '' || inputAuthor === '' || inputSynopsis === '') {
      alert("All the spaces must be filled!");
    } else {

      try {
        // Envia os dados para o servidor e aguarda a resposta com o diagnóstico
        const result = await postItem(inputPatient, inputPreg, inputPlas, inputPres, inputSkin, inputTest, inputMass, inputPedi, inputAge);
          // Limpa o formulário
        document.getElementById("newInput").value = "";
        document.getElementById("newPreg").value = "";
        document.getElementById("newPlas").value = "";

        
        // Recarrega a lista completa para mostrar o novo paciente com o diagnóstico
        await refreshList();
        
        // Mostra mensagem de sucesso com o diagnóstico
        const diagnostico = result.outcome === 1 ? "DIABÉTICO" : "NÃO DIABÉTICO";
        alert(`Paciente adicionado com sucesso!\nDiagnóstico: ${diagnostico}`);
        
        // Scroll para a tabela para mostrar o novo resultado
        document.querySelector('.items').scrollIntoView({ 
          behavior: 'smooth', 
          block: 'center' 
        });
        
      } catch (error) {
        console.error('Adding error:', error);
        alert("Error. Try again.");
      }
    }
  })
  .catch((error) => {
    console.error('Error:', error);
    alert("Prediction error.");
  });
}

/*
      insertList(inputBook, inputAuthor, inputSynopsis)
      postItem(inputBook, inputAuthor, inputSynopsis)
      
      alert("Book added succefully!")
    }
  }
  */

  /*
    --------------------------------------------------------------------------------------
    Funcao para inserir os dados do formulário na tabela de id 'Tabela'. Também gera o botão de exclusão.
    --------------------------------------------------------------------------------------
  */

    function insertList(book, author, synopsis, genre) {
      // Selecionar a tabela HTML com id 'Tabela'
      const tabela = document.getElementById('Tabela');
    
      // Criar uma nova linha
      const linha = tabela.insertRow();
    
      // Criar células e adicionar os dados
      const cellBook = linha.insertCell();
      cellBook.textContent = book;
  
      const cellAuthor = linha.insertCell();
      cellAuthor.textContent = author;
    
      const cellSynopsis = linha.insertCell();
      cellSynopsis.textContent = synopsis;

  
      /*
      // Insere a célula do gênero
     const genreCell = row.insertCell(item.length);
     const diagnosticText = outcome === 1 ? "DIABÉTICO" : "NÃO DIABÉTICO";
     diagnosticCell.textContent = diagnosticText;
  
     // Aplica styling baseado no diagnóstico
     if (outcome === 1) {
     diagnosticCell.className = "diagnostic-positive";
     } else {
     diagnosticCell.className = "diagnostic-negative";
     }

    }

*/


-----------------------


const newItem = async (event) => { 

    // 1. Obter os dados dos inputs do livro
    let inputName = document.getElementById("newName").value.trim(); // ID do input para Título
    let inputAuthor = document.getElementById("newAuthor").value.trim(); // ID do input para Autor
    let inputSynopsis = document.getElementById("newSynopsis").value.trim(); // ID do input para Sinopse

    // 2. Lógica de Verificação de Duplicidade (Requer um endpoint API para listar livros por título)
   
    
    
    fetch(`http://127.0.0.1:5000/books?name=${encodeURIComponent(inputName)}`, {
        method: 'GET'
    })
    .then((response) => response.json())
    .then(async (data) => {
      
    if (inputName === '' || inputAuthor === '' || inputSynopsis === '') {
      alert("All the spaces must be filled!");
        } else {
            try {
                // 3. Enviar os dados para a API para previsão
                // A API /predict_batch espera uma lista de livros, então enviamos uma lista com um único item.
                const bookDataToSend = [{
                    name: inputName,
                    author: inputAuthor,
                    synopsis: inputSynopsis
                }];

                const response = await fetch('http://127.0.0.1:5000/predict_batch', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ books: bookDataToSend }) // Enviando como lista de um item
                });

                const result = await response.json();

                if (!response.ok) {
                    throw new Error(result.error || 'unidentified error.');
                }

                // Assume que 'result.results' é um array e pegamos o primeiro (e único) item
                const predictedGenre = result.results[0]?.predicted_genre || 'Not found genre';

                // 4. Limpar o formulário (inputs individuais)
                document.getElementById("newName").value = "";
                document.getElementById("newAuthor").value = "";
                document.getElementById("newSynopsis").value = "";
                

                alert(`Book added succefuly!`);
                
     
                
            } catch (error) {
                console.error('Error:', error);
                alert(`Error. Try again.\nDetails: ${error.message}`);
            }
        }
    })
    .catch((error) => {
        console.error('Error:', error);
        alert("Error. Try again");
    });
}