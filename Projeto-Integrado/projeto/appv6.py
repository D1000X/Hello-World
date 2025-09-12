import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
from datetime import datetime

# ---------------------------
# Arquivos
# ---------------------------
ARQUIVO_ESTOQUE = "estoque.json"
ARQUIVO_NOTAS = "notas.json"

# ---------------------------
# Carregar dados
# ---------------------------
def carregar_estoque():
    if os.path.exists(ARQUIVO_ESTOQUE):
        try:
            with open(ARQUIVO_ESTOQUE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

def carregar_notas():
    if os.path.exists(ARQUIVO_NOTAS):
        try:
            with open(ARQUIVO_NOTAS, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return []
    return []

estoque = carregar_estoque()
notas = carregar_notas()

# Corrigir itens antigos sem validade/movimentações
for item in estoque:
    if "data_validade" not in item:
        item["data_validade"] = ""
    if "movimentacoes" not in item:
        item["movimentacoes"] = []

# ---------------------------
# Salvamento
# ---------------------------
def salvar_estoque(estoque_local):
    try:
        with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as f:
            json.dump(estoque_local, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar arquivo: {e}")

def salvar_notas(notas_local):
    try:
        with open(ARQUIVO_NOTAS, "w", encoding="utf-8") as f:
            json.dump(notas_local, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar notas fiscais: {e}")

def fazer_backup():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"estoque_backup_{timestamp}.json"
    try:
        with open(backup_name, "w", encoding="utf-8") as f:
            json.dump(estoque, f, indent=4, ensure_ascii=False)
        messagebox.showinfo("Sucesso", f"Backup criado: {backup_name}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao criar backup: {e}")

# ---------------------------
# Validações
# ---------------------------
def validar_ean13(ean):
    if len(ean) != 13 or not ean.isdigit():
        return False
    soma = sum(int(ean[i]) if i % 2 == 0 else int(ean[i]) * 3 for i in range(12))
    digito = (10 - (soma % 10)) % 10
    return digito == int(ean[-1])

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
    else:
        if len(codigo_barras.strip()) == 13 and not validar_ean13(codigo_barras.strip()):
            erros.append("EAN-13 inválido")
    return erros

# ---------------------------
# Interface - funções Estoque
# ---------------------------
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
    margem_lucro = round(preco_venda - preco_custo, 2)

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

def carregar_para_edicao(event=None):
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
    margem_lucro = round(preco_venda - preco_custo, 2)

    estoque[index_item].update({
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
        "data_atualizacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
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
        if (termo in item.get("nome","").lower() or 
            termo in item.get("categoria","").lower() or
            termo in item.get("codigo_barras","")):
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
                    values=(item.get("codigo_barras",""), item.get("nome",""), item.get("quantidade",0), item.get("unidade",""), item.get("categoria",""), 
                            item.get("preco_custo",0), item.get("preco_venda",0), item.get("margem_lucro",0), item.get("fornecedor",""), validade_str, alerta_validade), 
                    tags=('baixo_estoque',))
            else:
                tree.insert("", tk.END, 
                    values=(item.get("codigo_barras",""), item.get("nome",""), item.get("quantidade",0), item.get("unidade",""), item.get("categoria",""), 
                            item.get("preco_custo",0), item.get("preco_venda",0), item.get("margem_lucro",0), item.get("fornecedor",""), validade_str, alerta_validade))

def atualizar_lista():
    for item in tree.get_children():
        tree.delete(item)
    for item in estoque:
        limite = item.get("limite_alerta", 0)
        validade_str = item.get("data_validade", "")
        alerta_validade = ""
        try:
            if validade_str:
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
    total_quantidade = sum(item.get("quantidade",0) for item in estoque)
    itens_baixo_estoque = sum(1 for item in estoque if item.get("quantidade",0) <= item.get("limite_alerta",0))
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
        categoria = item.get("categoria","Outros")
        categorias_estoque.setdefault(categoria, []).append(item)
        total_itens += item.get("quantidade",0)
        if item.get("quantidade",0) <= item.get("limite_alerta",0):
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
                f"• {item['nome']}: {item['quantidade']} {item.get('unidade','')} "
                f"(Limite: {item.get('limite_alerta', 0)})\n", ("alerta",))
        text_relatorio.insert(tk.END, "\n")
    text_relatorio.insert(tk.END, "📦 DETALHAMENTO POR CATEGORIA\n\n", ("categoria",))
    for categoria, itens in sorted(categorias_estoque.items()):
        text_relatorio.insert(tk.END, f"--- {categoria.upper()} ---\n", ("categoria",))
        qtd_categoria = sum(item.get("quantidade",0) for item in itens)
        text_relatorio.insert(tk.END, f"Total na categoria: {qtd_categoria} unidades\n")
        for item in sorted(itens, key=lambda x: x.get('nome','')):
            status = " ⚠" if item.get("quantidade",0) <= item.get("limite_alerta", 0) else ""
            text_relatorio.insert(tk.END, 
                f"  • {item.get('nome','')}: {item.get('quantidade',0)} {item.get('unidade','')}{status}\n")
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
                    item.get("codigo_barras",""), 
                    item.get("nome",""), 
                    item.get("quantidade",0), 
                    item.get("unidade",""), 
                    item.get("categoria",""),
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

# ---------------------------
# Notas Fiscais - VALIDAÇÕES e lista temporária
# ---------------------------
def validar_campos_nf():
    erros = []
    numero_nf = entry_numero_nf.get().strip()
    fornecedor_nf = entry_fornecedor_nf.get().strip()
    cnpj_nf = entry_cnpj_nf.get().strip()
    data_emissao = entry_data_emissao_nf.get().strip()
    if not numero_nf:
        erros.append("Número da NF é obrigatório")
    if not fornecedor_nf:
        erros.append("Fornecedor é obrigatório")
    if not cnpj_nf:
        erros.append("CNPJ é obrigatório")
    elif len(cnpj_nf.replace('.', '').replace('/', '').replace('-', '')) != 14:
        erros.append("CNPJ deve ter 14 dígitos")
    if not data_emissao:
        erros.append("Data de emissão é obrigatória")
    else:
        try:
            datetime.strptime(data_emissao, "%d/%m/%Y")
        except ValueError:
            erros.append("Data de emissão inválida (DD/MM/AAAA)")
    return erros

def validar_item_nf():
    erros = []
    produto = entry_produto_nf.get().strip()
    quantidade_str = entry_quantidade_nf.get().strip()
    preco_str = entry_preco_nf.get().strip()
    data_validade = entry_validade_nf.get().strip()
    if not produto:
        erros.append("Nome do produto é obrigatório")
    if not quantidade_str:
        erros.append("Quantidade é obrigatória")
    else:
        try:
            qtd = int(quantidade_str)
            if qtd <= 0:
                erros.append("Quantidade deve ser maior que zero")
        except ValueError:
            erros.append("Quantidade deve ser um número inteiro")
    if not preco_str:
        erros.append("Preço unitário é obrigatório")
    else:
        try:
            preco = float(preco_str.replace(',', '.'))
            if preco < 0:
                erros.append("Preço não pode ser negativo")
        except ValueError:
            erros.append("Preço inválido")
    if data_validade:
        try:
            datetime.strptime(data_validade, "%d/%m/%Y")
        except ValueError:
            erros.append("Data de validade inválida (DD/MM/AAAA)")
    return erros

itens_nf_temporarios = []

def adicionar_item_nf():
    erros = validar_item_nf()
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return
    produto = entry_produto_nf.get().strip()
    quantidade = int(entry_quantidade_nf.get().strip())
    preco_unitario = float(entry_preco_nf.get().strip().replace(',', '.'))
    data_validade = entry_validade_nf.get().strip()
    subtotal = round(quantidade * preco_unitario, 2)
    item_nf = {
        "produto": produto,
        "quantidade": quantidade,
        "preco_unitario": preco_unitario,
        "subtotal": subtotal,
        "data_validade": data_validade
    }
    itens_nf_temporarios.append(item_nf)
    atualizar_lista_itens_nf()
    limpar_campos_item_nf()
    messagebox.showinfo("Sucesso", f"Item '{produto}' adicionado à NF!")

def remover_item_nf():
    selecao = tree_itens_nf.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um item para remover.")
        return
    item_selecionado = selecao[0]
    index_item = tree_itens_nf.index(item_selecionado)
    produto_nome = itens_nf_temporarios[index_item]["produto"]
    itens_nf_temporarios.pop(index_item)
    atualizar_lista_itens_nf()
    messagebox.showinfo("Sucesso", f"Item '{produto_nome}' removido da NF!")

def atualizar_lista_itens_nf():
    for item in tree_itens_nf.get_children():
        tree_itens_nf.delete(item)
    total_nf = 0
    for item in itens_nf_temporarios:
        tree_itens_nf.insert("", tk.END, values=(
            item["produto"],
            item["quantidade"],
            f"R$ {item['preco_unitario']:.2f}",
            f"R$ {item['subtotal']:.2f}",
            item["data_validade"]
        ))
        total_nf += item["subtotal"]
    label_total_nf.config(text=f"Total da NF: R$ {total_nf:.2f}")

def limpar_campos_item_nf():
    entry_produto_nf.delete(0, tk.END)
    entry_quantidade_nf.delete(0, tk.END)
    entry_preco_nf.delete(0, tk.END)
    entry_validade_nf.delete(0, tk.END)

def limpar_campos_nf():
    entry_numero_nf.delete(0, tk.END)
    entry_fornecedor_nf.delete(0, tk.END)
    entry_cnpj_nf.delete(0, tk.END)
    entry_data_emissao_nf.delete(0, tk.END)
    limpar_campos_item_nf()
    itens_nf_temporarios.clear()
    atualizar_lista_itens_nf()

def atualizar_estoque_com_nf(itens_nf):
    itens_atualizados = 0
    itens_novos = 0
    for item_nf in itens_nf:
        produto_encontrado = False
        for item_estoque in estoque:
            if item_estoque.get("nome","").lower() == item_nf["produto"].lower():
                item_estoque["quantidade"] = item_estoque.get("quantidade",0) + item_nf["quantidade"]
                item_estoque["data_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                if "movimentacoes" not in item_estoque:
                    item_estoque["movimentacoes"] = []
                item_estoque["movimentacoes"].append({
                    "tipo": "entrada_nf",
                    "quantidade": item_nf["quantidade"],
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "observacao": f"NF {entry_numero_nf.get().strip()}"
                })
                produto_encontrado = True
                itens_atualizados += 1
                break
        if not produto_encontrado:
            novo_codigo = f"NF{entry_numero_nf.get().strip()}{len(estoque)+1:03d}"
            novo_item = {
                "codigo_barras": novo_codigo,
                "nome": item_nf["produto"],
                "quantidade": item_nf["quantidade"],
                "unidade": "un",
                "categoria": "Outros",
                "limite_alerta": 0,
                "preco_custo": item_nf["preco_unitario"],
                "preco_venda": item_nf["preco_unitario"],
                "margem_lucro": 0,
                "fornecedor": entry_fornecedor_nf.get().strip(),
                "data_validade": item_nf.get("data_validade",""),
                "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "movimentacoes": [{
                    "tipo": "entrada_nf",
                    "quantidade": item_nf["quantidade"],
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "observacao": f"NF {entry_numero_nf.get().strip()}"
                }]
            }
            estoque.append(novo_item)
            itens_novos += 1
    salvar_estoque(estoque)
    atualizar_lista()
    atualizar_contador_itens()
    return itens_atualizados, itens_novos

def salvar_nf():
    erros = validar_campos_nf()
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return
    if not itens_nf_temporarios:
        messagebox.showwarning("Aviso", "Adicione pelo menos 1 item na NF!")
        return
    numero = entry_numero_nf.get().strip()
    fornecedor = entry_fornecedor_nf.get().strip()
    cnpj = entry_cnpj_nf.get().strip()
    data_emissao = entry_data_emissao_nf.get().strip()
    nf = {
        "numero": numero,
        "fornecedor": fornecedor,
        "cnpj": cnpj,
        "data_emissao": data_emissao,
        "itens": itens_nf_temporarios.copy(),
        "data_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notas.append(nf)
    salvar_notas(notas)
    atualizados, novos = atualizar_estoque_com_nf(itens_nf_temporarios)
    limpar_campos_nf()
    messagebox.showinfo("Sucesso", f"NF {numero} registrada! Itens atualizados: {atualizados}, novos: {novos}")

# ---------------------------
# Interface Tkinter
# ---------------------------
root = tk.Tk()
root.title("Controle de Estoque - v6")
root.geometry("1200x700")

# Frames principais
frame_top = tk.Frame(root)
frame_top.pack(fill="x", padx=8, pady=6)

frame_main = tk.Frame(root)
frame_main.pack(fill="both", expand=True, padx=8, pady=6)

# ---------- CONTROLES SUPERIORES ----------
btn_backup = tk.Button(frame_top, text="Backup", command=fazer_backup)
btn_backup.pack(side="left", padx=4)
btn_export_csv = tk.Button(frame_top, text="Exportar CSV", command=exportar_csv)
btn_export_csv.pack(side="left", padx=4)
btn_relatorio = tk.Button(frame_top, text="Gerar Relatório", command=gerar_relatorio)
btn_relatorio.pack(side="left", padx=4)

label_contador = tk.Label(frame_top, text="")
label_contador.pack(side="right")

# ---------- TABS ----------
notebook = ttk.Notebook(frame_main)
notebook.pack(fill="both", expand=True)

# --- Aba Estoque ---
aba_estoque = ttk.Frame(notebook)
notebook.add(aba_estoque, text="Estoque")

# Formulário Estoque (topo da aba)
frame_form = tk.Frame(aba_estoque)
frame_form.pack(fill="x", padx=6, pady=6)

labels = ["Código de Barras","Nome","Quantidade","Unidade","Categoria","Limite Alerta","Preço Custo","Preço Venda","Fornecedor","Validade (dd/mm/aaaa)"]
for i, txt in enumerate(labels):
    tk.Label(frame_form, text=txt).grid(row=0, column=i, padx=4, sticky="w")

entry_codigo_barras = tk.Entry(frame_form, width=12)
entry_codigo_barras.grid(row=1, column=0, padx=4)
entry_nome = tk.Entry(frame_form, width=20)
entry_nome.grid(row=1, column=1, padx=4)
entry_quantidade = tk.Entry(frame_form, width=8)
entry_quantidade.grid(row=1, column=2, padx=4)
entry_unidade = tk.Entry(frame_form, width=8)
entry_unidade.grid(row=1, column=3, padx=4)
combo_categoria = ttk.Combobox(frame_form, values=["Alimento","Bebida","Limpeza","Outro"], width=12)
combo_categoria.grid(row=1, column=4, padx=4)
entry_limite = tk.Entry(frame_form, width=8)
entry_limite.grid(row=1, column=5, padx=4)
entry_preco_custo = tk.Entry(frame_form, width=10)
entry_preco_custo.grid(row=1, column=6, padx=4)
entry_preco_venda = tk.Entry(frame_form, width=10)
entry_preco_venda.grid(row=1, column=7, padx=4)
entry_fornecedor = tk.Entry(frame_form, width=15)
entry_fornecedor.grid(row=1, column=8, padx=4)
entry_data_validade = tk.Entry(frame_form, width=14)
entry_data_validade.grid(row=1, column=9, padx=4)

# Botões do formulário
frame_buttons = tk.Frame(aba_estoque)
frame_buttons.pack(fill="x", padx=6, pady=6)
btn_adicionar = tk.Button(frame_buttons, text="Adicionar Produto", command=adicionar_item, bg="#4caf50", fg="white")
btn_adicionar.pack(side="left", padx=4)
btn_editar = tk.Button(frame_buttons, text="Editar Selecionado", command=editar_item, bg="#2196f3", fg="white")
btn_editar.pack(side="left", padx=4)
btn_remover = tk.Button(frame_buttons, text="Remover Selecionado", command=remover_item, bg="#f44336", fg="white")
btn_remover.pack(side="left", padx=4)
btn_limpar = tk.Button(frame_buttons, text="Limpar Campos", command=limpar_campos)
btn_limpar.pack(side="left", padx=4)

entry_busca = tk.Entry(frame_buttons, width=30)
entry_busca.pack(side="right", padx=4)
btn_buscar = tk.Button(frame_buttons, text="Buscar", command=buscar_item)
btn_buscar.pack(side="right", padx=4)

# Treeview Estoque
cols = ("Código","Nome","Qtd","Unidade","Categoria","Custo","Venda","Margem","Fornecedor","Validade","Alerta")
tree = ttk.Treeview(aba_estoque, columns=cols, show="headings", height=18)
for c in cols:
    tree.heading(c, text=c)
    tree.column(c, width=100)
tree.column("Nome", width=220)
tree.column("Fornecedor", width=140)
tree.pack(fill="both", expand=True, padx=6, pady=6)
tree.bind("<Double-1>", carregar_para_edicao)
tree.tag_configure('baixo_estoque', background='#ffe6e6')

# --- Aba Notas Fiscais ---
aba_nf = ttk.Frame(notebook)
notebook.add(aba_nf, text="Notas Fiscais")

# Cabeçalho NF
tk.Label(aba_nf, text="Número NF:").grid(row=0, column=0, padx=6, pady=4, sticky="e")
entry_numero_nf = tk.Entry(aba_nf, width=20)
entry_numero_nf.grid(row=0, column=1, padx=6, pady=4, sticky="w")

tk.Label(aba_nf, text="Fornecedor:").grid(row=1, column=0, padx=6, pady=4, sticky="e")
entry_fornecedor_nf = tk.Entry(aba_nf, width=30)
entry_fornecedor_nf.grid(row=1, column=1, padx=6, pady=4, sticky="w")

tk.Label(aba_nf, text="CNPJ:").grid(row=2, column=0, padx=6, pady=4, sticky="e")
entry_cnpj_nf = tk.Entry(aba_nf, width=20)
entry_cnpj_nf.grid(row=2, column=1, padx=6, pady=4, sticky="w")

tk.Label(aba_nf, text="Data Emissão (dd/mm/aaaa):").grid(row=3, column=0, padx=6, pady=4, sticky="e")
entry_data_emissao_nf = tk.Entry(aba_nf, width=20)
entry_data_emissao_nf.grid(row=3, column=1, padx=6, pady=4, sticky="w")

# Itens NF - inputs
tk.Label(aba_nf, text="Produto:").grid(row=4, column=0, padx=6, pady=4, sticky="e")
entry_produto_nf = tk.Entry(aba_nf, width=30)
entry_produto_nf.grid(row=4, column=1, padx=6, pady=4, sticky="w")

tk.Label(aba_nf, text="Quantidade:").grid(row=5, column=0, padx=6, pady=4, sticky="e")
entry_quantidade_nf = tk.Entry(aba_nf, width=10)
entry_quantidade_nf.grid(row=5, column=1, padx=6, pady=4, sticky="w")

tk.Label(aba_nf, text="Preço Unitário:").grid(row=6, column=0, padx=6, pady=4, sticky="e")
entry_preco_nf = tk.Entry(aba_nf, width=12)
entry_preco_nf.grid(row=6, column=1, padx=6, pady=4, sticky="w")

tk.Label(aba_nf, text="Validade (dd/mm/aaaa):").grid(row=7, column=0, padx=6, pady=4, sticky="e")
entry_validade_nf = tk.Entry(aba_nf, width=20)
entry_validade_nf.grid(row=7, column=1, padx=6, pady=4, sticky="w")

btn_add_item_nf = tk.Button(aba_nf, text="Adicionar Item à NF", command=adicionar_item_nf, bg="#4caf50", fg="white")
btn_add_item_nf.grid(row=8, column=0, columnspan=2, pady=6)

# Treeview itens NF
cols_itens_nf = ("Produto","Quantidade","Preço Unit.","Subtotal","Validade")
tree_itens_nf = ttk.Treeview(aba_nf, columns=cols_itens_nf, show="headings", height=8)
for c in cols_itens_nf:
    tree_itens_nf.heading(c, text=c)
    tree_itens_nf.column(c, width=120)
tree_itens_nf.grid(row=9, column=0, columnspan=3, padx=6, pady=6)

btn_remover_item_nf = tk.Button(aba_nf, text="Remover Item Selecionado", command=remover_item_nf, bg="#f44336", fg="white")
btn_remover_item_nf.grid(row=10, column=0, pady=4)

label_total_nf = tk.Label(aba_nf, text="Total da NF: R$ 0.00", font=("Arial", 11, "bold"))
label_total_nf.grid(row=10, column=1, pady=4, sticky="w")

btn_salvar_nf = tk.Button(aba_nf, text="Salvar Nota Fiscal", command=salvar_nf, bg="#2196f3", fg="white")
btn_salvar_nf.grid(row=11, column=0, columnspan=2, pady=10)

# Inicialização UI
atualizar_lista()
atualizar_contador_itens()
root.mainloop()
