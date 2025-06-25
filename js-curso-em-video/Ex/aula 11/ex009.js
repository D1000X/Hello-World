function verificar() {
    let text=window.document.getElementById('inputx')
    let res= window.document.getElementById('res')
    let val=text.value.trim()
    let pais= 'Brasil'
 res.innerHTML =`<p>Olá, entâo o seu pais de origen é ${val}.</p>`
   if (val.toLowerCase()===pais.toLowerCase()) {
        res.innerHTML += `<p> Você é Brasileiro</p> `
   } else {
        res.innerHTML += `<p> Você é Estrangeiro</p>`
   }
}
    