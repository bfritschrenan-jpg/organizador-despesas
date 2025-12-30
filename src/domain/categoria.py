class Categoria:
    def __init__(self, 
                 nome: str, 
                 id: int = None,
                 cor:str = "#808080"):
        self.nome = nome.strip().capitalize()
        self.id = id
        self.cor = cor
        
    def __str__(self):
        return f"[ID: {self.id}] {self.nome} ({self.cor})"