import json

json_str = '''[
  {
    "titulo": "Dom Casmurro",
    "autor": "Machado de Assis",
    "ano_publicacao": 1899,
    "genero": "Romance",
    "cidade": "Rio de Janeiro"
  },
  {
    "titulo": "O Pequeno Príncipe",
    "autor": "Antoine de Saint-Exupéry",
    "ano_publicacao": 1943,
    "genero": "Fábula",
    "cidade": "Paris"
  },
  {
    "titulo": "1984",
    "autor": "George Orwell",
    "ano_publicacao": 1949,
    "genero": "Distopia",
    "cidade": "Londres"
  }
]'''
dados = json.loads(json_str)
for livro in dados:
    titulo = livro["titulo"]
    autor = livro["autor"]
    print(f"Nome: {titulo}\nAutor: {autor}\n")