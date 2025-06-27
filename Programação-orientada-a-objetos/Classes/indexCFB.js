class Carro{
    constructor(modelo, cor, ano, motor){
    this.modelo = modelo;    
    this.cor = cor;
    this.ano = ano;
    this.motor = motor;
    }
    descrever(){
        return `Carro bem conservado, com design moderno e ótimo desempenho. Modelo ${this.modelo}, cor ${this.cor}, ano ${this.ano}, motor ${this.motor}. Ideal para o dia a dia, oferecendo conforto, economia e segurança. Documentação em dia e pronto para rodar.`;
    }
}

let c1 = new Carro("Ford Ka","branco", "2018","1.0");
let c2 = new Carro("Honda Civic","cinza","2021","2.0");
let c3 = new Carro("Renault Kwid","vermelho","2022","1.0");
let c4 = new Carro("Volkswagen Saveiro","prata","2019","1.6");

console.log(c1.descrever());
console.log(c2.descrever());
console.log(c3.descrever());
console.log(c4.descrever());