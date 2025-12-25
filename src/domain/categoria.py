class Categoria:
    def __init__(self, 
                 nome: str, 
                 cor:str = "#808080"):
        self.nome = nome.strip().capitalize()
        self.cor = cor
        
    def __str__(self):
        return self.nome