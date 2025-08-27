import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
from datetime import datetime

# --- Funções de Manipulação de Dados (JSON) ---

def carregar_estoque():
    """Carrega o estoque do arquivo JSON."""
    if os.path.exists("estoque.json"):
        try:
            with open("estoque.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo: {e}")
    return []

def salvar_estoque(estoque):
    """Salva o estoque no arquivo JSON."""
    try:
        with open("estoque.json", "w", encoding="utf-8") as f:
            json.dump(estoque, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")

def fazer_backup():
    """Cria backup automático do estoque."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"estoque_backup_{timestamp}.json"
    try:
        with open(backup_name, "w", encoding="utf-8") as f:
            json.dump(estoque, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Sucesso", f"Backup criado: {backup_name}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar backup: {e}")

# --- Funções da Interface ---

def validar_entrada(nome, quantidade_str, unidade, categoria, limite_str):
    """Valida os dados de entrada."""
    erros = []
    
    if not nome.strip():
        erros.append("Nome é obrigatório")
    elif len(nome.strip()) > 100:
        erros.append("Nome muito longo (máximo 100 caracteres)")
    
    if not quantidade_str.strip():
        erros.append("Quantidade é obrigatória")
    else:
        try:
            qtd = int(quantidade_str)
            if qtd < 0:
                erros.append("Quantidade não pode ser negativa")
        except ValueError:
            erros.append("Quantidade deve ser um número inteiro")
    
    if not unidade.strip():
        erros.append("Unidade é obrigatória")
    
    if not categoria.strip():
        erros.append("Categoria é obrigatória")
    
    if limite_str.strip():
        try:
            limite = int(limite_str)
            if limite < 0:
                erros.append("Limite de alerta não pode ser negativo")
        except ValueError:
            erros.append("Limite de alerta deve ser um número inteiro")
    
    return erros

def adicionar_item():
    """Adiciona um novo item ao estoque."""
    nome = entry_nome.get().strip()
    quantidade_str = entry_quantidade.get().strip()
    unidade = entry_unidade.get().strip()
    categoria = combo_categoria.get().strip()
    limite_str = entry_limite.get().strip()

    # Validação
    erros = validar_entrada(nome, quantidade_str, unidade, categoria, limite_str)
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return

    # Verificar se item já existe
    for item in estoque:
        if item["nome"].lower() == nome.lower():
            messagebox.showerror("Erro", "Item já existe no estoque!")
            return

    try:
        quantidade = int(quantidade_str)
        limite = int(limite_str) if limite_str else 0
    except ValueError:
        return

    item = {
        "nome": nome,
        "quantidade": quantidade,
        "unidade": unidade,
        "categoria": categoria,
        "limite_alerta": limite,
        "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    estoque.append(item)
    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    atualizar_contador_itens()
    messagebox.showinfo("Sucesso", "Item adicionado com sucesso!")

def remover_item():
    """Remove o item selecionado do estoque."""
    selecao = tree.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um item para remover.")
        return

    # Confirmação
    resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja remover este item?")
    if not resposta:
        return

    item_selecionado = selecao[0]
    index_item = tree.index(item_selecionado)
    
    nome_item = estoque[index_item]["nome"]
    estoque.pop(index_item)
    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    atualizar_contador_itens()
    messagebox.showinfo("Sucesso", f"Item '{nome_item}' removido com sucesso!")

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
    entry_quantidade.insert(0, str(item_data.get("quantidade", "")))
    entry_unidade.insert(0, item_data.get("unidade", ""))
    combo_categoria.set(item_data.get("categoria", ""))
    entry_limite.insert(0, str(item_data.get("limite_alerta", "")))

def editar_item():
    """Edita as informações do item selecionado."""
    selecao = tree.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um item para editar.")
        return

    item_selecionado = selecao[0]
    index_item = tree.index(item_selecionado)

    nome = entry_nome.get().strip()
    quantidade_str = entry_quantidade.get().strip()
    unidade = entry_unidade.get().strip()
    categoria = combo_categoria.get().strip()
    limite_str = entry_limite.get().strip()

    # Validação
    erros = validar_entrada(nome, quantidade_str, unidade, categoria, limite_str)
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return

    try:
        quantidade = int(quantidade_str)
        limite = int(limite_str) if limite_str else 0
    except ValueError:
        return

    estoque[index_item]["nome"] = nome
    estoque[index_item]["quantidade"] = quantidade
    estoque[index_item]["unidade"] = unidade
    estoque[index_item]["categoria"] = categoria
    estoque[index_item]["limite_alerta"] = limite
    estoque[index_item]["data_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    atualizar_contador_itens()
    messagebox.showinfo("Sucesso", "Item editado com sucesso!")
    
def limpar_campos():
    """Limpa os campos de entrada de texto."""
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_unidade.delete(0, tk.END)
    combo_categoria.set('')
    entry_limite.delete(0, tk.END)
    entry_busca.delete(0, tk.END)

def buscar_item():
    """Busca itens por nome ou categoria."""
    termo = entry_busca.get().strip().lower()
    
    # Limpa a tabela
    for item in tree.get_children():
        tree.delete(item)
    
    # Se não há termo de busca, mostra tudo
    if not termo:
        atualizar_lista()
        return
    
    # Filtra e adiciona itens que correspondem à busca
    for item in estoque:
        if (termo in item["nome"].lower() or 
            termo in item["categoria"].lower()):
            limite = item.get("limite_alerta", 0)
            if item["quantidade"] <= limite:
                tree.insert("", tk.END, 
                          values=(item["nome"], item["quantidade"], 
                                item["unidade"], item["categoria"]), 
                          tags=('baixo_estoque',))
            else:
                tree.insert("", tk.END, 
                          values=(item["nome"], item["quantidade"], 
                                item["unidade"], item["categoria"]))

def atualizar_lista():
    """Atualiza a lista de itens na tabela com alerta visual."""
    for item in tree.get_children():
        tree.delete(item)
    
    for item in estoque:
        limite = item.get("limite_alerta", 0)
        if item["quantidade"] <= limite:
            tree.insert("", tk.END, 
                      values=(item["nome"], item["quantidade"], 
                            item["unidade"], item["categoria"]), 
                      tags=('baixo_estoque',))
        else:
            tree.insert("", tk.END, 
                      values=(item["nome"], item["quantidade"], 
                            item["unidade"], item["categoria"]))

def atualizar_contador_itens():
    """Atualiza o contador de itens na interface."""
    total_produtos = len(estoque)
    total_quantidade = sum(item["quantidade"] for item in estoque)
    
    # Conta itens com estoque baixo
    itens_baixo_estoque = 0
    for item in estoque:
        if item["quantidade"] <= item.get("limite_alerta", 0):
            itens_baixo_estoque += 1
    
    label_contador.config(
        text=f"Total: {total_produtos} produtos | Quantidade total: {total_quantidade} unidades | Alertas: {itens_baixo_estoque}"
    )

def gerar_relatorio():
    """Gera e exibe um relatório de estoque em uma nova janela."""
    relatorio = tk.Toplevel(root)
    relatorio.title("Relatório de Estoque")
    relatorio.geometry("700x500")

    # Frame com scrollbar
    frame_scroll = tk.Frame(relatorio)
    frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)
    
    scrollbar = tk.Scrollbar(frame_scroll)
    scrollbar.pack(side="right", fill="y")
    
    text_relatorio = tk.Text(frame_scroll, wrap="word", yscrollcommand=scrollbar.set,
                           font=("Arial", 10))
    text_relatorio.pack(fill="both", expand=True)
    scrollbar.config(command=text_relatorio.yview)

    # Configurar tags para formatação
    text_relatorio.tag_configure("titulo", font=("Arial", 14, "bold"))
    text_relatorio.tag_configure("categoria", font=("Arial", 12, "bold"), foreground="blue")
    text_relatorio.tag_configure("alerta", foreground="red", font=("Arial", 10, "bold"))

    categorias_estoque = {}
    total_itens = 0
    total_produtos = len(estoque)
    itens_baixo_estoque = []

    for item in estoque:
        categoria = item["categoria"]
        if categoria not in categorias_estoque:
            categorias_estoque[categoria] = []
        categorias_estoque[categoria].append(item)
        total_itens += item["quantidade"]
        
        # Verificar se está com estoque baixo
        if item["quantidade"] <= item.get("limite_alerta", 0):
            itens_baixo_estoque.append(item)

    # Gerar relatório
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    text_relatorio.insert(tk.END, f"=== RELATÓRIO DE ESTOQUE ===\n", ("titulo",))
    text_relatorio.insert(tk.END, f"Gerado em: {data_atual}\n\n")
    
    text_relatorio.insert(tk.END, "📊 RESUMO GERAL\n", ("categoria",))
    text_relatorio.insert(tk.END, f"• Total de produtos cadastrados: {total_produtos}\n")
    text_relatorio.insert(tk.END, f"• Quantidade total em estoque: {total_itens} unidades\n")
    text_relatorio.insert(tk.END, f"• Itens com estoque baixo: {len(itens_baixo_estoque)}\n\n")

    # Alertas de estoque baixo
    if itens_baixo_estoque:
        text_relatorio.insert(tk.END, "⚠  ALERTAS DE ESTOQUE BAIXO\n", ("alerta",))
        for item in itens_baixo_estoque:
            text_relatorio.insert(tk.END, 
                f"• {item['nome']}: {item['quantidade']} {item['unidade']} "
                f"(Limite: {item.get('limite_alerta', 0)})\n", ("alerta",))
        text_relatorio.insert(tk.END, "\n")

    # Por categoria
    text_relatorio.insert(tk.END, "📦 DETALHAMENTO POR CATEGORIA\n\n", ("categoria",))
    for categoria, itens in sorted(categorias_estoque.items()):
        text_relatorio.insert(tk.END, f"--- {categoria.upper()} ---\n", ("categoria",))
        qtd_categoria = sum(item["quantidade"] for item in itens)
        text_relatorio.insert(tk.END, f"Total na categoria: {qtd_categoria} unidades\n")
        
        for item in sorted(itens, key=lambda x: x['nome']):
            status = " ⚠" if item["quantidade"] <= item.get("limite_alerta", 0) else ""
            text_relatorio.insert(tk.END, 
                f"  • {item['nome']}: {item['quantidade']} {item['unidade']}{status}\n")
        text_relatorio.insert(tk.END, "\n")
    
    text_relatorio.config(state=tk.DISABLED)

def exportar_csv():
    """Exporta o estoque para um arquivo CSV."""
    if not estoque:
        messagebox.showwarning("Aviso", "Não há itens para exportar.")
        return
    
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", ".csv"), ("All files", ".*")],
        title="Salvar arquivo CSV"
    )
    
    if not arquivo:
        return
    
    try:
        with open(arquivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Nome", "Quantidade", "Unidade", "Categoria", "Limite Alerta", "Data Cadastro"])
            for item in estoque:
                writer.writerow([
                    item["nome"], 
                    item["quantidade"], 
                    item["unidade"], 
                    item["categoria"],
                    item.get("limite_alerta", 0),
                    item.get("data_cadastro", "N/A")
                ])
        messagebox.showinfo("Sucesso", f"Dados exportados para: {arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar: {e}")

# --- Configuração da Janela Principal ---

root = tk.Tk()
root.title("Controle de Estoque - Versão 2.0")
root.geometry("900x700")
root.configure(bg="#f0f0f0")

# --- Carregar Dados Iniciais ---
estoque = carregar_estoque()

# --- Configuração de Estilos ---
style = ttk.Style()
style.theme_use('clam')  # Tema mais moderno

# Configurar estilo da Treeview
style.configure("Treeview", 
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white")

style.configure("Treeview.Heading",
                background="#4472C4",
                foreground="white",
                font=('Arial', 10, 'bold'))

style.map("Treeview",
          background=[('selected', '#4472C4')],
          foreground=[('selected', 'white')])

# --- Frame Principal ---
main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

# --- Título ---
title_frame = tk.Frame(main_frame, bg="#f0f0f0")
title_frame.pack(fill="x", pady=(0, 20))

title_label = tk.Label(title_frame, text="🏪 CONTROLE DE ESTOQUE", 
                      font=("Arial", 18, "bold"), 
                      bg="#f0f0f0", fg="#2c3e50")
title_label.pack()

# --- Frame para os Controles de Entrada ---
frame_controle = tk.LabelFrame(main_frame, text="📝 Dados do Produto", 
                              font=("Arial", 10, "bold"), 
                              bg="#f0f0f0", fg="#2c3e50")
frame_controle.pack(fill="x", pady=(0, 10))

# Layout em grid mais organizado
tk.Label(frame_controle, text="Nome:", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_nome = tk.Entry(frame_controle, width=40, font=("Arial", 10))
entry_nome.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Quantidade:", bg="#f0f0f0").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
entry_quantidade = tk.Entry(frame_controle, width=20, font=("Arial", 10))
entry_quantidade.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_controle, text="Unidade:", bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_unidade = tk.Entry(frame_controle, width=40, font=("Arial", 10))
entry_unidade.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Limite de Alerta:", bg="#f0f0f0").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
entry_limite = tk.Entry(frame_controle, width=20, font=("Arial", 10))
entry_limite.grid(row=1, column=3, padx=5, pady=5)

tk.Label(frame_controle, text="Categoria:", bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
categorias = ["Alimentos", "Limpeza", "Higiene Pessoal", "Medicamentos", "Eletrônicos", "Roupas", "Outros"]
combo_categoria = ttk.Combobox(frame_controle, values=categorias, width=37, font=("Arial", 10))
combo_categoria.grid(row=2, column=1, padx=5, pady=5)

# --- Frame para Busca ---
frame_busca = tk.LabelFrame(main_frame, text="🔍 Buscar Produtos", 
                           font=("Arial", 10, "bold"), 
                           bg="#f0f0f0", fg="#2c3e50")
frame_busca.pack(fill="x", pady=(0, 10))

tk.Label(frame_busca, text="Buscar:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
entry_busca = tk.Entry(frame_busca, width=40, font=("Arial", 10))
entry_busca.pack(side=tk.LEFT, padx=5)
entry_busca.bind('<KeyRelease>', lambda event: buscar_item())

botao_limpar_busca = tk.Button(frame_busca, text="Limpar", command=lambda: (entry_busca.delete(0, tk.END), atualizar_lista()))
botao_limpar_busca.pack(side=tk.LEFT, padx=5)

# --- Frame para os Botões de Ação ---
frame_botoes = tk.Frame(main_frame, bg="#f0f0f0")
frame_botoes.pack(fill="x", pady=(0, 10))

# Botões com cores e ícones
botao_adicionar = tk.Button(frame_botoes, text="➕ Adicionar", command=adicionar_item, 
                           bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=12)
botao_adicionar.pack(side=tk.LEFT, padx=3)

botao_editar = tk.Button(frame_botoes, text="✏ Editar", command=editar_item, 
                        bg="#f39c12", fg="white", font=("Arial", 10, "bold"), width=12)
botao_editar.pack(side=tk.LEFT, padx=3)

botao_remover = tk.Button(frame_botoes, text="🗑 Remover", command=remover_item, 
                         bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=12)
botao_remover.pack(side=tk.LEFT, padx=3)

botao_limpar = tk.Button(frame_botoes, text="🧹 Limpar", command=limpar_campos, 
                        bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), width=12)
botao_limpar.pack(side=tk.LEFT, padx=3)

botao_relatorio = tk.Button(frame_botoes, text="📊 Relatório", command=gerar_relatorio, 
                           bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=12)
botao_relatorio.pack(side=tk.LEFT, padx=3)

botao_backup = tk.Button(frame_botoes, text="💾 Backup", command=fazer_backup, 
                        bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), width=12)
botao_backup.pack(side=tk.LEFT, padx=3)

botao_exportar = tk.Button(frame_botoes, text="📤 Exportar CSV", command=exportar_csv, 
                          bg="#1abc9c", fg="white", font=("Arial", 10, "bold"), width=12)
botao_exportar.pack(side=tk.LEFT, padx=3)

# --- Frame para a tabela ---
frame_tabela = tk.LabelFrame(main_frame, text="📋 Lista de Produtos", 
                            font=("Arial", 10, "bold"), 
                            bg="#f0f0f0", fg="#2c3e50")
frame_tabela.pack(fill="both", expand=True, pady=(0, 10))

# --- Label para contador de itens ---
label_contador = tk.Label(main_frame, text="", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#2c3e50")
label_contador.pack(fill="x", pady=(0, 10))

# Tabela com scrollbar
frame_tree = tk.Frame(frame_tabela)
frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("nome", "quantidade", "unidade", "categoria")
tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=15)

# Configurar colunas
tree.heading("nome", text="Nome do Produto")
tree.heading("quantidade", text="Quantidade")
tree.heading("unidade", text="Unidade")
tree.heading("categoria", text="Categoria")

tree.column("nome", width=300, anchor="w")
tree.column("quantidade", width=100, anchor="center")
tree.column("unidade", width=100, anchor="center")
tree.column("categoria", width=150, anchor="center")

# Scrollbars
scrollbar_v = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
scrollbar_h = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)

tree.pack(side="left", fill="both", expand=True)
scrollbar_v.pack(side="right", fill="y")
scrollbar_h.pack(side="bottom", fill="x")

# CORREÇÃO: Configurar tag para estoque baixo DEPOIS de criar a tree
tree.tag_configure('baixo_estoque', background='#ffcccc', foreground='red')

tree.bind("<<TreeviewSelect>>", carregar_para_edicao)

# ---
# ...existing code...

# Atualiza a lista e contador ao iniciar
atualizar_lista()
atualizar_contador_itens()

# Inicia o loop principal do Tkinter
root.mainloop()