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