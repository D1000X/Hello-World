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
    nome = entry_nome.get().strip()
    quantidade_str = entry_quantidade.get().strip()
    unidade = entry_unidade.get().strip()
    categoria = combo_categoria.get().strip()
    limite_str = entry_limite.get().strip()

    if not nome or not quantidade_str or not unidade or not categoria:
        messagebox.showerror("Erro", "Campos Nome, Quantidade, Unidade e Categoria são obrigatórios.")
        return

    try:
        quantidade = int(quantidade_str)
        limite = int(limite_str) if limite_str else 0
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e Limite de Alerta devem ser números inteiros.")
        return

    item = {
        "nome": nome,
        "quantidade": quantidade,
        "unidade": unidade,
        "categoria": categoria,
        "limite_alerta": limite
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
    index_item = tree.index(item_selecionado)
    item_data = estoque[index_item]

    limpar_campos()
    entry_nome.insert(0, item_data.get("nome", ""))
    entry_quantidade.insert(0, item_data.get("quantidade", ""))
    entry_unidade.insert(0, item_data.get("unidade", ""))
    combo_categoria.set(item_data.get("categoria", ""))
    entry_limite.insert(0, item_data.get("limite_alerta", ""))

def editar_item():
    """Edita as informações do item selecionado."""
    selecao = tree.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um item para editar.")
        return

    item_selecionado = selecao[0]
    index_item = tree.index(item_selecionado)

    novo_nome = entry_nome.get().strip()
    nova_quantidade_str = entry_quantidade.get().strip()
    nova_unidade = entry_unidade.get().strip()
    nova_categoria = combo_categoria.get().strip()
    novo_limite_str = entry_limite.get().strip()

    if not novo_nome or not nova_quantidade_str or not nova_unidade or not nova_categoria:
        messagebox.showerror("Erro", "Campos Nome, Quantidade, Unidade e Categoria são obrigatórios.")
        return

    try:
        nova_quantidade = int(nova_quantidade_str)
        novo_limite = int(novo_limite_str) if novo_limite_str else 0
    except ValueError:
        messagebox.showerror("Erro", "Quantidade e Limite de Alerta devem ser números inteiros.")
        return

    estoque[index_item]["nome"] = novo_nome
    estoque[index_item]["quantidade"] = nova_quantidade
    estoque[index_item]["unidade"] = nova_unidade
    estoque[index_item]["categoria"] = nova_categoria
    estoque[index_item]["limite_alerta"] = novo_limite

    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    
def limpar_campos():
    """Limpa os campos de entrada de texto."""
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_unidade.delete(0, tk.END)
    combo_categoria.set('')
    entry_limite.delete(0, tk.END)

def atualizar_lista():
    """Atualiza a lista de itens na tabela com alerta visual."""
    for item in tree.get_children():
        tree.delete(item)
    
    for item in estoque:
        limite = item.get("limite_alerta", 0)  # Pega o limite, com 0 como padrão se não existir
        if item["quantidade"] <= limite:
            tree.insert("", tk.END, values=(item["nome"], item["quantidade"], item["unidade"], item["categoria"]), tags=('baixo_estoque',))
        else:
            tree.insert("", tk.END, values=(item["nome"], item["quantidade"], item["unidade"], item["categoria"]))

def gerar_relatorio():
    """Gera e exibe um relatório de estoque em uma nova janela."""
    relatorio = tk.Toplevel(root)
    relatorio.title("Relatório de Estoque")
    relatorio.geometry("600x400")

    categorias_estoque = {}
    total_itens = 0

    for item in estoque:
        categoria = item["categoria"]
        if categoria not in categorias_estoque:
            categorias_estoque[categoria] = []
        categorias_estoque[categoria].append(item)
        total_itens += item["quantidade"]

    text_relatorio = tk.Text(relatorio, wrap="word", padx=10, pady=10)
    text_relatorio.pack(fill="both", expand=True)

    text_relatorio.insert(tk.END, "--- Relatório Geral de Estoque ---\n\n", ("titulo",))
    text_relatorio.insert(tk.END, f"Total de itens no estoque (em unidades): {total_itens}\n\n", ("normal",))

    for categoria, itens in categorias_estoque.items():
        text_relatorio.insert(tk.END, f"--- Categoria: {categoria} ---\n", ("categoria",))
        for item in itens:
            text_relatorio.insert(tk.END, f"  - {item['nome']}: {item['quantidade']} {item['unidade']}\n")
        text_relatorio.insert(tk.END, "\n")
    
    text_relatorio.config(state=tk.DISABLED)

# --- Configuração da Janela Principal ---

root = tk.Tk()
root.title("Controle de Estoque")
root.geometry("800x600")

# --- Carregar Dados Iniciais ---

estoque = carregar_estoque()

# --- Configuração de Estilos para o Alerta ---
style = ttk.Style()
style.configure("Treeview", rowheight=25)
style.map("Treeview",
          background=[('selected', 'blue')],
          foreground=[('selected', 'white')])

style.configure("baixo_estoque", foreground="red")

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

tk.Label(frame_controle, text="Limite de Alerta:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
entry_limite = tk.Entry(frame_controle, width=40)
entry_limite.grid(row=4, column=1, padx=5, pady=5)

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

botao_relatorio = tk.Button(frame_botoes, text="Gerar Relatório", command=gerar_relatorio)
botao_relatorio.pack(side=tk.LEFT, padx=5)

# --- Tabela para a Lista de Itens (TreeView) ---

columns = ("nome", "quantidade", "unidade", "categoria")
tree = ttk.Treeview(root, columns=columns, show='headings')
tree.heading("nome", text="Nome")
tree.heading("quantidade", text="Quantidade")
tree.heading("unidade", text="Unidade")
tree.heading("categoria", text="Categoria")
tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

tree.bind("<<TreeviewSelect>>", carregar_para_edicao)

# --- Atualizar a lista inicial e iniciar o loop da GUI ---

atualizar_lista()
root.mainloop()