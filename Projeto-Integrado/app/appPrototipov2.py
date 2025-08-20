import tkinter as tk
from tkinter import messagebox
import json
import os

# --- Funções de Banco de Dados (JSON) ---
# O nome do arquivo onde os dados serão salvos
DATABASE_FILE = "pacientes.json"

def carregar_dados():
    """Carrega a lista de pacientes do arquivo JSON. Se o arquivo não existir, retorna uma lista vazia."""
    if os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "r") as file:
            return json.load(file)
    return []

def salvar_dados(dados):
    """Salva a lista de pacientes no arquivo JSON."""
    with open(DATABASE_FILE, "w") as file:
        json.dump(dados, file, indent=4)

# --- Variáveis Globais ---
# A lista de pacientes agora é carregada do arquivo ao iniciar
pacientes = carregar_dados()

# --- Funções do Aplicativo (Lógica de Negócio) ---
def cadastrar_paciente():
    """Coleta os dados dos campos da interface e adiciona um novo paciente."""
    nome = entry_nome.get()
    idade_str = entry_idade.get()
    telefone = entry_telefone.get()

    if not nome or not idade_str or not telefone:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        return
        
    try:
        idade = int(idade_str)
        paciente = {"nome": nome, "idade": idade, "telefone": telefone}
        pacientes.append(paciente)
        salvar_dados(pacientes)
        messagebox.showinfo("Sucesso", "Paciente cadastrado com sucesso!")
        
        # Limpar os campos para o próximo cadastro
        entry_nome.delete(0, tk.END)
        entry_idade.delete(0, tk.END)
        entry_telefone.delete(0, tk.END)

    except ValueError:
        messagebox.showerror("Erro", "Idade inválida! Digite um número inteiro.")

def ver_estatisticas():
    """Calcula e exibe as estatísticas dos pacientes."""
    if not pacientes:
        messagebox.showinfo("Estatísticas", "Nenhum paciente cadastrado.")
        return

    total = len(pacientes)
    media_idade = sum(p["idade"] for p in pacientes) / total if total > 0 else 0
    paciente_mais_velho = max(pacientes, key=lambda p: p["idade"])
    paciente_mais_novo = min(pacientes, key=lambda p: p["idade"])

    estatisticas_texto = f"""
Total de pacientes: {total}
Média de idade: {media_idade:.2f}
Paciente mais velho: {paciente_mais_velho['nome']} ({paciente_mais_velho['idade']} anos)
Paciente mais novo: {paciente_mais_novo['nome']} ({paciente_mais_novo['idade']} anos)
    """
    messagebox.showinfo("Estatísticas da Clínica", estatisticas_texto)

def buscar_paciente():
    """Busca pacientes por nome e exibe os resultados."""
    nome_busca = entry_busca.get()
    if not nome_busca:
        messagebox.showerror("Erro", "Digite um nome para buscar!")
        return

    encontrados = [p for p in pacientes if nome_busca.lower() in p["nome"].lower()]
    
    if encontrados:
        resultados = "Pacientes Encontrados:\n"
        for p in encontrados:
            resultados += f"Nome: {p['nome']}, Idade: {p['idade']}, Telefone: {p['telefone']}\n"
        messagebox.showinfo("Resultados da Busca", resultados)
    else:
        messagebox.showinfo("Resultados da Busca", "Paciente não encontrado.")

def listar_pacientes():
    """Exibe a lista completa de pacientes em uma nova janela."""
    if not pacientes:
        messagebox.showinfo("Lista de Pacientes", "Nenhum paciente cadastrado.")
        return

    # Cria uma nova janela para exibir a lista
    janela_lista = tk.Toplevel(root)
    janela_lista.title("Lista de Todos os Pacientes")
    
    # Cria uma barra de rolagem
    scrollbar = tk.Scrollbar(janela_lista)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Cria um widget de texto para exibir os pacientes
    lista_texto = tk.Text(janela_lista, wrap="word", yscrollcommand=scrollbar.set)
    scrollbar.config(command=lista_texto.yview)
    lista_texto.pack(expand=True, fill="both")
    
    if pacientes:
        for p in pacientes:
            lista_texto.insert(tk.END, f"Nome: {p['nome']}, Idade: {p['idade']}, Telefone: {p['telefone']}\n\n")
    
    lista_texto.config(state=tk.DISABLED) # Desabilita a edição do texto

# --- Configuração da Interface Gráfica (Tkinter) ---
root = tk.Tk()
root.title("Sistema Clínica Vida+")

# Frame para o Cadastro de Pacientes
frame_cadastro = tk.LabelFrame(root, text="Cadastrar Paciente", padx=10, pady=10)
frame_cadastro.pack(padx=10, pady=10)

tk.Label(frame_cadastro, text="Nome:").grid(row=0, column=0, sticky="w")
entry_nome = tk.Entry(frame_cadastro, width=30)
entry_nome.grid(row=0, column=1)

tk.Label(frame_cadastro, text="Idade:").grid(row=1, column=0, sticky="w")
entry_idade = tk.Entry(frame_cadastro, width=30)
entry_idade.grid(row=1, column=1)

tk.Label(frame_cadastro, text="Telefone:").grid(row=2, column=0, sticky="w")
entry_telefone = tk.Entry(frame_cadastro, width=30)
entry_telefone.grid(row=2, column=1)

botao_cadastrar = tk.Button(frame_cadastro, text="Cadastrar", command=cadastrar_paciente)
botao_cadastrar.grid(row=3, column=0, columnspan=2, pady=10)

# Frame para a Busca de Pacientes
frame_busca = tk.LabelFrame(root, text="Buscar Paciente", padx=10, pady=10)
frame_busca.pack(padx=10, pady=10)

tk.Label(frame_busca, text="Nome:").grid(row=0, column=0, sticky="w")
entry_busca = tk.Entry(frame_busca, width=30)
entry_busca.grid(row=0, column=1)

botao_buscar = tk.Button(frame_busca, text="Buscar", command=buscar_paciente)
botao_buscar.grid(row=0, column=2, padx=5)

# Frame para os Botões de Ação
frame_botoes = tk.Frame(root, padx=10, pady=10)
frame_botoes.pack(padx=10, pady=10)

botao_estatisticas = tk.Button(frame_botoes, text="Ver Estatísticas", command=ver_estatisticas)
botao_estatisticas.pack(side="left", padx=5)

botao_listar = tk.Button(frame_botoes, text="Listar Todos", command=listar_pacientes)
botao_listar.pack(side="left", padx=5)

botao_sair = tk.Button(frame_botoes, text="Sair", command=root.quit)
botao_sair.pack(side="left", padx=5)

# Iniciar o loop principal da interface
root.mainloop()