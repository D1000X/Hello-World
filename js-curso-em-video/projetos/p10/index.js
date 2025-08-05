let num = document.querySelector('input#fnum');
let lista = document.querySelector('select#flista');
let result = document.querySelector('div#res');

let numeros = [];

function anumero(n){
if(Number(n) >= 1 && Number(n) <= 100){
    return true
}else{
    return false
}
}
function inlista(n,l){
if(l.indexOf(Number(n)) != -1){
    return true
}else{
    return false
}
}

function adicionar(){
if(anumero(num.value) && !inlista(num.value,numeros)){
   numeros.push(Number(num.value))
   let item = document.createElement(`option`);
   item.text = `valor ${num.value} adicionado.`;
   lista.appendChild(item);
}else{
    window.alert('Valor invalido ou já adicionado na lista!')
}
num.value ='';
num.focus();
}
function mostrarRelatorio(){
    if(numeros.length == 0){
        window.alert('adicione valores antes de finalizar!')
    }else{
        result.innerHTML ='';
        let total = numeros.length;
        let maior = numeros[0];
        let menor = numeros[0];
        let soma = 0;
        let media = 0;
        for (let pos in numeros){
            soma += numeros[pos];
            if(numeros[pos]> maior){
                maior = numeros[pos];
            }
            if(numeros[pos]< menor){
                menor = numeros [pos];
            }
        }
        media = soma /total;
        result.innerHTML +=`<p> Ao todo, temos ${total} numeros cadastrados.</p>`;
        result.innerHTML +=`<p>O maior valor infromado foi ${maior}.</p>`;
        result.innerHTML +=`<p> O menor valor informado foi ${menor}.</p>`;
        result.innerHTML +=`<p> A soma de todos os valores é ${soma}.</p>`;
        result.innerHTML +=`<p> A media dos valores digitados é ${media}.</p>`;
    }
}