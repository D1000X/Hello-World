class Livro {
    //Isso é uma classe. Tipo uma receita de bolo, saca? Ela define o que todo "livro" vai ter — título, autor, ano...

    constructor(titulo, autor, ano) {
        this.titulo = titulo;
        this.autor = autor;
        this.ano = ano;
     //O constructor é um método especial que é executado automaticamente quando um novo objeto é criado com new Livro(...).ele Atribui os valores recebidos aos atributos do objeto.
    }
    detalhes () {
        return `O livro ${this.titulo} foi escrito pelo autor ${this.autor} em ${this.ano}.`
        //Esse é um método da classe ele retorna uma mensagem descritiva sobre o livro atual.

    }
}
    const livro1= new Livro("O Selhor dos Aneis part 1","J.R.R. Tolkien","29 de julho de 1954");
    const livro2 = new Livro("Misery: louca obsessão","Stephen King","8 de junho de 1987")
    const livro3 = new Livro("Carrie","Stephen King","5 de abril de 1974")
    // Aqui você está usando a palavra-chave new para criar um novo objeto da classe Livro, os livros agora são objetos independentes, com seus próprios valores para título, autor e ano.

    console.log(livro1.detalhes());
    console.log(livro2.detalhes());
    console.log(livro3.detalhes());