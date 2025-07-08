/*
  --------------------------------------------------------------------------------------
  Função para obter a lista existente do servidor via requisição GET
  --------------------------------------------------------------------------------------
*/
 const getList = async () => {
  
    fetch('http://localhost:5000/books', {method: 'GET',})

      .then(response => response.json())
      .then(data => {data.books.forEach(item => insertList(item.title, item.author, item.synopsis, item.genre))})
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
const postItem = async (inputTitle, inputAuthor, inputSynopsis) => {
  try {
    const response = await fetch('http://localhost:5000/predict', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        title: inputTitle,
        author: inputAuthor,
        synopsis: inputSynopsis
      })
    });

    if (!response.ok) {
      throw new Error(`Erro na requisição: ${response.statusText}`);
    }

    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Erro ao chamar postItem:', error);
    throw error;
  }
};

/*
  --------------------------------------------------------------------------------------
  Função para adicionar um novo item (livro) com titulo, autor, sinopse e gênero
  --------------------------------------------------------------------------------------
*/
const newItem = async (event) => {
 

 let inputTitle = document.getElementById("title").value; 
 let inputAuthor = document.getElementById("author").value;     
 let inputSynopsis = document.getElementById("synopsis").value; 


 const checkUrl = `http://127.0.0.1:5000/books?title=${inputTitle}`; 

   
    if (inputTitle === '') {
        alert("Title can not be empty!");
        return;
    }
    if (inputAuthor === '') {
        alert("Author can not be empty!");
        return;
    }
    if (inputSynopsis === '') {
        alert("Synopsis can not be empty!");
        return;
    }

    try {
       
      const result = await postItem(inputTitle, inputAuthor, inputSynopsis); 
        
        document.getElementById("title").value = "";
        document.getElementById("author").value = "";
        document.getElementById("synopsis").value = "";
        
        console.log("Data recieved:", result);

        insertList(result.title, result.author, result.synopsis, result.predicted_genre); 

        console.log("Resposta da API:", result);

        if (!result || !result.predicted_genre) {
        console.error("Genre not provided or field missing:", result);
        alert("Error predicting genre. Try again.");
        return;
        }
        
       
        alert(`Book added succefuly!\nPredicted Genre: ${result.predicted_genre}`);
        

        
    } catch (error) {
        console.error('Error adding book:', error);
        alert("Error adding book. Try again.");
    }
}



/*
  --------------------------------------------------------------------------------------
  Função para inserir livros na tabela com a criacao de uma linha
 
  --------------------------------------------------------------------------------------
*/
const insertList = (title, author, synopsis, predicted_genre) => {
 var item = [title, author, synopsis]; 
 var table = document.getElementById('Tabela');
 var row = table.insertRow(); 

 
 for (var i = 0; i < item.length; i++) {
  var cell = row.insertCell(i);
  cell.textContent = item[i];
 }
    

 var genreCell = row.insertCell(item.length); 
 genreCell.textContent = predicted_genre;

}
