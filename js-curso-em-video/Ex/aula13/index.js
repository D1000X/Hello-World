let agora = new Date()
let hora = agora.getHours()
console.log(`São exatamente ${hora} horas`)
if (hora<=5) {
    console.log('Boa madrugada')
}else if (hora<=12) {
    console.log('Bom dia men')
}else if (hora<=18) {
    console.log('Boa tarde')
}else{
    console.log('Boa noite')
}