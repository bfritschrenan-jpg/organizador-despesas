from .categoria import Categoria
from typing import Optional
class Despesa:
    def __init__(self, 
                 descricao: str, 
                 valor: float,
                 data_vencimento: str,
                 categoria_obj: Optional[Categoria] = None,
                 status: str = "PENDENTE",
                 tipo: str = "UNICA", 
                 total_parcelas: int = None, 
                 parcela_atual: int = None,
                 nome_categoria = None ):
        
        self.descricao = descricao
        self.valor = valor
        self.categoria = categoria_obj
        self.data_vencimento = data_vencimento
        self.status = status
        self.tipo = tipo
        self.total_parcelas = total_parcelas 
        self.parcela_atual = parcela_atual
        self.nome_categoria = nome_categoria