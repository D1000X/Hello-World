function carregar () {
    let msg = window.document.getElementById('msg');
    let foto = window.document.getElementById('imagen');
    let data = new Date();
    let hora = data.getHours();
    //let hora = 20

    msg.innerText = `Agora são ${hora} horas.`;
    if (hora>= 5 && hora < 12)  {
        //bom dia
        foto.src ='img/manha.jpg';
        document.body.style.background ='#e2cd9f';
    } else if (hora >= 12 && hora < 18) {
        //boa tarde
        foto.src ='img/tarde.jpg';
        document.body.style.background ='#f2b066';
    } else if(hora >=18 && hora < 23){
        //boa noite
        foto.src ='img/noite.jpg';
        document.body.style.background ='#4b4d63';

    }else {
        //boa madrugada
        foto.src ='img/madrugada.jpg';
        document.bady,style.background ='#00008B.'
    }
} 