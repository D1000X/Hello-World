//exemplo de objeto.
//os valores dentro  de um objeto são chamados propriedades.
 const carro = {
    marca:"ford",
    modelo:"Ka",
    ano:"2015" ,
     placa:"72H7P8",

    buzina: function(){
      console.log("Biiiiiiiiii")},
    
    completo:function(){
        return`A marca é ${this.marca}, o modelo é ${this.modelo}`
    }};
    console.log(carro.completo())
    
   console.log(carro.buzina());
// Objetos também podem ter metodos, Um método e uma função colocada dentro de uma propriedade.
