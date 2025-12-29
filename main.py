from src.infrastructure.database_manager import DatabaseManager
from src.services.categoria_service import CategoriaService

def main():
    db = DatabaseManager()
    cat_service = CategoriaService(db)

    while True:
        print("\n=== ORGANIZADOR DE DESPESAS ===")
        print("1. Cadastrar Nova Categoria")
        print("2. Listar Categorias")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            print("Saindo... Até logo!")
            break
            
        elif opcao == "1":
            nome = input("Nome da Categoria: ")
            cor = input("Cor (Deixe vazio para padrão): ")
            
            sucesso, mensagem = cat_service.cadastrar_categoria(nome, cor)
            print(f"\n>>> {mensagem}")
        elif opcao == "2":
            lista = cat_service.listar_todas_categorias()
            if not lista:
                print("\n⚠️ Nenhuma categoria cadastrada ainda.")
            else:
                print("\n--- LISTA DE CATEGORIAS ---")
                for categoria in lista:
                    print(f"📌 {categoria.nome} (Cor: {categoria.cor})")


        else:
            print("\n❌ Opção inválida!")

if __name__ == "__main__":
    main()