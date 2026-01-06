from src.infrastructure.database_manager import DatabaseManager
from src.services.categoria_service import CategoriaService
from src.domain.despesa import Despesa
from datetime import datetime, date
class DespesaService:
    def __init__(self, db_manager, categoria_service):
        self.db = db_manager
        self.categoria_service = categoria_service

    def cadastrar_despesa(self, 
                          descricao, 
                          valor, 
                          data_vencimento,
                          status, 
                          tipo,
                          total_parcelas, 
                          parcela_atual, 
                          categoria_obj ):
        
        descricao = descricao.strip()
        
        nova_despesa = Despesa(descricao, 
                          valor, 
                          data_vencimento,
                          categoria_obj,
                          status, 
                          tipo,
                          total_parcelas, 
                          parcela_atual, 
                          )
        
        self.db.salvar_despesa(nova_despesa)

        return True, "✅ Despesa cadastrada com sucesso!"
    
    def listar_despesas(self):
        despesas = self.db.listar_despesas()
        despesas_objetos = []
        for despesa in despesas:
            print(despesa)
            obj = Despesa(despesa[1],
                          despesa[2],
                          despesa[3],
                          despesa[4],
                          despesa[5],
                          despesa[6],
                          despesa[7],
                          despesa[8],
                          despesa[9])
            
            obj.id = despesa[0]
            despesas_objetos.append(obj)
        print(despesas_objetos)
        return despesas_objetos
    
    def remover_despesa(self, id_despesa):
        sucesso = self.db.remover_despesa(id_despesa)
        if sucesso:
            return True, "Despesa removida com sucesso!"
        return False, "Erro: Despesa não encontrada."