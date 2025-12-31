import os
from src.infrastructure.database_manager import DatabaseManager
from src.services.categoria_service import CategoriaService

# --- FUNÇÕES DE APOIO (HELPERS) ---

def fluxo_listar_categorias(service):
    print("\n--- LISTA DE CATEGORIAS ---")
    lista = service.listar_todas_categorias()
    if not lista:
        print("⚠️ Nenhuma categoria cadastrada.")
        return
    for cat in lista:
        print(f"📌 [ID: {cat.id}] {cat.nome} (Cor: {cat.cor})")

def fluxo_cadastrar_categoria(service):
    print("\n--- CADASTRAR NOVA CATEGORIA ---")
    nome = input("Nome da Categoria: ")
    cor = input("Cor (Deixe vazio para padrão): ")
    sucesso, mensagem = service.cadastrar_categoria(nome, cor)
    print(f"\n>>> {mensagem}")

def fluxo_remover_categoria(service):
    print("\n--- REMOVER CATEGORIA ---")
    lista = service.listar_todas_categorias()

    if not lista:
        print("⚠️ Nenhuma categoria disponível para remover.")
        return
    
    for categoria in lista:
        print(f"[{categoria.id}] {categoria.nome}")

    try:
        id_selecionado = int(input("\nDigite o ID da categoria que deseja remover: "))
        categoria_alvo = None

        for categoria in lista:
            if categoria.id == id_selecionado:
                categoria_alvo = categoria

        if categoria_alvo is not None:
            print(f"\n⚠️  AVISO: Você está prestes a apagar a categoria '{categoria_alvo.nome}'.")
            confirmacao = input("Tem certeza absoluta? (S/N): ").upper().strip()

            if confirmacao == "S":
                sucesso, mensagem = service.remover_categoria(id_selecionado)
                print(f"\n>>> {mensagem}")
            else: 
                print("\nOperação cancelada.")

        else:
            print(f"\n❌ Erro: Não encontrei nenhuma categoria com o ID {id_selecionado}.")

    except ValueError:
           print("\n❌ Erro: Você precisa digitar um número válido para o ID!")

# --- FUNÇÃO PRINCIPAL ---

def main():
    db = DatabaseManager()
    cat_service = CategoriaService(db)

    while True:
        print("\n=== ORGANIZADOR DE DESPESAS ===")
        print("1. Listar Categorias")
        print("2. Cadastrar Categoria")
        print("3. Editar Categoria")
        print("4. Excluir Categoria")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            print("Saindo... Até logo!")
            break
        elif opcao == "1":
            fluxo_listar_categorias(cat_service)
        elif opcao == "2":
            fluxo_cadastrar_categoria(cat_service)
        elif opcao == "4":
            fluxo_remover_categoria(cat_service)    
        # Próximos passos: Opção 3 e 4
        else:
            print("\n❌ Opção inválida!")

if __name__ == "__main__":
    main()