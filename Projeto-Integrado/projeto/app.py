import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- Funções de Manipulação de Dados (JSON) ---

def carregar_estoque():
    """Carrega o estoque do arquivo JSON."""
    if os.path.exists("estoque.json"):
        with open("estoque.json", "r") as f:
            return json.load(f)
    return []

def salvar_estoque(estoque):
    """Salva o estoque no arquivo JSON."""
    with open("estoque.json", "w") as f:
        json.dump(estoque, f, indent=4)

# --- Funções da Interface ---

def adicionar_item():
    """Adiciona um novo item ao estoque."""
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    unidade = entry_unidade.get()
    categoria = combo_categoria.get()

    if not nome or not quantidade or not unidade or not categoria:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    try:
        quantidade = int(quantidade)
    except ValueError:
        messagebox.showerror("Erro", "A quantidade deve ser um número inteiro.")
        return

    item = {
        "nome": nome,
        "quantidade": quantidade,
        "unidade": unidade,
        "categoria": categoria
    }
    
    estoque.append(item)
    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()

def remover_item():
    """Remove o item selecionado do estoque."""
    selecao = tree.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um item para remover.")
        return

    item_selecionado = selecao[0]
    index_item = tree.index(item_selecionado)
    
    estoque.pop(index_item)
    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()

def carregar_para_edicao(event):
    """Carrega os dados do item selecionado para os campos de entrada."""
    selecao = tree.selection()
    if not selecao:
        return
    
    item_selecionado = selecao[0]
    valores = tree.item(item_selecionado, 'values')

    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, valores[0])
    
    entry_quantidade.delete(0, tk.END)
    entry_quantidade.insert(0, valores[1])

    entry_unidade.delete(0, tk.END)
    entry_unidade.insert(0, valores[2])

    combo_categoria.set(valores[3])

def editar_item():
    """Edita as informações do item selecionado."""
    selecao = tree.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um item para editar.")
        return

    item_selecionado = selecao[0]
    index_item = tree.index(item_selecionado)

    novo_nome = entry_nome.get()
    nova_quantidade = entry_quantidade.get()
    nova_unidade = entry_unidade.get()
    nova_categoria = combo_categoria.get()

    if not novo_nome or not nova_quantidade or not nova_unidade or not nova_categoria:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    try:
        nova_quantidade = int(nova_quantidade)
    except ValueError:
        messagebox.showerror("Erro", "A quantidade deve ser um número inteiro.")
        return

    estoque[index_item]["nome"] = novo_nome
    estoque[index_item]["quantidade"] = nova_quantidade
    estoque[index_item]["unidade"] = nova_unidade
    estoque[index_item]["categoria"] = nova_categoria

    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    
def limpar_campos():
    """Limpa os campos de entrada de texto."""
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_unidade.delete(0, tk.END)
    combo_categoria.set('') # Limpa o combobox

def atualizar_lista():
    """Atualiza a lista de itens na tabela."""
    for item in tree.get_children():
        tree.delete(item)
    
    for item in estoque:
        tree.insert("", tk.END, values=(item["nome"], item["quantidade"], item["unidade"], item["categoria"]))

# --- Configuração da Janela Principal ---

root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("800x600")

# --- Carregar Dados Iniciais ---

estoque = carregar_estoque()

# --- Frame para os Controles de Entrada ---
frame_controle = tk.Frame(root, padx=10, pady=10)
frame_controle.pack(pady=10)

tk.Label(frame_controle, text="Nome:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_nome = tk.Entry(frame_controle, width=40)
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Quantidade:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_quantidade = tk.Entry(frame_controle, width=40)
entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Unidade:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
entry_unidade = tk.Entry(frame_controle, width=40)
entry_unidade.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Categoria:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
categorias = ["Alimentos", "Limpeza", "Higiene Pessoal"]
combo_categoria = ttk.Combobox(frame_controle, values=categorias, width=37)
combo_categoria.grid(row=3, column=1, padx=5, pady=5)

# --- Frame para os Botões de Ação ---

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=5)

botao_adicionar = tk.Button(frame_botoes, text="Adicionar Item", command=adicionar_item)
botao_adicionar.pack(side=tk.LEFT, padx=5)

botao_editar = tk.Button(frame_botoes, text="Editar Item", command=editar_item)
botao_editar.pack(side=tk.LEFT, padx=5)

botao_remover = tk.Button(frame_botoes, text="Remover Item", command=remover_item)
botao_remover.pack(side=tk.LEFT, padx=5)

botao_limpar = tk.Button(frame_botoes, text="Limpar Campos", command=limpar_campos)
botao_limpar.pack(side=tk.LEFT, padx=5)

# --- Tabela para a Lista de Itens (TreeView) ---

columns = ("nome", "quantidade", "unidade", "categoria")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("nome", text="Nome")
tree.heading("quantidade", text="Quantidade")
tree.heading("unidade", text="Unidade")
tree.heading("categoria", text="Categoria")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Vincula a função de carregamento aos cliques do mouse na tabela
tree.bind("<<TreeviewSelect>>", carregar_para_edicao)

# --- Atualizar a lista inicial e iniciar o loop da GUI ---

atualizar_lista()
root.mainloop()