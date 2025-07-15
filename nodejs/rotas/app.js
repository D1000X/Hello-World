const express = require("express");
const app = express();
app.get("/",function (req,res) {
    res.send("Seja Bem-Vindo ao nosso site")
});
app.get("/artigos/:id",function(req,res) {
    if (req.params.id == "1") {
        res.send("1 - como criar aplicativos para android e IOS")
    } else if(req.params.id == "2"){
        res.send("2 - como criar programas e apps")
    }else{
        res.send("nelhum artigo foi encontrado!")
    }
})
app.listen(8081,function () {
    console.log("Servidor está On")
});