# Importa o módulo chamado 'name_space' e o apelida como 'ns' para facilitar o uso
import name_space as ns

# Importa todos os nomes públicos (funções, classes, variáveis, etc.) do módulo 'name_space'.
# Isso permite usar os elementos diretamente, sem precisar prefixar com 'name_space.'.
# Atenção: o uso de 'import *' pode causar conflitos de nomes e reduzir a legibilidade do código.
from name_space import *

# Importa apenas o objeto 'name_de_usuario' do módulo 'name_space'.
# Isso permite utilizar 'name_de_usuario' diretamente no código, sem precisar prefixar com 'name_space.'.
# Essa abordagem é mais segura e legível do que usar 'import *', pois evita conflitos de nomes e deixa claro o que está sendo utilizado.
from name_space import name_de_usuario

# Imprime o valor da variável 'name_de_usuario' que está definida dentro do módulo 'name_space'
print(ns.name_de_usuario)

# Cria uma variável chamada 'mensagem' e atribui a ela uma string
mensagem = " ou você quer o peitinho do galego?"

# Chama a função 'funcao_do_name' que está dentro do módulo 'name_space',
# passando a variável 'mensagem' como argumento
ns.funcao_do_name(mensagem)