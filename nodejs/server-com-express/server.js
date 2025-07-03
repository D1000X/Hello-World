const express = require("express");
//constante com as configurações do express
const server = express();
//constante que vai receber o express

// ROTA PRINCIPAL - Rota padrão do site (http://localhost:8081/)
server.get("/",function(req,res){
     // Envia uma mensagem de boas-vindas ao acessar a rota principal
    res.send("Seja Bem-vindo ao nosso site");
});

// ROTA DE ARTIGOS COM PARÂMETROS DINÂMICOS
// Essa rota espera dois valores na URL: ID do artigo e data de publicação
// Exemplo de URL válida: http://localhost:8081/artigos/1/18-05-2025
server.get("/artigos/:id/:data",function(req,res){
     // Captura os parâmetros id e data diretamente da URL
    if (req.params.id == "1" && req.params.data == "18-05-2025") {
         // Se o id for 1 e a data for a esperada, mostra o artigo 1
        res.send("1 - Como criar apps Android é IOS");
    } else if(req.params.id == "2"){
         // Se o id for 2, mostra o artigo 2
        res.send(" 2 - Como usar o node.js");
    }else{
        // Caso contrário, mostra mensagem de erro
        res.send("rota não encontrada!")
    }
    // OBS: Poderia ter usado req.params para capturar id e data separadamente:
    // const { id, data } = req.params;
});
// ROTA DE CONTATO - Página simples de contato (http://localhost:8081/contato)
server.get("/contato",function(req,res){
    res.send("Deixe sua mensagen aqui")
});


server.listen(8081,function() {
    console.log("O server está ON...")
});
//porta com listen para o servidor escutar
//estrutura base
// para inicializar o server usamos o comando node + nome do arquivo.

/*tentei usar ctrl + c para desligar o server mas não deu certo, então tive que desligar manualmente com o comando: Get-Process node , para conseguir ver o id do server , então usando o comando: Stop-Process -Id(Id do server aqui) -Force, assim consegui desligar o server com sucesso.*/