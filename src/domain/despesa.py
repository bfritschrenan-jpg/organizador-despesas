from .categoria import Categoria

class Despesa:
    def __init__(self, 
                 descricao: str, 
                 valor: float, 
                 categoria: Categoria, 
                 data_vencimento: str, 
                 tipo: str = "UNICA", 
                 status: str = "PENDENTE", 
                 total_parcelas: int = None, 
                 parcela_atual: int = None):

        self.descricao = descricao
        self.valor = valor
        self.categoria = categoria
        self.data_vencimento = data_vencimento
        self.status = status
        self.tipo = tipo.upper()
        self.total_parcelas = total_parcelas 
        self.parcela_atual = parcela_atual
        