from src.infrastructure.database_manager import DatabaseManager
from src.domain.categoria import Categoria

def testar_banco():
    db = DatabaseManager()
    
    # 1. Criamos um objeto Categoria (na memória RAM)
    nova_cat = Categoria(nome="Lazer", cor="#1ABC9C")
    print(f"Objeto criado: {nova_cat.nome} ({nova_cat.cor})")

    # 2. Mandamos o gerente salvar no arquivo (Disco Rígido)
    novo_id = db.salvar_categoria(nova_cat)
    
    if novo_id:
        print(f"✅ SUCESSO: Categoria salva com o ID: {novo_id}")
    else:
        print("❌ ERRO: Não foi possível salvar a categoria.")

if __name__ == "__main__":
    testar_banco()