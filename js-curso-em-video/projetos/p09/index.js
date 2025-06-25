function tabuada() {
    let num =  document.getElementById('txtn');
    let tab = document.getElementById('seltab')
    if (num.value.length == 0) {
       window.alert('por favor, digite um número!!!')
    }else{
    let n = Number(num.value)
    let c = 1
    tab.innerHTML = ''
    while (c <= 10) {
        let iten = document.createElement('option')
        iten.text = `${n}X${c} = ${n*c}`
        tab.appendChild(iten)
        c++
    } 
    }  
}
     