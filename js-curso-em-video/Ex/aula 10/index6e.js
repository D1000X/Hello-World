let a = window.document.getElementById("area");
a.addEventListener("click",clicar)
a.addEventListener("mouseenter",entrar)
a.addEventListener("mouseout",sair)
function clicar() {
    let a = window.document.getElementById("area");
    a.innerText="clicou!";
    a.style.background = "red";
}
function entrar() {
    a.innerText = "entrou";
}
function sair() {
    a.innerText = "saiu";
    a.style.background = "green";
}