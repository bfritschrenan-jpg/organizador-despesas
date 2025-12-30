from src.infrastructure.database_manager import DatabaseManager
from src.domain.categoria import Categoria
class CategoriaService:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def cadastrar_categoria(self,nome,cor):

        nome_categoria = nome.strip()

        if not nome_categoria:
            return False, "Erro: A categoria precisa de um nome!"
        
        nome_existe = self.db.buscar_categoria_por_nome(nome_categoria)

        if nome_existe is not None:
            return False, f"Erro: A categoria '{nome_categoria}' já existe!"
        
        if cor and cor.strip():
            nova_categoria = Categoria(nome=nome_categoria, cor=cor)
        else:
            nova_categoria = Categoria(nome=nome_categoria)
            
        self.db.salvar_categoria(nova_categoria)

        return True, f"Sucesso: Categoria '{nome_categoria}' cadastrada!"
    
    def listar_todas_categorias(self):
        categorias = self.db.listar_categorias()
        categorias_obj = []
        for categoria in categorias:
            obj = Categoria(categoria[1], categoria[0], categoria[2])
            categorias_obj.append(obj)
        return categorias_obj
    
    def remover_categoria(self, id_categoria):
        sucesso = self.db.remover_categoria(id_categoria)
        if sucesso:
            return True, "Categoria removida com sucesso!"
        return False, "Erro: Categoria não encontrada."
    
    def atualizar_categoria(self, id_categoria, novo_nome, nova_cor):
        if not novo_nome:
            return False, "Erro: A categoria precisa de um nome!"
        
        categorias = self.listar_todas_categorias()

        if any(categoria.nome == novo_nome and categoria.id != id_categoria for categoria in categorias):
            return False, f"Erro: Já existe outra categoria chamada '{novo_nome}'!"
        
        sucesso = self.db.atualizar_categoria(id_categoria, novo_nome, nova_cor)
        if sucesso:
            return True, "Categoria atualizada com sucesso!"
        return False, "Erro ao atualizar: Categoria não encontrada."