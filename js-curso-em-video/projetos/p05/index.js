let paragrafo = document.getElementById("para");
let botaomais = document.getElementById("mais");
let botaomenos = document.getElementById("menos");
let contador = 0;

botaomais.addEventListener("click", function () {
    contador++;
    paragrafo.textContent=contador;
});
botaomenos.addEventListener("click", function() {
    contador--;
    paragrafo.textContent=contador;
});