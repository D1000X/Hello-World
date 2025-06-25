let nome= window.prompt('digite seu nome:');
let peso= Number(window.prompt('digite seu peso:'));
let altura= Number(window.prompt('digite a sua altura'));
let imc= peso/ (altura**2);
let catg;
if (imc<18.5) {
    catg= 'abaixo do peso ideal';
} else if (imc >= 18.5 && imc<24.9) {
    catg='no peso ideal';
}else if (imc>=25 && imc<29.9 ) {
    catg='com sobre peso';
}else {
    catg= 'com obesidade';
}

window.alert(`olá, ${nome} com base na sua massa corporal de ${peso}kg e altura de ${altura} m,você esta ${catg} `)  