const express = require("express");
//constante com as configurações do express
const server = express();
//constante que vai receber o express
server.listen(8081,function() {
    console.log("O server está ON...")
});
//porta com listen para o servidor escutar
//estrutura base
// para inicializar o server usamos o comando node + nome do arquivo.

/*tentei usar ctrl + c para desligar o server mas não deu certo, então tive que desligar manualmente com o comando: Get-Process node , para conseguir ver o id do server , então usando o comando: Stop-Process -Id(Id do server aqui) -Force, assim consegui desligar o server com sucesso.*/