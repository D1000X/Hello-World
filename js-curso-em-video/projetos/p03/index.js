function gerar (){
let caracteres = ("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%&*");
let senha = ""; 

for (let i = 0 ; i < 8; i++){
    let indiceAleatorio = Math.floor(Math.random() * caracteres.length);
    let caracterisEscolhido = caracteres [indiceAleatorio];
    senha += caracterisEscolhido; 
}

document.getElementById("senha").textContent = senha;
}
document.getElementById("gerar").addEventListener("click",gerar)