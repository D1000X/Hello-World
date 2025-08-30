import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
from datetime import datetime

# --- Funções de Manipulação de Dados (JSON) ---

def carregar_estoque():
    if os.path.exists("estoque.json"):
        try:
            with open("estoque.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar arquivo: {e}")
    return []

def salvar_estoque(estoque):
    try:
        with open("estoque.json", "w", encoding="utf-8") as f:
            json.dump(estoque, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")

def fazer_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"estoque_backup_{timestamp}.json"
    try:
        with open(backup_name, "w", encoding="utf-8") as f:
            json.dump(estoque, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Sucesso", f"Backup criado: {backup_name}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar backup: {e}")

# --- Validação EAN-13 ---
def validar_ean13(ean):
    if len(ean) != 13 or not ean.isdigit():
        return False
    soma = sum(int(ean[i]) if i % 2 == 0 else int(ean[i]) * 3 for i in range(12))
    digito = (10 - (soma % 10)) % 10
    return digito == int(ean[-1])

# --- Funções da Interface ---

def validar_entrada(nome, quantidade_str, unidade, categoria, limite_str, preco_custo_str, preco_venda_str, fornecedor, data_validade, codigo_barras):
    erros = []
    if not nome.strip():
        erros.append("Nome é obrigatório")
    elif len(nome.strip()) > 100:
        erros.append("Nome muito longo (máx 100 caracteres)")
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
    try:
        preco_custo = float(preco_custo_str.replace(',','.'))
        preco_venda = float(preco_venda_str.replace(',','.'))
        if preco_custo < 0 or preco_venda < 0:
            erros.append("Preços não podem ser negativos")
    except ValueError:
        erros.append("Preços inválidos")
    if not fornecedor.strip():
        erros.append("Fornecedor é obrigatório")
    if data_validade.strip():
        try:
            datetime.strptime(data_validade, "%d/%m/%Y")
        except ValueError:
            erros.append("Data de validade inválida (DD/MM/AAAA)")
    if not codigo_barras.strip():
        erros.append("Código de barras é obrigatório")
    # Removido: validação EAN-13
    return erros

def adicionar_item():
    nome = entry_nome.get().strip()
    quantidade_str = entry_quantidade.get().strip()
    unidade = entry_unidade.get().strip()
    categoria = combo_categoria.get().strip()
    limite_str = entry_limite.get().strip()
    preco_custo_str = entry_preco_custo.get().strip()
    preco_venda_str = entry_preco_venda.get().strip()
    fornecedor = entry_fornecedor.get().strip()
    data_validade = entry_data_validade.get().strip()
    codigo_barras = entry_codigo_barras.get().strip()

    erros = validar_entrada(nome, quantidade_str, unidade, categoria, limite_str, preco_custo_str, preco_venda_str, fornecedor, data_validade, codigo_barras)
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return

    for item in estoque:
        if item.get("codigo_barras", "") == codigo_barras:
            messagebox.showerror("Erro", "Código de barras já cadastrado!")
            return

    quantidade = int(quantidade_str)
    limite = int(limite_str) if limite_str else 0
    preco_custo = float(preco_custo_str.replace(',','.'))
    preco_venda = float(preco_venda_str.replace(',','.'))
    margem_lucro = preco_venda - preco_custo

    item = {
        "codigo_barras": codigo_barras,
        "nome": nome,
        "quantidade": quantidade,
        "unidade": unidade,
        "categoria": categoria,
        "limite_alerta": limite,
        "preco_custo": preco_custo,
        "preco_venda": preco_venda,
        "margem_lucro": margem_lucro,
        "fornecedor": fornecedor,
        "data_validade": data_validade,
        "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "movimentacoes": []
    }
    estoque.append(item)
    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    atualizar_contador_itens()
    messagebox.showinfo("Sucesso", "Item adicionado com sucesso!")

def remover_item():
    selecao = tree.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um item para remover.")
        return
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
    selecao = tree.selection()
    if not selecao:
        return
    item_selecionado = selecao[0]
    index_item = tree.index(item_selecionado)
    item_data = estoque[index_item]
    limpar_campos()
    entry_codigo_barras.insert(0, item_data.get("codigo_barras", ""))
    entry_nome.insert(0, item_data.get("nome", ""))
    entry_quantidade.insert(0, str(item_data.get("quantidade", "")))
    entry_unidade.insert(0, item_data.get("unidade", ""))
    combo_categoria.set(item_data.get("categoria", ""))
    entry_limite.insert(0, str(item_data.get("limite_alerta", "")))
    entry_preco_custo.insert(0, str(item_data.get("preco_custo", "")))
    entry_preco_venda.insert(0, str(item_data.get("preco_venda", "")))
    entry_fornecedor.insert(0, item_data.get("fornecedor", ""))
    entry_data_validade.insert(0, item_data.get("data_validade", ""))

def editar_item():
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
    preco_custo_str = entry_preco_custo.get().strip()
    preco_venda_str = entry_preco_venda.get().strip()
    fornecedor = entry_fornecedor.get().strip()
    data_validade = entry_data_validade.get().strip()
    codigo_barras = entry_codigo_barras.get().strip()
    erros = validar_entrada(nome, quantidade_str, unidade, categoria, limite_str, preco_custo_str, preco_venda_str, fornecedor, data_validade, codigo_barras)
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return
    quantidade = int(quantidade_str)
    limite = int(limite_str) if limite_str else 0
    preco_custo = float(preco_custo_str.replace(',','.'))
    preco_venda = float(preco_venda_str.replace(',','.'))
    margem_lucro = preco_venda - preco_custo
    estoque[index_item]["codigo_barras"] = codigo_barras
    estoque[index_item]["nome"] = nome
    estoque[index_item]["quantidade"] = quantidade
    estoque[index_item]["unidade"] = unidade
    estoque[index_item]["categoria"] = categoria
    estoque[index_item]["limite_alerta"] = limite
    estoque[index_item]["preco_custo"] = preco_custo
    estoque[index_item]["preco_venda"] = preco_venda
    estoque[index_item]["margem_lucro"] = margem_lucro
    estoque[index_item]["fornecedor"] = fornecedor
    estoque[index_item]["data_validade"] = data_validade
    estoque[index_item]["data_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    salvar_estoque(estoque)
    atualizar_lista()
    limpar_campos()
    atualizar_contador_itens()
    messagebox.showinfo("Sucesso", "Item editado com sucesso!")

def limpar_campos():
    entry_codigo_barras.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_unidade.delete(0, tk.END)
    combo_categoria.set('')
    entry_limite.delete(0, tk.END)
    entry_preco_custo.delete(0, tk.END)
    entry_preco_venda.delete(0, tk.END)
    entry_fornecedor.delete(0, tk.END)
    entry_data_validade.delete(0, tk.END)
    entry_busca.delete(0, tk.END)

def buscar_item():
    termo = entry_busca.get().strip().lower()
    for item in tree.get_children():
        tree.delete(item)
    if not termo:
        atualizar_lista()
        return
    for item in estoque:
        if (termo in item["nome"].lower() or 
            termo in item["categoria"].lower() or
            termo in item["codigo_barras"]):
            limite = item.get("limite_alerta", 0)
            validade_str = item.get("data_validade", "")
            alerta_validade = ""
            try:
                validade = datetime.strptime(validade_str, "%d/%m/%Y")
                dias_para_vencer = (validade - datetime.now()).days
                if dias_para_vencer <= 30:
                    alerta_validade = "⚠"
            except Exception:
                alerta_validade = ""
            if item["quantidade"] <= limite:
                tree.insert("", tk.END, 
                    values=(item["codigo_barras"], item["nome"], item["quantidade"], item["unidade"], item["categoria"], 
                            item["preco_custo"], item["preco_venda"], item["margem_lucro"], item["fornecedor"], validade_str, alerta_validade), 
                    tags=('baixo_estoque',))
            else:
                tree.insert("", tk.END, 
                    values=(item["codigo_barras"], item["nome"], item["quantidade"], item["unidade"], item["categoria"], 
                            item["preco_custo"], item["preco_venda"], item["margem_lucro"], item["fornecedor"], validade_str, alerta_validade))

def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    for item in estoque:
        limite = item.get("limite_alerta", 0)
        validade_str = item.get("data_validade", "")
        alerta_validade = ""
        try:
            validade = datetime.strptime(validade_str, "%d/%m/%Y")
            dias_para_vencer = (validade - datetime.now()).days
            if dias_para_vencer <= 30:
                alerta_validade = "⚠"
        except Exception:
            alerta_validade = ""
        if item.get("quantidade", 0) <= limite:
            tree.insert("", tk.END, 
                values=(
                    item.get("codigo_barras", ""),
                    item.get("nome", ""),
                    item.get("quantidade", 0),
                    item.get("unidade", ""),
                    item.get("categoria", ""),
                    item.get("preco_custo", 0),
                    item.get("preco_venda", 0),
                    item.get("margem_lucro", 0),
                    item.get("fornecedor", ""),
                    validade_str,
                    alerta_validade
                ), 
                tags=('baixo_estoque',))
        else:
            tree.insert("", tk.END, 
                values=(
                    item.get("codigo_barras", ""),
                    item.get("nome", ""),
                    item.get("quantidade", 0),
                    item.get("unidade", ""),
                    item.get("categoria", ""),
                    item.get("preco_custo", 0),
                    item.get("preco_venda", 0),
                    item.get("margem_lucro", 0),
                    item.get("fornecedor", ""),
                    validade_str,
                    alerta_validade
                ))

def atualizar_contador_itens():
    total_produtos = len(estoque)
    total_quantidade = sum(item["quantidade"] for item in estoque)
    itens_baixo_estoque = 0
    for item in estoque:
        if item["quantidade"] <= item.get("limite_alerta", 0):
            itens_baixo_estoque += 1
    label_contador.config(
        text=f"Total: {total_produtos} produtos | Quantidade total: {total_quantidade} unidades | Alertas: {itens_baixo_estoque}"
    )

def gerar_relatorio():
    relatorio = tk.Toplevel(root)
    relatorio.title("Relatório de Estoque")
    relatorio.geometry("900x600")
    frame_scroll = tk.Frame(relatorio)
    frame_scroll.pack(fill="both", expand=True, padx=10, pady=10)
    scrollbar = tk.Scrollbar(frame_scroll)
    scrollbar.pack(side="right", fill="y")
    text_relatorio = tk.Text(frame_scroll, wrap="word", yscrollcommand=scrollbar.set, font=("Arial", 10))
    text_relatorio.pack(fill="both", expand=True)
    scrollbar.config(command=text_relatorio.yview)
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
        if item["quantidade"] <= item.get("limite_alerta", 0):
            itens_baixo_estoque.append(item)
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    text_relatorio.insert(tk.END, f"=== RELATÓRIO DE ESTOQUE ===\n", ("titulo",))
    text_relatorio.insert(tk.END, f"Gerado em: {data_atual}\n\n")
    text_relatorio.insert(tk.END, "📊 RESUMO GERAL\n", ("categoria",))
    text_relatorio.insert(tk.END, f"• Total de produtos cadastrados: {total_produtos}\n")
    text_relatorio.insert(tk.END, f"• Quantidade total em estoque: {total_itens} unidades\n")
    text_relatorio.insert(tk.END, f"• Itens com estoque baixo: {len(itens_baixo_estoque)}\n\n")
    if itens_baixo_estoque:
        text_relatorio.insert(tk.END, "⚠  ALERTAS DE ESTOQUE BAIXO\n", ("alerta",))
        for item in itens_baixo_estoque:
            text_relatorio.insert(tk.END, 
                f"• {item['nome']}: {item['quantidade']} {item['unidade']} "
                f"(Limite: {item.get('limite_alerta', 0)})\n", ("alerta",))
        text_relatorio.insert(tk.END, "\n")
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
            writer.writerow(["Código de Barras", "Nome", "Quantidade", "Unidade", "Categoria", "Limite Alerta", "Preço Custo", "Preço Venda", "Margem Lucro", "Fornecedor", "Validade", "Data Cadastro"])
            for item in estoque:
                writer.writerow([
                    item["codigo_barras"], 
                    item["nome"], 
                    item["quantidade"], 
                    item["unidade"], 
                    item["categoria"],
                    item.get("limite_alerta", 0),
                    item.get("preco_custo", 0),
                    item.get("preco_venda", 0),
                    item.get("margem_lucro", 0),
                    item.get("fornecedor", ""),
                    item.get("data_validade", ""),
                    item.get("data_cadastro", "N/A")
                ])
        messagebox.showinfo("Sucesso", f"Dados exportados para: {arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar: {e}")

# --- Configuração da Janela Principal ---

root = tk.Tk()
root.title("Controle de Estoque - Versão 2.0")
root.geometry("1100x750")
root.configure(bg="#f0f0f0")

estoque = carregar_estoque()

style = ttk.Style()
style.theme_use('clam')
style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white")
style.configure("Treeview.Heading", background="#4472C4", foreground="white", font=('Arial', 10, 'bold'))
style.map("Treeview", background=[('selected', '#4472C4')], foreground=[('selected', 'white')])

main_frame = tk.Frame(root, bg="#f0f0f0")
main_frame.pack(fill="both", expand=True, padx=10, pady=10)

title_frame = tk.Frame(main_frame, bg="#f0f0f0")
title_frame.pack(fill="x", pady=(0, 20))
title_label = tk.Label(title_frame, text="🏪 CONTROLE DE ESTOQUE", font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
title_label.pack()

frame_controle = tk.LabelFrame(main_frame, text="📝 Dados do Produto", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#2c3e50")
frame_controle.pack(fill="x", pady=(0, 10))

tk.Label(frame_controle, text="Código de Barras (EAN-13):", bg="#f0f0f0").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
entry_codigo_barras = tk.Entry(frame_controle, width=40, font=("Arial", 10))
entry_codigo_barras.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Nome:", bg="#f0f0f0").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
entry_nome = tk.Entry(frame_controle, width=40, font=("Arial", 10))
entry_nome.grid(row=0, column=3, padx=5, pady=5)

tk.Label(frame_controle, text="Quantidade:", bg="#f0f0f0").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
entry_quantidade = tk.Entry(frame_controle, width=20, font=("Arial", 10))
entry_quantidade.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Unidade:", bg="#f0f0f0").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
entry_unidade = tk.Entry(frame_controle, width=20, font=("Arial", 10))
entry_unidade.grid(row=1, column=3, padx=5, pady=5)

tk.Label(frame_controle, text="Categoria:", bg="#f0f0f0").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
categorias = ["Alimentos", "Limpeza", "Higiene Pessoal", "Medicamentos", "Eletrônicos", "Roupas", "Outros"]
combo_categoria = ttk.Combobox(frame_controle, values=categorias, width=37, font=("Arial", 10))
combo_categoria.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Limite de Alerta:", bg="#f0f0f0").grid(row=2, column=2, sticky=tk.W, padx=5, pady=5)
entry_limite = tk.Entry(frame_controle, width=20, font=("Arial", 10))
entry_limite.grid(row=2, column=3, padx=5, pady=5)

tk.Label(frame_controle, text="Preço de Custo:", bg="#f0f0f0").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
entry_preco_custo = tk.Entry(frame_controle, width=20, font=("Arial", 10))
entry_preco_custo.grid(row=3, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Preço de Venda:", bg="#f0f0f0").grid(row=3, column=2, sticky=tk.W, padx=5, pady=5)
entry_preco_venda = tk.Entry(frame_controle, width=20, font=("Arial", 10))
entry_preco_venda.grid(row=3, column=3, padx=5, pady=5)

tk.Label(frame_controle, text="Fornecedor:", bg="#f0f0f0").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
entry_fornecedor = tk.Entry(frame_controle, width=40, font=("Arial", 10))
entry_fornecedor.grid(row=4, column=1, padx=5, pady=5)

tk.Label(frame_controle, text="Data de Validade (DD/MM/AAAA):", bg="#f0f0f0").grid(row=4, column=2, sticky=tk.W, padx=5, pady=5)
entry_data_validade = tk.Entry(frame_controle, width=20, font=("Arial", 10))
entry_data_validade.grid(row=4, column=3, padx=5, pady=5)

frame_busca = tk.LabelFrame(main_frame, text="🔍 Buscar Produtos", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#2c3e50")
frame_busca.pack(fill="x", pady=(0, 10))
tk.Label(frame_busca, text="Buscar:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
entry_busca = tk.Entry(frame_busca, width=40, font=("Arial", 10))
entry_busca.pack(side=tk.LEFT, padx=5)
entry_busca.bind('<KeyRelease>', lambda event: buscar_item())
botao_limpar_busca = tk.Button(frame_busca, text="Limpar", command=lambda: (entry_busca.delete(0, tk.END), atualizar_lista()))
botao_limpar_busca.pack(side=tk.LEFT, padx=5)

frame_botoes = tk.Frame(main_frame, bg="#f0f0f0")
frame_botoes.pack(fill="x", pady=(0, 10))
botao_adicionar = tk.Button(frame_botoes, text="➕ Adicionar", command=adicionar_item, bg="#27ae60", fg="white", font=("Arial", 10, "bold"), width=12)
botao_adicionar.pack(side=tk.LEFT, padx=3)
botao_editar = tk.Button(frame_botoes, text="✏ Editar", command=editar_item, bg="#f39c12", fg="white", font=("Arial", 10, "bold"), width=12)
botao_editar.pack(side=tk.LEFT, padx=3)
botao_remover = tk.Button(frame_botoes, text="🗑 Remover", command=remover_item, bg="#e74c3c", fg="white", font=("Arial", 10, "bold"), width=12)
botao_remover.pack(side=tk.LEFT, padx=3)
botao_limpar = tk.Button(frame_botoes, text="🧹 Limpar", command=limpar_campos, bg="#95a5a6", fg="white", font=("Arial", 10, "bold"), width=12)
botao_limpar.pack(side=tk.LEFT, padx=3)
botao_relatorio = tk.Button(frame_botoes, text="📊 Relatório", command=gerar_relatorio, bg="#3498db", fg="white", font=("Arial", 10, "bold"), width=12)
botao_relatorio.pack(side=tk.LEFT, padx=3)
botao_backup = tk.Button(frame_botoes, text="💾 Backup", command=fazer_backup, bg="#9b59b6", fg="white", font=("Arial", 10, "bold"), width=12)
botao_backup.pack(side=tk.LEFT, padx=3)
botao_exportar = tk.Button(frame_botoes, text="📤 Exportar CSV", command=exportar_csv, bg="#1abc9c", fg="white", font=("Arial", 10, "bold"), width=12)
botao_exportar.pack(side=tk.LEFT, padx=3)

frame_tabela = tk.LabelFrame(main_frame, text="📋 Lista de Produtos", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#2c3e50")
frame_tabela.pack(fill="both", expand=True, pady=(0, 10))
label_contador = tk.Label(main_frame, text="", font=("Arial", 10, "bold"), bg="#f0f0f0", fg="#2c3e50")
label_contador.pack(fill="x", pady=(0, 10))
frame_tree = tk.Frame(frame_tabela)
frame_tree.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("codigo_barras", "nome", "quantidade", "unidade", "categoria", "preco_custo", "preco_venda", "margem_lucro", "fornecedor", "data_validade", "alerta_validade")
tree = ttk.Treeview(frame_tree, columns=columns, show='headings', height=15)
tree.heading("codigo_barras", text="Código de Barras")
tree.heading("nome", text="Nome do Produto")
tree.heading("quantidade", text="Quantidade")
tree.heading("unidade", text="Unidade")
tree.heading("categoria", text="Categoria")
tree.heading("preco_custo", text="Preço de Custo")
tree.heading("preco_venda", text="Preço de Venda")
tree.heading("margem_lucro", text="Margem de Lucro")
tree.heading("fornecedor", text="Fornecedor")
tree.heading("data_validade", text="Validade")
tree.heading("alerta_validade", text="Alerta")
tree.column("codigo_barras", width=120, anchor="center")
tree.column("nome", width=200, anchor="w")
tree.column("quantidade", width=80, anchor="center")
tree.column("unidade", width=80, anchor="center")
tree.column("categoria", width=120, anchor="center")
tree.column("preco_custo", width=100, anchor="center")
tree.column("preco_venda", width=100, anchor="center")
tree.column("margem_lucro", width=100, anchor="center")
tree.column("fornecedor", width=150, anchor="center")
tree.column("data_validade", width=100, anchor="center")
tree.column("alerta_validade", width=60, anchor="center")
scrollbar_v = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
scrollbar_h = ttk.Scrollbar(frame_tree, orient="horizontal", command=tree.xview)
tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
tree.pack(side="left", fill="both", expand=True)
scrollbar_v.pack(side="right", fill="y")
scrollbar_h.pack(side="bottom", fill="x")
tree.tag_configure('baixo_estoque', background='#ffcccc', foreground='red')
tree.bind("<<TreeviewSelect>>", carregar_para_edicao)

atualizar_lista()
atualizar_contador_itens()
root.mainloop()