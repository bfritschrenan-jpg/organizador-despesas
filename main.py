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

def fluxo_editar_categoria(service):
    print("\n--- EDITAR CATEGORIA ---")
    lista = service.listar_todas_categorias()
    if not lista:
        print("⚠️ Nenhuma categoria disponível para editar.")
        return
    for categoria in lista:
        print(f"[{categoria.id}] {categoria.nome}")
    try:
        id_selecionado = int(input("\nDigite o ID da categoria que deseja editar: "))
        categoria_alvo = None

        for categoria in lista:
            if categoria.id == id_selecionado:
                categoria_alvo = categoria
        if categoria_alvo is not None:
            print(f"\n⚠️  AVISO: Você está prestes a editar a categoria '{categoria_alvo.nome}'.")
            confirmacao = input("Tem certeza absoluta? (S/N): ").upper().strip()
            if confirmacao == "S":
                novo_nome = input("Novo nome (ou aperte Enter para manter): ")
                if novo_nome == "":  # Se ele apenas apertou Enter
                    novo_nome = categoria_alvo.nome
                nova_cor = input("Nova cor (ou aperte Enter para manter): ")
                if nova_cor == "":  # Se ele apenas apertou Enter
                    nova_cor = categoria_alvo.cor
                sucesso, mensagem = service.atualizar_categoria(id_selecionado, novo_nome, nova_cor)
                print(f"\n>>> {mensagem}")
            else: 
                print("\nOperação cancelada.")
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
        elif opcao == "3":
            fluxo_editar_categoria(cat_service)    
        elif opcao == "4":
            fluxo_remover_categoria(cat_service)    
        else:
            print("\n❌ Opção inválida!")

if __name__ == "__main__":
    main()