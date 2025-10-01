import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os
import csv
from datetime import datetime, timedelta

# ---------------------------
# Arquivos do Sistema
# ---------------------------
ARQUIVO_ESTOQUE = "estoque.json"
ARQUIVO_NOTAS = "notas.json"
ARQUIVO_USUARIOS = "usuarios.json"

# ---------------------------
# Paleta de Cores
# ---------------------------
COLORS = {
    'primary': '#1976d2',
    'primary_light': '#42a5f5',
    'primary_dark': '#0d47a1',
    'secondary': '#424242',
    'success': '#4caf50',
    'danger': '#f44336',
    'warning': '#ff9800',
    'background': '#f5f5f5',
    'surface': '#ffffff',
    'text_primary': '#212121',
    'text_secondary': '#757575',
    'low_stock': '#ffebee',
    'expired': '#ffcdd2'
}

# ---------------------------
# Variáveis Globais
# ---------------------------
usuario_logado = None
estoque = []
notas = []
usuarios = []
itens_nf_temporarios = []
style = None

# ---------------------------
# Configuração de Estilos
# ---------------------------
def configurar_estilos():
    global style
    style = ttk.Style()
    
    # Configurar tema base
    style.theme_use('clam')
    
    # Estilo para Notebook (abas)
    style.configure('TNotebook', background=COLORS['background'])
    style.configure('TNotebook.Tab', 
                   padding=[20, 10], 
                   background=COLORS['surface'],
                   foreground=COLORS['text_primary'],
                   font=('Segoe UI', 10))
    style.map('TNotebook.Tab',
              background=[('selected', COLORS['primary']),
                         ('active', COLORS['primary_light'])],
              foreground=[('selected', 'white'),
                         ('active', 'white')])
    
    # Estilo para Treeview
    style.configure('Treeview', 
                   background=COLORS['surface'],
                   foreground=COLORS['text_primary'],
                   fieldbackground=COLORS['surface'],
                   font=('Segoe UI', 9))
    style.configure('Treeview.Heading', 
                   background=COLORS['primary'],
                   foreground='white',
                   font=('Segoe UI', 10, 'bold'))
    
    # Estilo para Combobox
    style.configure('TCombobox', 
                   fieldbackground=COLORS['surface'],
                   background=COLORS['surface'])
    
    # Estilo para Labels
    style.configure('Title.TLabel', 
                   background=COLORS['background'],
                   foreground=COLORS['text_primary'],
                   font=('Segoe UI', 14, 'bold'))
    
    style.configure('Subtitle.TLabel', 
                   background=COLORS['background'],
                   foreground=COLORS['text_secondary'],
                   font=('Segoe UI', 10))
    
    # Estilo para Frames
    style.configure('Card.TFrame', 
                   background=COLORS['surface'],
                   relief='flat',
                   borderwidth=1)

def criar_botao_personalizado(parent, text, command, bg_color, fg_color='white', width=None):
    """Cria um botão com estilo personalizado"""
    btn = tk.Button(parent, text=text, command=command,
                   bg=bg_color, fg=fg_color,
                   font=('Segoe UI', 10, 'bold'),
                   relief='flat', borderwidth=0,
                   padx=15, pady=8,
                   cursor='hand2')
    if width:
        btn.config(width=width)
    
    # Efeitos de hover
    def on_enter(e):
        btn.config(bg=ajustar_cor(bg_color, -20))
    def on_leave(e):
        btn.config(bg=bg_color)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

def ajustar_cor(hex_color, ajuste):
    """Ajusta o brilho de uma cor hexadecimal"""
    hex_color = hex_color.lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    rgb = tuple(max(0, min(255, c + ajuste)) for c in rgb)
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"

# ---------------------------
# Funções de Usuários
# ---------------------------
def carregar_usuarios():
    if not os.path.exists(ARQUIVO_USUARIOS):
        usuarios_default = [{"usuario": "admin", "senha": "admin123", "nivel": "admin"}]
        salvar_usuarios(usuarios_default)
        return usuarios_default
    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return [{"usuario": "admin", "senha": "admin123", "nivel": "admin"}]

def salvar_usuarios(usuarios_local):
    try:
        with open(ARQUIVO_USUARIOS, "w", encoding="utf-8") as f:
            json.dump(usuarios_local, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar usuários: {e}")

# ---------------------------
# Funções de Dados
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

def salvar_estoque(estoque_local):
    try:
        with open(ARQUIVO_ESTOQUE, "w", encoding="utf-8") as f:
            json.dump(estoque_local, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar estoque: {e}")

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
        backup_data = {
            "estoque": estoque,
            "notas": notas,
            "data_backup": timestamp
        }
        with open(backup_name, "w", encoding="utf-8") as f:
            json.dump(backup_data, f, indent=4, ensure_ascii=False)
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

def validar_entrada_produto(nome, quantidade_str, unidade, categoria, limite_str, 
                          preco_custo_str, preco_venda_str, fornecedor, data_validade, codigo_barras):
    erros = []
    
    # Validar nome
    if not nome.strip():
        erros.append("Nome é obrigatório")
    elif len(nome.strip()) > 100:
        erros.append("Nome muito longo (máx 100 caracteres)")
    
    # Validar quantidade
    if not quantidade_str.strip():
        erros.append("Quantidade é obrigatória")
    else:
        try:
            qtd = int(quantidade_str)
            if qtd < 0:
                erros.append("Quantidade não pode ser negativa")
        except ValueError:
            erros.append("Quantidade deve ser um número inteiro")
    
    # Validar outros campos obrigatórios
    if not unidade.strip():
        erros.append("Unidade é obrigatória")
    if not categoria.strip():
        erros.append("Categoria é obrigatória")
    if not fornecedor.strip():
        erros.append("Fornecedor é obrigatório")
    
    # Validar limite de alerta
    if limite_str.strip():
        try:
            limite = int(limite_str)
            if limite < 0:
                erros.append("Limite de alerta não pode ser negativo")
        except ValueError:
            erros.append("Limite de alerta deve ser um número inteiro")
    
    # Validar preços
    try:
        preco_custo = float(preco_custo_str.replace(',', '.'))
        preco_venda = float(preco_venda_str.replace(',', '.'))
        if preco_custo < 0 or preco_venda < 0:
            erros.append("Preços não podem ser negativos")
    except ValueError:
        erros.append("Preços inválidos")
    
    # Validar data de validade
    if data_validade.strip():
        try:
            datetime.strptime(data_validade, "%d/%m/%Y")
        except ValueError:
            erros.append("Data de validade inválida (DD/MM/AAAA)")
    
    # Validar código de barras
    if not codigo_barras.strip():
        erros.append("Código de barras é obrigatório")
    elif len(codigo_barras.strip()) == 13 and not validar_ean13(codigo_barras.strip()):
        erros.append("EAN-13 inválido")
    
    return erros

# ---------------------------
# Tela de Login
# ---------------------------
def iniciar_login():
    global tela_login, entry_usuario, entry_senha, usuarios
    
    usuarios = carregar_usuarios()
    
    tela_login = tk.Tk()
    tela_login.title("Login - Sistema de Estoque v7")
    tela_login.geometry("450x500")
    tela_login.resizable(False, False)
    tela_login.configure(bg=COLORS['background'])
    
    # Centralizar na tela
    tela_login.eval('tk::PlaceWindow . center')
    
    # Frame principal com padding
    main_frame = tk.Frame(tela_login, bg=COLORS['surface'], padx=40, pady=40)
    main_frame.pack(expand=True, fill="both", padx=30, pady=30)
    
    # Logo/Título
    titulo_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    titulo_frame.pack(pady=(0, 30))
    
    tk.Label(titulo_frame, text="SISTEMA DE ESTOQUE", 
            font=('Segoe UI', 20, 'bold'), 
            fg=COLORS['primary'], bg=COLORS['surface']).pack()
    
    tk.Label(titulo_frame, text="Versão 7.0", 
            font=('Segoe UI', 12), 
            fg=COLORS['text_secondary'], bg=COLORS['surface']).pack(pady=(5, 0))
    
    # Formulário de login
    form_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    form_frame.pack(fill="x", pady=20)
    
    # Campo usuário
    tk.Label(form_frame, text="Usuário:", 
            font=('Segoe UI', 11, 'bold'), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).pack(anchor="w", pady=(0, 5))
    
    entry_usuario = tk.Entry(form_frame, font=('Segoe UI', 12), 
                            relief='solid', borderwidth=1, highlightthickness=0)
    entry_usuario.pack(fill="x", pady=(0, 15), ipady=8)
    
    # Campo senha
    tk.Label(form_frame, text="Senha:", 
            font=('Segoe UI', 11, 'bold'), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).pack(anchor="w", pady=(0, 5))
    
    entry_senha = tk.Entry(form_frame, font=('Segoe UI', 12), show="*",
                          relief='solid', borderwidth=1, highlightthickness=0)
    entry_senha.pack(fill="x", pady=(0, 25), ipady=8)
    
    # Botão de login
    btn_login = criar_botao_personalizado(form_frame, "ENTRAR", verificar_login, 
                                        COLORS['primary'], width=20)
    btn_login.pack(fill="x", pady=10, ipady=5)
    
    # Informações do admin
    info_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    info_frame.pack(pady=(30, 0))
    
    tk.Label(info_frame, text="Primeiro acesso:", 
            font=('Segoe UI', 10, 'bold'), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).pack()
    
    tk.Label(info_frame, text="Usuário: admin | Senha: admin123", 
            font=('Segoe UI', 9), 
            fg=COLORS['text_secondary'], bg=COLORS['surface']).pack(pady=(5, 0))
    
    # Binds
    entry_senha.bind('<Return>', lambda event: verificar_login())
    entry_usuario.bind('<Return>', lambda event: entry_senha.focus())
    entry_usuario.focus()
    
    tela_login.mainloop()

def verificar_login():
    usuario = entry_usuario.get().strip()
    senha = entry_senha.get().strip()
    
    if not usuario or not senha:
        messagebox.showerror("Erro", "Digite usuário e senha")
        return
    
    for u in usuarios:
        if u["usuario"] == usuario and u["senha"] == senha:
            global usuario_logado
            usuario_logado = u
            messagebox.showinfo("Login", f"Bem-vindo {usuario}!")
            tela_login.destroy()
            abrir_sistema()
            return
    
    messagebox.showerror("Erro", "Usuário ou senha inválidos")

def logout():
    global usuario_logado
    usuario_logado = None
    root.destroy()
    iniciar_login()

# ---------------------------
# Sistema Principal
# ---------------------------
def abrir_sistema():
    global root, tree_estoque, estoque, notas
    global entry_codigo, entry_nome, entry_quantidade, entry_unidade
    global combo_categoria, entry_limite, entry_preco_custo, entry_preco_venda
    global entry_fornecedor, entry_validade, entry_busca, label_contador
    
    # Carregar dados
    estoque = carregar_estoque()
    notas = carregar_notas()
    
    # Corrigir dados antigos
    for item in estoque:
        if "data_validade" not in item:
            item["data_validade"] = ""
        if "movimentacoes" not in item:
            item["movimentacoes"] = []
    
    # Janela principal
    root = tk.Tk()
    root.title(f"Sistema de Estoque v7 - {usuario_logado['usuario']} ({usuario_logado['nivel']})")
    root.geometry("1400x800")
    root.configure(bg=COLORS['background'])
    root.state('zoomed')  # Maximizar no Windows
    
    # Configurar estilos
    configurar_estilos()
    
    # Header
    criar_header()
    
    # Notebook principal
    notebook = ttk.Notebook(root, style='TNotebook')
    notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    
    # Criar abas
    criar_aba_estoque(notebook)
    criar_aba_notas_fiscais(notebook)
    if usuario_logado["nivel"] == "admin":
        criar_aba_usuarios(notebook)
    criar_aba_relatorios(notebook)
    
    # Inicialização
    atualizar_lista_estoque()
    atualizar_contador_itens()
    
    root.mainloop()

def criar_header():
    """Cria o cabeçalho do sistema"""
    header_frame = tk.Frame(root, bg=COLORS['primary'], height=60)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)
    
    # Título
    title_frame = tk.Frame(header_frame, bg=COLORS['primary'])
    title_frame.pack(side="left", padx=20, pady=15)
    
    tk.Label(title_frame, text="SISTEMA DE ESTOQUE", 
            font=('Segoe UI', 16, 'bold'), 
            fg='white', bg=COLORS['primary']).pack(side="left")
    
    # Informações do usuário e botões
    user_frame = tk.Frame(header_frame, bg=COLORS['primary'])
    user_frame.pack(side="right", padx=20, pady=10)
    
    # Contador de itens
    global label_contador
    label_contador = tk.Label(user_frame, text="", 
                            font=('Segoe UI', 10), 
                            fg='white', bg=COLORS['primary'])
    label_contador.pack(side="left", padx=(0, 20))
    
    # Botão backup
    btn_backup = criar_botao_personalizado(user_frame, "Backup", fazer_backup, 
                                         COLORS['success'])
    btn_backup.pack(side="left", padx=5)
    
    # Botão logout
    btn_logout = criar_botao_personalizado(user_frame, "Sair", logout, 
                                         COLORS['danger'])
    btn_logout.pack(side="left", padx=5)

def criar_aba_estoque(notebook):
    """Cria a aba de gestão de estoque"""
    global tree_estoque, entry_codigo, entry_nome, entry_quantidade, entry_unidade
    global combo_categoria, entry_limite, entry_preco_custo, entry_preco_venda
    global entry_fornecedor, entry_validade, entry_busca
    
    aba_estoque = ttk.Frame(notebook)
    notebook.add(aba_estoque, text="📦 Estoque")
    
    # Frame principal
    main_frame = ttk.Frame(aba_estoque, style='Card.TFrame')
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título da seção
    title_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    title_frame.pack(fill="x", padx=20, pady=(20, 10))
    
    tk.Label(title_frame, text="Gestão de Produtos", 
            font=('Segoe UI', 16, 'bold'), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).pack(side="left")
    
    # Formulário de produto
    form_frame = tk.LabelFrame(main_frame, text="Dados do Produto", 
                              font=('Segoe UI', 11, 'bold'),
                              fg=COLORS['text_primary'], bg=COLORS['surface'])
    form_frame.pack(fill="x", padx=20, pady=10)
    
    # Primeira linha do formulário
    row1 = tk.Frame(form_frame, bg=COLORS['surface'])
    row1.pack(fill="x", padx=10, pady=10)
    
    # Código de barras
    tk.Label(row1, text="Código:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=0, sticky="w")
    entry_codigo = tk.Entry(row1, width=15, font=('Segoe UI', 10))
    entry_codigo.grid(row=1, column=0, padx=(0, 10), sticky="ew")
    
    # Nome do produto
    tk.Label(row1, text="Nome do Produto:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=1, sticky="w")
    entry_nome = tk.Entry(row1, width=25, font=('Segoe UI', 10))
    entry_nome.grid(row=1, column=1, padx=(0, 10), sticky="ew")
    
    # Quantidade
    tk.Label(row1, text="Quantidade:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=2, sticky="w")
    entry_quantidade = tk.Entry(row1, width=10, font=('Segoe UI', 10))
    entry_quantidade.grid(row=1, column=2, padx=(0, 10), sticky="ew")
    
    # Unidade
    tk.Label(row1, text="Unidade:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=3, sticky="w")
    entry_unidade = tk.Entry(row1, width=8, font=('Segoe UI', 10))
    entry_unidade.grid(row=1, column=3, padx=(0, 10), sticky="ew")
    
    # Categoria
    tk.Label(row1, text="Categoria:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=4, sticky="w")
    combo_categoria = ttk.Combobox(row1, values=["Alimento", "Bebida", "Limpeza", "Higiene", "Outros"], 
                                  width=12, font=('Segoe UI', 10))
    combo_categoria.grid(row=1, column=4, sticky="ew")
    
    # Segunda linha do formulário
    row2 = tk.Frame(form_frame, bg=COLORS['surface'])
    row2.pack(fill="x", padx=10, pady=10)
    
    # Limite de alerta
    tk.Label(row2, text="Limite Alerta:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=0, sticky="w")
    entry_limite = tk.Entry(row2, width=10, font=('Segoe UI', 10))
    entry_limite.grid(row=1, column=0, padx=(0, 10), sticky="ew")
    
    # Preço de custo
    tk.Label(row2, text="Preço Custo:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=1, sticky="w")
    entry_preco_custo = tk.Entry(row2, width=12, font=('Segoe UI', 10))
    entry_preco_custo.grid(row=1, column=1, padx=(0, 10), sticky="ew")
    
    # Preço de venda
    tk.Label(row2, text="Preço Venda:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=2, sticky="w")
    entry_preco_venda = tk.Entry(row2, width=12, font=('Segoe UI', 10))
    entry_preco_venda.grid(row=1, column=2, padx=(0, 10), sticky="ew")
    
    # Fornecedor
    tk.Label(row2, text="Fornecedor:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=3, sticky="w")
    entry_fornecedor = tk.Entry(row2, width=20, font=('Segoe UI', 10))
    entry_fornecedor.grid(row=1, column=3, padx=(0, 10), sticky="ew")
    
    # Data de validade
    tk.Label(row2, text="Validade (dd/mm/aaaa):", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=4, sticky="w")
    entry_validade = tk.Entry(row2, width=15, font=('Segoe UI', 10))
    entry_validade.grid(row=1, column=4, sticky="ew")
    
    # Botões de ação
    btn_frame = tk.Frame(form_frame, bg=COLORS['surface'])
    btn_frame.pack(fill="x", padx=10, pady=15)
    
    btn_adicionar = criar_botao_personalizado(btn_frame, "Adicionar", adicionar_produto, 
                                            COLORS['success'])
    btn_adicionar.pack(side="left", padx=5)
    
    btn_editar = criar_botao_personalizado(btn_frame, "Editar", editar_produto, 
                                         COLORS['primary'])
    btn_editar.pack(side="left", padx=5)
    
    btn_remover = criar_botao_personalizado(btn_frame, "Remover", remover_produto, 
                                          COLORS['danger'])
    btn_remover.pack(side="left", padx=5)
    
    btn_limpar = criar_botao_personalizado(btn_frame, "Limpar", limpar_campos_produto, 
                                         COLORS['secondary'])
    btn_limpar.pack(side="left", padx=5)
    
    # Campo de busca
    search_frame = tk.Frame(btn_frame, bg=COLORS['surface'])
    search_frame.pack(side="right")
    
    tk.Label(search_frame, text="Buscar:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).pack(side="left")
    entry_busca = tk.Entry(search_frame, width=20, font=('Segoe UI', 10))
    entry_busca.pack(side="left", padx=5)
    btn_buscar = criar_botao_personalizado(search_frame, "Buscar", buscar_produto, 
                                         COLORS['primary'])
    btn_buscar.pack(side="left", padx=5)
    
    # Lista de produtos
    list_frame = tk.LabelFrame(main_frame, text="Lista de Produtos", 
                              font=('Segoe UI', 11, 'bold'),
                              fg=COLORS['text_primary'], bg=COLORS['surface'])
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Treeview com scrollbars
    tree_frame = tk.Frame(list_frame, bg=COLORS['surface'])
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Colunas da tabela
    colunas = ("Código", "Nome", "Qtd", "Unidade", "Categoria", "Custo", "Venda", "Margem", "Fornecedor", "Validade", "Status")
    tree_estoque = ttk.Treeview(tree_frame, columns=colunas, show="headings", height=15)
    
    # Configurar colunas
    larguras = [100, 200, 60, 80, 100, 80, 80, 80, 150, 100, 80]
    for i, col in enumerate(colunas):
        tree_estoque.heading(col, text=col)
        tree_estoque.column(col, width=larguras[i], minwidth=50)
    
    # Scrollbars
    scrollbar_v = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_estoque.yview)
    scrollbar_h = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree_estoque.xview)
    tree_estoque.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
    
    # Pack da treeview e scrollbars
    tree_estoque.grid(row=0, column=0, sticky="nsew")
    scrollbar_v.grid(row=0, column=1, sticky="ns")
    scrollbar_h.grid(row=1, column=0, sticky="ew")
    
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    
    # Configurar tags para cores alternadas
    tree_estoque.tag_configure('par', background='#f8f9fa')
    tree_estoque.tag_configure('impar', background=COLORS['surface'])
    tree_estoque.tag_configure('baixo_estoque', background=COLORS['low_stock'])
    tree_estoque.tag_configure('vencido', background=COLORS['expired'])
    
    # Bind para carregar item selecionado
    tree_estoque.bind("<Double-1>", carregar_produto_para_edicao)

def criar_aba_notas_fiscais(notebook):
    """Cria a aba de notas fiscais"""
    global tree_notas, entry_numero_nf, entry_fornecedor_nf, entry_cnpj_nf, entry_data_emissao
    global entry_produto_nf, entry_quantidade_nf, entry_preco_nf, entry_validade_nf
    global tree_itens_nf, label_total_nf
    
    aba_nf = ttk.Frame(notebook)
    notebook.add(aba_nf, text="🧾 Notas Fiscais")
    
    # Frame principal
    main_frame = ttk.Frame(aba_nf, style='Card.TFrame')
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título
    title_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    title_frame.pack(fill="x", padx=20, pady=(20, 10))
    
    tk.Label(title_frame, text="Registro de Notas Fiscais", 
            font=('Segoe UI', 16, 'bold'), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).pack(side="left")
    
    # Frame de dados da NF
    nf_frame = tk.LabelFrame(main_frame, text="Dados da Nota Fiscal", 
                            font=('Segoe UI', 11, 'bold'),
                            fg=COLORS['text_primary'], bg=COLORS['surface'])
    nf_frame.pack(fill="x", padx=20, pady=10)
    
    # Linha 1 - dados da NF
    row1_nf = tk.Frame(nf_frame, bg=COLORS['surface'])
    row1_nf.pack(fill="x", padx=10, pady=10)
    
    tk.Label(row1_nf, text="Número NF:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=0, sticky="w")
    entry_numero_nf = tk.Entry(row1_nf, width=20, font=('Segoe UI', 10))
    entry_numero_nf.grid(row=1, column=0, padx=(0, 10), sticky="ew")
    
    tk.Label(row1_nf, text="Fornecedor:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=1, sticky="w")
    entry_fornecedor_nf = tk.Entry(row1_nf, width=30, font=('Segoe UI', 10))
    entry_fornecedor_nf.grid(row=1, column=1, padx=(0, 10), sticky="ew")
    
    tk.Label(row1_nf, text="CNPJ:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=2, sticky="w")
    entry_cnpj_nf = tk.Entry(row1_nf, width=20, font=('Segoe UI', 10))
    entry_cnpj_nf.grid(row=1, column=2, padx=(0, 10), sticky="ew")
    
    tk.Label(row1_nf, text="Data Emissão (dd/mm/aaaa):", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=3, sticky="w")
    entry_data_emissao = tk.Entry(row1_nf, width=15, font=('Segoe UI', 10))
    entry_data_emissao.grid(row=1, column=3, sticky="ew")
    
    # Frame de itens da NF
    itens_frame = tk.LabelFrame(main_frame, text="Itens da Nota Fiscal", 
                               font=('Segoe UI', 11, 'bold'),
                               fg=COLORS['text_primary'], bg=COLORS['surface'])
    itens_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    # Formulário de itens
    item_form = tk.Frame(itens_frame, bg=COLORS['surface'])
    item_form.pack(fill="x", padx=10, pady=10)
    
    tk.Label(item_form, text="Produto:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=0, sticky="w")
    entry_produto_nf = tk.Entry(item_form, width=25, font=('Segoe UI', 10))
    entry_produto_nf.grid(row=1, column=0, padx=(0, 10), sticky="ew")
    
    tk.Label(item_form, text="Quantidade:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=1, sticky="w")
    entry_quantidade_nf = tk.Entry(item_form, width=10, font=('Segoe UI', 10))
    entry_quantidade_nf.grid(row=1, column=1, padx=(0, 10), sticky="ew")
    
    tk.Label(item_form, text="Preço Unitário:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=2, sticky="w")
    entry_preco_nf = tk.Entry(item_form, width=12, font=('Segoe UI', 10))
    entry_preco_nf.grid(row=1, column=2, padx=(0, 10), sticky="ew")
    
    tk.Label(item_form, text="Validade (dd/mm/aaaa):", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=3, sticky="w")
    entry_validade_nf = tk.Entry(item_form, width=15, font=('Segoe UI', 10))
    entry_validade_nf.grid(row=1, column=3, padx=(0, 10), sticky="ew")
    
    btn_add_item = criar_botao_personalizado(item_form, "Adicionar Item", adicionar_item_nf, 
                                           COLORS['success'])
    btn_add_item.grid(row=1, column=4, padx=10)
    
    # Lista de itens temporários
    list_itens_frame = tk.Frame(itens_frame, bg=COLORS['surface'])
    list_itens_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    colunas_itens = ("Produto", "Quantidade", "Preço Unit.", "Subtotal", "Validade")
    tree_itens_nf = ttk.Treeview(list_itens_frame, columns=colunas_itens, show="headings", height=8)
    
    for col in colunas_itens:
        tree_itens_nf.heading(col, text=col)
        tree_itens_nf.column(col, width=120)
    
    # Scrollbars para itens
    scroll_itens_v = ttk.Scrollbar(list_itens_frame, orient="vertical", command=tree_itens_nf.yview)
    tree_itens_nf.configure(yscrollcommand=scroll_itens_v.set)
    
    tree_itens_nf.grid(row=0, column=0, sticky="nsew")
    scroll_itens_v.grid(row=0, column=1, sticky="ns")
    
    list_itens_frame.grid_rowconfigure(0, weight=1)
    list_itens_frame.grid_columnconfigure(0, weight=1)
    
    # Botões de ação para itens
    btn_itens_frame = tk.Frame(itens_frame, bg=COLORS['surface'])
    btn_itens_frame.pack(fill="x", padx=10, pady=10)
    
    btn_remover_item = criar_botao_personalizado(btn_itens_frame, "Remover Item", remover_item_nf, 
                                               COLORS['danger'])
    btn_remover_item.pack(side="left", padx=5)
    
    global label_total_nf
    label_total_nf = tk.Label(btn_itens_frame, text="Total da NF: R$ 0,00", 
                             font=('Segoe UI', 12, 'bold'), 
                             fg=COLORS['text_primary'], bg=COLORS['surface'])
    label_total_nf.pack(side="right")
    
    # Botões finais
    final_btn_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    final_btn_frame.pack(fill="x", padx=20, pady=20)
    
    btn_salvar_nf = criar_botao_personalizado(final_btn_frame, "Salvar Nota Fiscal", salvar_nota_fiscal, 
                                            COLORS['primary'])
    btn_salvar_nf.pack(side="left", padx=5)
    
    btn_limpar_nf = criar_botao_personalizado(final_btn_frame, "Limpar Formulário", limpar_formulario_nf, 
                                            COLORS['secondary'])
    btn_limpar_nf.pack(side="left", padx=5)

def criar_aba_usuarios(notebook):
    """Cria a aba de administração de usuários"""
    global tree_usuarios, entry_novo_usuario, entry_nova_senha, combo_nivel_usuario
    
    aba_usuarios = ttk.Frame(notebook)
    notebook.add(aba_usuarios, text="👤 Usuários")
    
    main_frame = ttk.Frame(aba_usuarios, style='Card.TFrame')
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título
    title_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    title_frame.pack(fill="x", padx=20, pady=(20, 10))
    
    tk.Label(title_frame, text="Administração de Usuários", 
            font=('Segoe UI', 16, 'bold'), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).pack(side="left")
    
    # Formulário de novo usuário
    form_frame = tk.LabelFrame(main_frame, text="Cadastrar Novo Usuário", 
                              font=('Segoe UI', 11, 'bold'),
                              fg=COLORS['text_primary'], bg=COLORS['surface'])
    form_frame.pack(fill="x", padx=20, pady=10)
    
    form_row = tk.Frame(form_frame, bg=COLORS['surface'])
    form_row.pack(fill="x", padx=10, pady=10)
    
    tk.Label(form_row, text="Usuário:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=0, sticky="w")
    entry_novo_usuario = tk.Entry(form_row, width=20, font=('Segoe UI', 10))
    entry_novo_usuario.grid(row=1, column=0, padx=(0, 10), sticky="ew")
    
    tk.Label(form_row, text="Senha:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=1, sticky="w")
    entry_nova_senha = tk.Entry(form_row, width=20, font=('Segoe UI', 10), show="*")
    entry_nova_senha.grid(row=1, column=1, padx=(0, 10), sticky="ew")
    
    tk.Label(form_row, text="Nível:", font=('Segoe UI', 10), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).grid(row=0, column=2, sticky="w")
    combo_nivel_usuario = ttk.Combobox(form_row, values=["admin", "comum"], width=12, font=('Segoe UI', 10))
    combo_nivel_usuario.grid(row=1, column=2, padx=(0, 10), sticky="ew")
    
    btn_cadastrar = criar_botao_personalizado(form_row, "Cadastrar", cadastrar_novo_usuario, 
                                            COLORS['success'])
    btn_cadastrar.grid(row=1, column=3, padx=10)
    
    # Lista de usuários
    list_frame = tk.LabelFrame(main_frame, text="Usuários Cadastrados", 
                              font=('Segoe UI', 11, 'bold'),
                              fg=COLORS['text_primary'], bg=COLORS['surface'])
    list_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
    tree_frame = tk.Frame(list_frame, bg=COLORS['surface'])
    tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    colunas_usuarios = ("Usuário", "Nível", "Data Criação")
    tree_usuarios = ttk.Treeview(tree_frame, columns=colunas_usuarios, show="headings", height=12)
    
    for col in colunas_usuarios:
        tree_usuarios.heading(col, text=col)
        tree_usuarios.column(col, width=150)
    
    scroll_usuarios = ttk.Scrollbar(tree_frame, orient="vertical", command=tree_usuarios.yview)
    tree_usuarios.configure(yscrollcommand=scroll_usuarios.set)
    
    tree_usuarios.grid(row=0, column=0, sticky="nsew")
    scroll_usuarios.grid(row=0, column=1, sticky="ns")
    
    tree_frame.grid_rowconfigure(0, weight=1)
    tree_frame.grid_columnconfigure(0, weight=1)
    
    btn_usuarios_frame = tk.Frame(list_frame, bg=COLORS['surface'])
    btn_usuarios_frame.pack(fill="x", padx=10, pady=10)
    
    btn_remover_usuario = criar_botao_personalizado(btn_usuarios_frame, "Remover Usuário", remover_usuario, 
                                                  COLORS['danger'])
    btn_remover_usuario.pack(side="left")
    
    # Carregar usuários existentes
    atualizar_lista_usuarios()

def criar_aba_relatorios(notebook):
    """Cria a aba de relatórios"""
    aba_relatorios = ttk.Frame(notebook)
    notebook.add(aba_relatorios, text="📊 Relatórios")
    
    main_frame = ttk.Frame(aba_relatorios, style='Card.TFrame')
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título
    title_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    title_frame.pack(fill="x", padx=20, pady=(20, 10))
    
    tk.Label(title_frame, text="Relatórios e Exportações", 
            font=('Segoe UI', 16, 'bold'), 
            fg=COLORS['text_primary'], bg=COLORS['surface']).pack(side="left")
    
    # Cards de relatórios
    cards_frame = tk.Frame(main_frame, bg=COLORS['surface'])
    cards_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Card Estoque Geral
    card1 = tk.LabelFrame(cards_frame, text="Estoque Geral", 
                         font=('Segoe UI', 12, 'bold'),
                         fg=COLORS['text_primary'], bg=COLORS['surface'])
    card1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", ipadx=20, ipady=20)
    
    tk.Label(card1, text="Relatório completo do estoque\ncom alertas de validade e estoque baixo", 
            font=('Segoe UI', 10), 
            fg=COLORS['text_secondary'], bg=COLORS['surface']).pack(pady=10)
    
    btn_rel_estoque = criar_botao_personalizado(card1, "Gerar Relatório", gerar_relatorio_estoque, 
                                              COLORS['primary'])
    btn_rel_estoque.pack()
    
    # Card Produtos Vencidos
    card2 = tk.LabelFrame(cards_frame, text="Produtos Vencidos", 
                         font=('Segoe UI', 12, 'bold'),
                         fg=COLORS['danger'], bg=COLORS['surface'])
    card2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", ipadx=20, ipady=20)
    
    tk.Label(card2, text="Lista de produtos vencidos\nou próximos ao vencimento", 
            font=('Segoe UI', 10), 
            fg=COLORS['text_secondary'], bg=COLORS['surface']).pack(pady=10)
    
    btn_rel_vencidos = criar_botao_personalizado(card2, "Verificar Vencidos", gerar_relatorio_vencidos, 
                                               COLORS['danger'])
    btn_rel_vencidos.pack()
    
    # Card Estoque Baixo
    card3 = tk.LabelFrame(cards_frame, text="Estoque Baixo", 
                         font=('Segoe UI', 12, 'bold'),
                         fg=COLORS['warning'], bg=COLORS['surface'])
    card3.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", ipadx=20, ipady=20)
    
    tk.Label(card3, text="Produtos com estoque\nabaixo do limite de alerta", 
            font=('Segoe UI', 10), 
            fg=COLORS['text_secondary'], bg=COLORS['surface']).pack(pady=10)
    
    btn_rel_baixo = criar_botao_personalizado(card3, "Verificar Estoque", gerar_relatorio_estoque_baixo, 
                                            COLORS['warning'])
    btn_rel_baixo.pack()
    
    # Card Exportações
    card4 = tk.LabelFrame(cards_frame, text="Exportações", 
                         font=('Segoe UI', 12, 'bold'),
                         fg=COLORS['success'], bg=COLORS['surface'])
    card4.grid(row=1, column=1, padx=10, pady=10, sticky="nsew", ipadx=20, ipady=20)
    
    tk.Label(card4, text="Exportar dados para\narquivos CSV ou Excel", 
            font=('Segoe UI', 10), 
            fg=COLORS['text_secondary'], bg=COLORS['surface']).pack(pady=10)
    
    btn_export = criar_botao_personalizado(card4, "Exportar CSV", exportar_csv, 
                                         COLORS['success'])
    btn_export.pack()
    
    # Configurar grid weights
    cards_frame.grid_columnconfigure(0, weight=1)
    cards_frame.grid_columnconfigure(1, weight=1)
    cards_frame.grid_rowconfigure(0, weight=1)
    cards_frame.grid_rowconfigure(1, weight=1)

# ---------------------------
# Funções do Estoque
# ---------------------------
def adicionar_produto():
    """Adiciona um novo produto ao estoque"""
    nome = entry_nome.get().strip()
    quantidade_str = entry_quantidade.get().strip()
    unidade = entry_unidade.get().strip()
    categoria = combo_categoria.get().strip()
    limite_str = entry_limite.get().strip()
    preco_custo_str = entry_preco_custo.get().strip()
    preco_venda_str = entry_preco_venda.get().strip()
    fornecedor = entry_fornecedor.get().strip()
    data_validade = entry_validade.get().strip()
    codigo_barras = entry_codigo.get().strip()
    
    erros = validar_entrada_produto(nome, quantidade_str, unidade, categoria, limite_str, 
                                  preco_custo_str, preco_venda_str, fornecedor, data_validade, codigo_barras)
    
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return
    
    # Verificar se código já existe
    for item in estoque:
        if item.get("codigo_barras", "") == codigo_barras:
            messagebox.showerror("Erro", "Código de barras já cadastrado!")
            return
    
    quantidade = int(quantidade_str)
    limite = int(limite_str) if limite_str else 0
    preco_custo = float(preco_custo_str.replace(',', '.'))
    preco_venda = float(preco_venda_str.replace(',', '.'))
    margem_lucro = round(preco_venda - preco_custo, 2)
    
    produto = {
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
        "movimentacoes": [{
            "tipo": "entrada_manual",
            "quantidade": quantidade,
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observacao": "Cadastro inicial"
        }]
    }
    
    estoque.append(produto)
    salvar_estoque(estoque)
    atualizar_lista_estoque()
    limpar_campos_produto()
    atualizar_contador_itens()
    
    messagebox.showinfo("Sucesso", f"Produto '{nome}' adicionado com sucesso!")

def editar_produto():
    """Edita o produto selecionado"""
    selecao = tree_estoque.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um produto para editar.")
        return

    item_selecionado = selecao[0]
    valores = tree_estoque.item(item_selecionado, "values")
    codigo_barras = valores[0]

    # Encontrar o índice correto na lista estoque
    index_item = next((i for i, p in enumerate(estoque) if p.get("codigo_barras") == codigo_barras), None)
    if index_item is None:
        messagebox.showerror("Erro", "Produto não encontrado no estoque.")
        return

    nome = entry_nome.get().strip()
    quantidade_str = entry_quantidade.get().strip()
    unidade = entry_unidade.get().strip()
    categoria = combo_categoria.get().strip()
    limite_str = entry_limite.get().strip()
    preco_custo_str = entry_preco_custo.get().strip()
    preco_venda_str = entry_preco_venda.get().strip()
    fornecedor = entry_fornecedor.get().strip()
    data_validade = entry_validade.get().strip()
    codigo_barras = entry_codigo.get().strip()
    
    erros = validar_entrada_produto(nome, quantidade_str, unidade, categoria, limite_str, 
                                  preco_custo_str, preco_venda_str, fornecedor, data_validade, codigo_barras)
    
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return
    
    quantidade = int(quantidade_str)
    limite = int(limite_str) if limite_str else 0
    preco_custo = float(preco_custo_str.replace(',', '.'))
    preco_venda = float(preco_venda_str.replace(',', '.'))
    margem_lucro = round(preco_venda - preco_custo, 2)
    
    # Registrar movimentação se houve alteração na quantidade
    quantidade_anterior = estoque[index_item].get("quantidade", 0)
    if quantidade != quantidade_anterior:
        diferenca = quantidade - quantidade_anterior
        tipo_mov = "ajuste_positivo" if diferenca > 0 else "ajuste_negativo"
        estoque[index_item]["movimentacoes"].append({
            "tipo": tipo_mov,
            "quantidade": abs(diferenca),
            "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "observacao": f"Ajuste manual: {quantidade_anterior} → {quantidade}"
        })
    
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
    atualizar_lista_estoque()
    limpar_campos_produto()
    atualizar_contador_itens()
    
    messagebox.showinfo("Sucesso", f"Produto '{nome}' atualizado com sucesso!")

def remover_produto():
    """Remove o produto selecionado"""
    selecao = tree_estoque.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um produto para remover.")
        return
    
    item_selecionado = selecao[0]
    index_item = tree_estoque.index(item_selecionado)
    nome_produto = estoque[index_item]["nome"]
    
    resposta = messagebox.askyesno("Confirmação", 
                                  f"Tem certeza que deseja remover o produto '{nome_produto}'?")
    if not resposta:
        return
    
    estoque.pop(index_item)
    salvar_estoque(estoque)
    atualizar_lista_estoque()
    limpar_campos_produto()
    atualizar_contador_itens()
    
    messagebox.showinfo("Sucesso", f"Produto '{nome_produto}' removido com sucesso!")

def carregar_produto_para_edicao(event=None):
    """Carrega os dados do produto selecionado para edição"""
    selecao = tree_estoque.selection()
    if not selecao:
        return
    
    item_selecionado = selecao[0]
    index_item = tree_estoque.index(item_selecionado)
    produto = estoque[index_item]
    
    limpar_campos_produto()
    
    entry_codigo.insert(0, produto.get("codigo_barras", ""))
    entry_nome.insert(0, produto.get("nome", ""))
    entry_quantidade.insert(0, str(produto.get("quantidade", "")))
    entry_unidade.insert(0, produto.get("unidade", ""))
    combo_categoria.set(produto.get("categoria", ""))
    entry_limite.insert(0, str(produto.get("limite_alerta", "")))
    entry_preco_custo.insert(0, str(produto.get("preco_custo", "")))
    entry_preco_venda.insert(0, str(produto.get("preco_venda", "")))
    entry_fornecedor.insert(0, produto.get("fornecedor", ""))
    entry_validade.insert(0, produto.get("data_validade", ""))

def limpar_campos_produto():
    """Limpa todos os campos do formulário de produto"""
    entry_codigo.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_unidade.delete(0, tk.END)
    combo_categoria.set('')
    entry_limite.delete(0, tk.END)
    entry_preco_custo.delete(0, tk.END)
    entry_preco_venda.delete(0, tk.END)
    entry_fornecedor.delete(0, tk.END)
    entry_validade.delete(0, tk.END)

def buscar_produto():
    """Busca produtos por nome, categoria ou código"""
    termo = entry_busca.get().strip().lower()
    if not termo:
        atualizar_lista_estoque()
        return
    
    # Limpar árvore
    for item in tree_estoque.get_children():
        tree_estoque.delete(item)
    
    # Filtrar e exibir produtos
    produtos_encontrados = []
    for produto in estoque:
        if (termo in produto.get("nome", "").lower() or 
            termo in produto.get("categoria", "").lower() or
            termo in produto.get("codigo_barras", "")):
            produtos_encontrados.append(produto)
    
    exibir_produtos_na_tree(produtos_encontrados)

def atualizar_lista_estoque():
    """Atualiza a lista de produtos na treeview"""
    exibir_produtos_na_tree(estoque)

def exibir_produtos_na_tree(produtos):
    """Exibe uma lista de produtos na treeview"""
    # Limpar árvore
    for item in tree_estoque.get_children():
        tree_estoque.delete(item)
    
    for i, produto in enumerate(produtos):
        # Determinar status do produto
        quantidade = produto.get("quantidade", 0)
        limite = produto.get("limite_alerta", 0)
        data_validade = produto.get("data_validade", "")
        
        status = "Normal"
        tag = 'par' if i % 2 == 0 else 'impar'
        
        # Verificar se está com estoque baixo
        if quantidade <= limite:
            status = "Estoque Baixo"
            tag = 'baixo_estoque'
        
        # Verificar se está vencido ou próximo do vencimento
        if data_validade:
            try:
                validade = datetime.strptime(data_validade, "%d/%m/%Y")
                dias_para_vencer = (validade - datetime.now()).days
                if dias_para_vencer < 0:
                    status = "Vencido"
                    tag = 'vencido'
                elif dias_para_vencer <= 30:
                    status = "Próx. Vencimento"
                    if tag != 'baixo_estoque':  # Manter prioridade do estoque baixo
                        tag = 'vencido'
            except ValueError:
                pass
        
        # Inserir na árvore
        tree_estoque.insert("", tk.END, 
            values=(
                produto.get("codigo_barras", ""),
                produto.get("nome", ""),
                quantidade,
                produto.get("unidade", ""),
                produto.get("categoria", ""),
                f"R$ {produto.get('preco_custo', 0):.2f}",
                f"R$ {produto.get('preco_venda', 0):.2f}",
                f"R$ {produto.get('margem_lucro', 0):.2f}",
                produto.get("fornecedor", ""),
                data_validade,
                status
            ), 
            tags=(tag,))

def atualizar_contador_itens():
    """Atualiza o contador de itens no header"""
    total_produtos = len(estoque)
    total_quantidade = sum(item.get("quantidade", 0) for item in estoque)
    itens_baixo_estoque = sum(1 for item in estoque if item.get("quantidade", 0) <= item.get("limite_alerta", 0))
    
    # Contar produtos vencidos ou próximos ao vencimento
    produtos_vencidos = 0
    for item in estoque:
        data_validade = item.get("data_validade", "")
        if data_validade:
            try:
                validade = datetime.strptime(data_validade, "%d/%m/%Y")
                if (validade - datetime.now()).days <= 30:
                    produtos_vencidos += 1
            except ValueError:
                pass
    
    label_contador.config(
        text=f"Produtos: {total_produtos} | Quantidade: {total_quantidade} | Alertas: {itens_baixo_estoque} | Vencimento: {produtos_vencidos}"
    )

# ---------------------------
# Funções de Notas Fiscais
# ---------------------------
def validar_dados_nf():
    """Valida os dados da nota fiscal"""
    erros = []
    numero = entry_numero_nf.get().strip()
    fornecedor = entry_fornecedor_nf.get().strip()
    cnpj = entry_cnpj_nf.get().strip()
    data_emissao = entry_data_emissao.get().strip()
    
    if not numero:
        erros.append("Número da NF é obrigatório")
    if not fornecedor:
        erros.append("Fornecedor é obrigatório")
    if not cnpj:
        erros.append("CNPJ é obrigatório")
    elif len(cnpj.replace('.', '').replace('/', '').replace('-', '')) != 14:
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
    """Valida os dados de um item da NF"""
    erros = []
    produto = entry_produto_nf.get().strip()
    quantidade_str = entry_quantidade_nf.get().strip()
    preco_str = entry_preco_nf.get().strip()
    validade = entry_validade_nf.get().strip()
    
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
    if validade:
        try:
            datetime.strptime(validade, "%d/%m/%Y")
        except ValueError:
            erros.append("Data de validade inválida (DD/MM/AAAA)")
    
    return erros

def adicionar_item_nf():
    """Adiciona um item à lista temporária da NF"""
    erros = validar_item_nf()
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return
    
    produto = entry_produto_nf.get().strip()
    quantidade = int(entry_quantidade_nf.get().strip())
    preco_unitario = float(entry_preco_nf.get().strip().replace(',', '.'))
    validade = entry_validade_nf.get().strip()
    subtotal = round(quantidade * preco_unitario, 2)
    
    item = {
        "produto": produto,
        "quantidade": quantidade,
        "preco_unitario": preco_unitario,
        "subtotal": subtotal,
        "data_validade": validade
    }
    
    itens_nf_temporarios.append(item)
    atualizar_lista_itens_nf()
    limpar_campos_item_nf()
    
    messagebox.showinfo("Sucesso", f"Item '{produto}' adicionado à NF!")

def remover_item_nf():
    """Remove um item da lista temporária da NF"""
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
    """Atualiza a lista de itens temporários da NF"""
    # Limpar árvore
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
    """Limpa os campos do formulário de item da NF"""
    entry_produto_nf.delete(0, tk.END)
    entry_quantidade_nf.delete(0, tk.END)
    entry_preco_nf.delete(0, tk.END)
    entry_validade_nf.delete(0, tk.END)

def limpar_formulario_nf():
    """Limpa todo o formulário de NF"""
    entry_numero_nf.delete(0, tk.END)
    entry_fornecedor_nf.delete(0, tk.END)
    entry_cnpj_nf.delete(0, tk.END)
    entry_data_emissao.delete(0, tk.END)
    limpar_campos_item_nf()
    itens_nf_temporarios.clear()
    atualizar_lista_itens_nf()

def salvar_nota_fiscal():
    """Salva a nota fiscal e atualiza o estoque"""
    erros = validar_dados_nf()
    if erros:
        messagebox.showerror("Erro de Validação", "\n".join(erros))
        return
    
    if not itens_nf_temporarios:
        messagebox.showwarning("Aviso", "Adicione pelo menos um item à NF!")
        return
    
    numero = entry_numero_nf.get().strip()
    fornecedor = entry_fornecedor_nf.get().strip()
    cnpj = entry_cnpj_nf.get().strip()
    data_emissao = entry_data_emissao.get().strip()
    
    # Verificar se NF já existe
    for nf in notas:
        if nf.get("numero") == numero:
            messagebox.showerror("Erro", "Número de NF já cadastrado!")
            return
    
    nota_fiscal = {
        "numero": numero,
        "fornecedor": fornecedor,
        "cnpj": cnpj,
        "data_emissao": data_emissao,
        "itens": itens_nf_temporarios.copy(),
        "data_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "total": sum(item["subtotal"] for item in itens_nf_temporarios)
    }
    
    notas.append(nota_fiscal)
    salvar_notas(notas)
    
    # Atualizar estoque
    atualizados, novos = atualizar_estoque_com_nf(itens_nf_temporarios, numero, fornecedor)
    
    limpar_formulario_nf()
    atualizar_lista_estoque()
    atualizar_contador_itens()
    
    messagebox.showinfo("Sucesso", 
                       f"NF {numero} registrada com sucesso!\n"
                       f"Produtos atualizados: {atualizados}\n"
                       f"Produtos novos: {novos}")

def atualizar_estoque_com_nf(itens_nf, numero_nf, fornecedor):
    """Atualiza o estoque com base nos itens da NF"""
    itens_atualizados = 0
    itens_novos = 0
    
    for item_nf in itens_nf:
        produto_encontrado = False
        
        # Procurar produto existente pelo nome
        for produto in estoque:
            if produto.get("nome", "").lower() == item_nf["produto"].lower():
                # Atualizar quantidade
                produto["quantidade"] = produto.get("quantidade", 0) + item_nf["quantidade"]
                produto["data_atualizacao"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                # Registrar movimentação
                produto["movimentacoes"].append({
                    "tipo": "entrada_nf",
                    "quantidade": item_nf["quantidade"],
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "observacao": f"NF {numero_nf} - {fornecedor}"
                })
                
                produto_encontrado = True
                itens_atualizados += 1
                break
        
        # Se não encontrou, criar novo produto
        if not produto_encontrado:
            novo_codigo = f"NF{numero_nf}{len(estoque) + 1:03d}"
            
            novo_produto = {
                "codigo_barras": novo_codigo,
                "nome": item_nf["produto"],
                "quantidade": item_nf["quantidade"],
                "unidade": "un",
                "categoria": "Outros",
                "limite_alerta": 5,
                "preco_custo": item_nf["preco_unitario"],
                "preco_venda": item_nf["preco_unitario"] * 1.3,  # Margem padrão de 30%
                "margem_lucro": item_nf["preco_unitario"] * 0.3,
                "fornecedor": fornecedor,
                "data_validade": item_nf.get("data_validade", ""),
                "data_cadastro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "movimentacoes": [{
                    "tipo": "entrada_nf",
                    "quantidade": item_nf["quantidade"],
                    "data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "observacao": f"NF {numero_nf} - {fornecedor} (Produto novo)"
                }]
            }
            
            estoque.append(novo_produto)
            itens_novos += 1
    
    salvar_estoque(estoque)
    return itens_atualizados, itens_novos

# ---------------------------
# Funções de Usuários
# ---------------------------
def cadastrar_novo_usuario():
    """Cadastra um novo usuário no sistema"""
    usuario = entry_novo_usuario.get().strip()
    senha = entry_nova_senha.get().strip()
    nivel = combo_nivel_usuario.get().strip()
    
    if not usuario or not senha or not nivel:
        messagebox.showerror("Erro", "Preencha todos os campos")
        return
    
    # Verificar se usuário já existe
    for u in usuarios:
        if u["usuario"] == usuario:
            messagebox.showerror("Erro", "Usuário já existe!")
            return
    
    novo_usuario = {
        "usuario": usuario,
        "senha": senha,
        "nivel": nivel,
        "data_criacao": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    atualizar_lista_usuarios()
    
    # Limpar campos
    entry_novo_usuario.delete(0, tk.END)
    entry_nova_senha.delete(0, tk.END)
    combo_nivel_usuario.set('')
    
    messagebox.showinfo("Sucesso", f"Usuário '{usuario}' cadastrado com sucesso!")

def remover_usuario():
    """Remove o usuário selecionado"""
    selecao = tree_usuarios.selection()
    if not selecao:
        messagebox.showerror("Erro", "Selecione um usuário para remover")
        return
    
    item_selecionado = selecao[0]
    index_item = tree_usuarios.index(item_selecionado)
    usuario_remover = usuarios[index_item]["usuario"]
    
    if usuario_remover == "admin":
        messagebox.showerror("Erro", "Não é possível remover o usuário admin")
        return
    
    if usuario_remover == usuario_logado["usuario"]:
        messagebox.showerror("Erro", "Não é possível remover o próprio usuário")
        return
    
    resposta = messagebox.askyesno("Confirmação", f"Remover usuário '{usuario_remover}'?")
    if resposta:
        usuarios.pop(index_item)
        salvar_usuarios(usuarios)
        atualizar_lista_usuarios()
        messagebox.showinfo("Sucesso", f"Usuário '{usuario_remover}' removido!")

def atualizar_lista_usuarios():
    """Atualiza a lista de usuários na treeview"""
    for item in tree_usuarios.get_children():
        tree_usuarios.delete(item)
    
    for usuario in usuarios:
        tree_usuarios.insert("", tk.END, values=(
            usuario["usuario"],
            usuario["nivel"],
            usuario.get("data_criacao", "N/A")
        ))

# ---------------------------
# Funções de Relatórios
# ---------------------------
def gerar_relatorio_estoque():
    """Gera relatório completo do estoque"""
    if not estoque:
        messagebox.showwarning("Aviso", "Não há produtos no estoque para gerar relatório.")
        return
    
    janela_relatorio = tk.Toplevel(root)
    janela_relatorio.title("Relatório de Estoque")
    janela_relatorio.geometry("900x700")
    janela_relatorio.configure(bg=COLORS['background'])
    
    # Frame com scrollbar
    main_frame = tk.Frame(janela_relatorio, bg=COLORS['surface'])
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Scrollbar
    scrollbar = tk.Scrollbar(main_frame)
    scrollbar.pack(side="right", fill="y")
    
    # Text widget
    text_relatorio = tk.Text(main_frame, wrap="word", yscrollcommand=scrollbar.set, 
                            font=('Segoe UI', 10), bg=COLORS['surface'])
    text_relatorio.pack(fill="both", expand=True)
    scrollbar.config(command=text_relatorio.yview)
    
    # Configurar tags
    text_relatorio.tag_configure("titulo", font=('Segoe UI', 16, 'bold'), foreground=COLORS['primary'])
    text_relatorio.tag_configure("subtitulo", font=('Segoe UI', 12, 'bold'), foreground=COLORS['secondary'])
    text_relatorio.tag_configure("alerta", foreground=COLORS['danger'], font=('Segoe UI', 10, 'bold'))
    text_relatorio.tag_configure("sucesso", foreground=COLORS['success'])
    
    # Gerar conteúdo do relatório
    data_atual = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    
    text_relatorio.insert(tk.END, "RELATÓRIO GERAL DE ESTOQUE\n", ("titulo",))
    text_relatorio.insert(tk.END, f"Gerado em: {data_atual}\n\n")
    
    # Estatísticas gerais
    total_produtos = len(estoque)
    total_quantidade = sum(p.get("quantidade", 0) for p in estoque)
    valor_total_custo = sum(p.get("quantidade", 0) * p.get("preco_custo", 0) for p in estoque)
    valor_total_venda = sum(p.get("quantidade", 0) * p.get("preco_venda", 0) for p in estoque)
    
    text_relatorio.insert(tk.END, "RESUMO GERAL\n", ("subtitulo",))
    text_relatorio.insert(tk.END, f"Total de produtos cadastrados: {total_produtos}\n")
    text_relatorio.insert(tk.END, f"Quantidade total em estoque: {total_quantidade} unidades\n")
    text_relatorio.insert(tk.END, f"Valor total (custo): R$ {valor_total_custo:.2f}\n")
    text_relatorio.insert(tk.END, f"Valor total (venda): R$ {valor_total_venda:.2f}\n")
    text_relatorio.insert(tk.END, f"Margem de lucro total: R$ {valor_total_venda - valor_total_custo:.2f}\n\n")
    
    # Produtos com estoque baixo
    produtos_baixo_estoque = [p for p in estoque if p.get("quantidade", 0) <= p.get("limite_alerta", 0)]
    if produtos_baixo_estoque:
        text_relatorio.insert(tk.END, "ALERTAS DE ESTOQUE BAIXO\n", ("alerta",))
        for produto in produtos_baixo_estoque:
            text_relatorio.insert(tk.END, 
                f"• {produto['nome']}: {produto['quantidade']} {produto.get('unidade', '')} "
                f"(Limite: {produto.get('limite_alerta', 0)})\n", ("alerta",))
        text_relatorio.insert(tk.END, "\n")
    
    # Produtos próximos ao vencimento
    produtos_vencimento = []
    for produto in estoque:
        data_validade = produto.get("data_validade", "")
        if data_validade:
            try:
                validade = datetime.strptime(data_validade, "%d/%m/%Y")
                dias_para_vencer = (validade - datetime.now()).days
                if dias_para_vencer <= 30:
                    produtos_vencimento.append((produto, dias_para_vencer))
            except ValueError:
                pass
    
    if produtos_vencimento:
        text_relatorio.insert(tk.END, "ALERTAS DE VENCIMENTO (30 dias)\n", ("alerta",))
        produtos_vencimento.sort(key=lambda x: x[1])  # Ordenar por dias para vencer
        for produto, dias in produtos_vencimento:
            if dias < 0:
                status = "VENCIDO"
            else:
                status = "PRÓXIMO"
            text_relatorio.insert(tk.END, 
                f"• {produto['nome']}: {status} (Validade: {produto.get('data_validade', '')})\n", ("alerta",))
        text_relatorio.insert(tk.END, "\n")
    
    # Produtos por categoria
    text_relatorio.insert(tk.END, "PRODUTOS POR CATEGORIA\n", ("subtitulo",))
    categorias = {}
    for produto in estoque:
        categoria = produto.get("categoria", "Outros")
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append(produto)
    
    for categoria, produtos in sorted(categorias.items()):
        text_relatorio.insert(tk.END, f"\n{categoria.upper()}\n", ("subtitulo",))
        qtd_categoria = sum(p.get("quantidade", 0) for p in produtos)
        text_relatorio.insert(tk.END, f"Total na categoria: {qtd_categoria} unidades\n")
        
        for produto in sorted(produtos, key=lambda x: x.get('nome', '')):
            status_icons = []
            if produto.get("quantidade", 0) <= produto.get("limite_alerta", 0):
                status_icons.append("⚠️")
            
            data_val = produto.get("data_validade", "")
            if data_val:
                try:
                    validade = datetime.strptime(data_val, "%d/%m/%Y")
                    if (validade - datetime.now()).days <= 30:
                        status_icons.append("📅")
                except ValueError:
                    pass
            
            status_str = " ".join(status_icons)
            text_relatorio.insert(tk.END, 
                f"  • {produto.get('nome', '')}: {produto.get('quantidade', 0)} {produto.get('unidade', '')} "
                f"- R$ {produto.get('preco_venda', 0):.2f} {status_str}\n")
    
    text_relatorio.config(state=tk.DISABLED)
    
    # Botão para salvar relatório
    btn_salvar = criar_botao_personalizado(janela_relatorio, "Salvar Relatório", 
                                         lambda: salvar_relatorio_arquivo(text_relatorio.get(1.0, tk.END)), 
                                         COLORS['success'])
    btn_salvar.pack(pady=10)

def gerar_relatorio_vencidos():
    """Gera relatório de produtos vencidos ou próximos ao vencimento"""
    produtos_vencimento = []
    
    for produto in estoque:
        data_validade = produto.get("data_validade", "")
        if data_validade:
            try:
                validade = datetime.strptime(data_validade, "%d/%m/%Y")
                dias_para_vencer = (validade - datetime.now()).days
                if dias_para_vencer <= 30:
                    produtos_vencimento.append((produto, dias_para_vencer))
            except ValueError:
                pass
    
    if not produtos_vencimento:
        messagebox.showinfo("Relatório de Vencimentos", 
                           "Não há produtos vencidos ou próximos ao vencimento (30 dias).")
        return
    
    # Criar janela de relatório
    janela = tk.Toplevel(root)
    janela.title("Produtos com Vencimento Próximo")
    janela.geometry("800x600")
    janela.configure(bg=COLORS['background'])
    
    # Frame principal
    main_frame = tk.Frame(janela, bg=COLORS['surface'])
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Título
    tk.Label(main_frame, text="PRODUTOS PRÓXIMOS AO VENCIMENTO", 
            font=('Segoe UI', 16, 'bold'), 
            fg=COLORS['danger'], bg=COLORS['surface']).pack(pady=10)
    
    # Treeview
    colunas = ("Produto", "Quantidade", "Validade", "Dias para Vencer", "Status")
    tree_vencidos = ttk.Treeview(main_frame, columns=colunas, show="headings", height=15)
    
    for col in colunas:
        tree_vencidos.heading(col, text=col)
        tree_vencidos.column(col, width=150)
    
    # Scrollbar
    scroll_vencidos = ttk.Scrollbar(main_frame, orient="vertical", command=tree_vencidos.yview)
    tree_vencidos.configure(yscrollcommand=scroll_vencidos.set)
    
    # Pack treeview
    tree_vencidos.pack(side="left", fill="both", expand=True)
    scroll_vencidos.pack(side="right", fill="y")
    
    tree_vencidos.tag_configure('vencido', background=COLORS['expired'])
    tree_vencidos.tag_configure('proximo', background='#fff3cd')
    
    # Preencher dados
    produtos_vencimento.sort(key=lambda x: x[1])  # Ordenar por dias
    
    for produto, dias in produtos_vencimento:
        if dias < 0:
            status = "VENCIDO"
            tag = 'vencido'
            dias_texto = f"{abs(dias)} dias atrás"
        else:
            status = "PRÓXIMO"
            tag = 'proximo'
            dias_texto = f"{dias} dias"
        
        tree_vencidos.insert("", tk.END, 
            values=(
                produto.get('nome', ''),
                f"{produto.get('quantidade', 0)} {produto.get('unidade', '')}",
                produto.get('data_validade', ''),
                dias_texto,
                status
            ),
            tags=(tag,))

def gerar_relatorio_estoque_baixo():
    """Gera relatório de produtos com estoque baixo"""
    produtos_baixo = [p for p in estoque if p.get("quantidade", 0) <= p.get("limite_alerta", 0)]
    
    if not produtos_baixo:
        messagebox.showinfo("Relatório de Estoque Baixo", 
                           "Não há produtos com estoque abaixo do limite de alerta.")
        return
    
    # Criar janela
    janela = tk.Toplevel(root)
    janela.title("Produtos com Estoque Baixo")
    janela.geometry("800x600")
    janela.configure(bg=COLORS['background'])
    
    main_frame = tk.Frame(janela, bg=COLORS['surface'])
    main_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
    tk.Label(main_frame, text="PRODUTOS COM ESTOQUE BAIXO", 
            font=('Segoe UI', 16, 'bold'), 
            fg=COLORS['warning'], bg=COLORS['surface']).pack(pady=10)
    
    # Treeview
    colunas = ("Produto", "Estoque Atual", "Limite Alerta", "Fornecedor", "Categoria")
    tree_baixo = ttk.Treeview(main_frame, columns=colunas, show="headings", height=15)
    
    for col in colunas:
        tree_baixo.heading(col, text=col)
        tree_baixo.column(col, width=150)
    
    scroll_baixo = ttk.Scrollbar(main_frame, orient="vertical", command=tree_baixo.yview)
    tree_baixo.configure(yscrollcommand=scroll_baixo.set)
    
    tree_baixo.pack(side="left", fill="both", expand=True)
    scroll_baixo.pack(side="right", fill="y")
    
    tree_baixo.tag_configure('baixo', background=COLORS['low_stock'])
    
    # Preencher dados
    for produto in produtos_baixo:
        tree_baixo.insert("", tk.END, 
            values=(
                produto.get('nome', ''),
                f"{produto.get('quantidade', 0)} {produto.get('unidade', '')}",
                produto.get('limite_alerta', 0),
                produto.get('fornecedor', ''),
                produto.get('categoria', '')
            ),
            tags=('baixo',))

def salvar_relatorio_arquivo(conteudo):
    """Salva o relatório em arquivo de texto"""
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Arquivos de Texto", "*.txt"), ("Todos os arquivos", "*.*")],
        title="Salvar Relatório"
    )
    
    if not arquivo:
        return
    
    try:
        with open(arquivo, 'w', encoding='utf-8') as f:
            f.write(conteudo)
        messagebox.showinfo("Sucesso", f"Relatório salvo em: {arquivo}")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao salvar relatório: {e}")

def exportar_csv():
    """Exporta o estoque atual para arquivo CSV"""
    if not estoque:
        messagebox.showwarning("Aviso", "Não há produtos para exportar.")
        return
    
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        title="Exportar Estoque para CSV"
    )
    
    if not arquivo:
        return
    
    try:
        with open(arquivo, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            
            # Cabeçalho
            writer.writerow([
                "Código de Barras", "Nome", "Quantidade", "Unidade", "Categoria",
                "Limite Alerta", "Preço Custo", "Preço Venda", "Margem Lucro",
                "Fornecedor", "Data Validade", "Data Cadastro"
            ])
            
            # Dados
            for produto in estoque:
                writer.writerow([
                    produto.get("codigo_barras", ""),
                    produto.get("nome", ""),
                    produto.get("quantidade", 0),
                    produto.get("unidade", ""),
                    produto.get("categoria", ""),
                    produto.get("limite_alerta", 0),
                    produto.get("preco_custo", 0),
                    produto.get("preco_venda", 0),
                    produto.get("margem_lucro", 0),
                    produto.get("fornecedor", ""),
                    produto.get("data_validade", ""),
                    produto.get("data_cadastro", "")
                ])
        
        messagebox.showinfo("Sucesso", f"Estoque exportado para: {arquivo}")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao exportar: {e}")

# ---------------------------
# INICIALIZAÇÃO DO SISTEMA
# ---------------------------
if __name__ == "__main__":
    # Inicializar o sistema
    iniciar_login()