function calcular() {
    let  txtv = window.document.querySelector('input#tvel')
    let res = window.document.querySelector('div#res')
    let vel =  Number(txtv.value)
        res.innerHTML = `<p>sua velocidade atual e de ${vel} </p>`
    if (vel>65) {
        res.innerHTML += `<p>Voce esta <strong>Multado</strong> por excesso de velocidade</p>`
    }
    res.innerHTML += `<p>Dirija sempre com cinto de seguraca</p>`
}