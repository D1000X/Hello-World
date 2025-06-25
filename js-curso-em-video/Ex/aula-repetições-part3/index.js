function contar () {
const inicio = document.getElementById('txti');
const fim = document.getElementById('txtf');
const passo = document.getElementById('txtp');
const res = document.getElementById('res');
if (inicio.value.length == 0 || fim.value.length == 0 || passo.value.length == 0) {
    res.innerHTML = 'Impossivel Contar'
    window.alert('[ERRO] faltam dados')  
} else{
    res.innerHTML = 'Contando: <br>'
    let i = Number(inicio.value)
    let f = Number(fim.value)
    let p = Number(passo.value)
    if(p<=0){
        window.alert('Passo invalido!')
    }
    if (i<f) {
        for (let c = i; c <= f; c += p){
            res.innerHTML += `${c}\u{1f449}`
        }
     }else{
        for(let c = i; c >= f; c -= p){
             res.innerHTML += `${c}\u{1f449}`
        }
             
     }
         res.innerHTML += `\u{1F3C1}`
 }
    
}

