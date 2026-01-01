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
                          categoria_id ):
        
        descricao = descricao.strip()

        if not descricao:
            return False, "❌ Erro: A despesa precisa de uma descrição!"
        
        if valor <= 0:
            return False, "❌ Erro: O valor da despesa deve ser maior que zero!"
        
        try:
            data_venc_objeto = datetime.strptime(data_vencimento, "%Y-%m-%d").date()
            data_atual = date.today()
            if status.lower() == "pendente" and data_venc_objeto < data_atual:
                status = "ATRASADA"
            else:
                status = status.upper() 
        except ValueError:
            return False, "❌ Erro: Formato de data inválido! Use AAAA-MM-DD."
        
        list_cat = self.categoria_service.listar_todas_categorias()

        categoria_encontrada = None

        if not list_cat:
            return False, "❌ Erro: Nenhuma categoria cadastrada no sistema."
        
        for categoria in list_cat:
            if categoria.id == categoria_id:
                categoria_encontrada = categoria
                break
        if categoria_encontrada is None:
            return False, f"❌ Erro: A categoria com ID {categoria_id} não existe."
        
        nova_despesa = Despesa(descricao, 
                          valor, 
                          data_vencimento,
                          status, 
                          tipo,
                          total_parcelas, 
                          parcela_atual, 
                          categoria_encontrada )
        
        self.db.salvar_despesa(nova_despesa)