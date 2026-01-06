from src.infrastructure.database_manager import DatabaseManager
from src.services.categoria_service import CategoriaService
from src.services.despesa_service import DespesaService
from datetime import datetime, date

# --- FUNÇÕES DE APOIO  CATEGORIAS (HELPERS) ---

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
    sucesso, mensagem, categoria_obj = service.cadastrar_categoria(nome, cor)
    print(f"\n>>> {mensagem}")
    return sucesso, categoria_obj

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

# --- FUNÇÕES DE APOIO DESPESA ---

def fluxo_cadastrar_despesa(service):

    descricao = while_true("Descrição")
    valor = while_true("Valor", tipo=float, validacao=lambda valor_inteiro: valor_inteiro > 0)
    data_vencimento = while_true("Data de vencimento (ano-mês-dia)", validacao=verifica_data)
    data_venc_objeto = datetime.strptime(data_vencimento, "%Y-%m-%d").date()
    data_atual = date.today()
    status = while_true("digite 1 para paga e 2 para pendente", opcoes=["1", "2"])
    if status == "1":
        status = "pago"
    else: 
        status = "pendente"
    if status == "pendente" and data_venc_objeto < data_atual:
        status = "atrasada"

    tipo = while_true("Digite 1 para despesa fixa e 2 para unica e 3 para parcelada", opcoes=["1", "2", "3"])


    if tipo == "3":
        tipo = "parcelada"
        total_parcelas = while_true("Digite o total de parcelas", tipo=int, validacao=lambda valor_inteiro: valor_inteiro > 0)
    elif tipo == "2":
        tipo = "unica"
        total_parcelas = 0
    else: 
        tipo = "fixa" 
        total_parcelas = 0
      

    lista = service_db().listar_todas_categorias()
    lista_id = []
    
    if not lista:
        print("⚠️ Nenhuma categoria cadastrada.")
        categoria_id = while_true("Degite 1 para cadastar uma nova categoria ou 2 para dexar sem categoria", opcoes=["1", "2"])
        if categoria_id == "1":
            nova_categoria, nova_categoria_id = fluxo_cadastrar_categoria(service_db())
            while nova_categoria == False:
                fluxo_cadastrar_categoria(service_db())
            categoria_id = nova_categoria_id.id
        else:
            categoria_id = None
    else:
        for categoria in lista:
            lista_id.append(categoria.id)
        
        fluxo_listar_categorias(service_db())
        categoria_id = while_true("Digite o ID da categoria ou tecle ENTER para dexar sem categoria", tipo=int, opcoes=lista_id, campo="categoria")
        if categoria_id is not None:
            categoria_obj = next((obj for obj in lista if obj.id == categoria_id))
            categoria = categoria_obj
        else: 
            categoria = categoria_id
            
    parcela_atual = None

    if total_parcelas > 0:
        for i in range(1, total_parcelas + 1):
            descricao = f"{descricao} - {i}/{total_parcelas}"
            parcela_atual = i
            sucesso, mensagem = service.cadastrar_despesa(descricao, 
                          valor, 
                          data_vencimento,
                          status, 
                          tipo,
                          total_parcelas, 
                          parcela_atual, 
                          categoria)
    else:
        sucesso, mensagem = service.cadastrar_despesa(descricao, 
                          valor, 
                          data_vencimento,
                          status, 
                          tipo,
                          total_parcelas, 
                          parcela_atual, 
                          categoria)

    print(f"\n>>> ✅ Despesa cadastrada com sucesso!")

def fluxo_listar_despesas(service):
    print("\n--- LISTA DE DESPESAS ---")
    lista = service.listar_despesas()
    if not lista:
        print("⚠️ Nenhuma despesa cadastrada cadastrada.")
        return
    for despesa in lista:
        print(f"\n📌 [ID: {despesa.id}] {despesa.descricao} (Valor: {despesa.valor}) (status: {despesa.status}) (Categoria: {despesa.nome_categoria})")

def fluxo_remover_despesa(service):
    fluxo_listar_despesas(service)
    id_despesa = while_true("Digite o ID da despesa a remover:\n>>> ", tipo=int)
    sucesso, mensagem= service.remover_despesa(id_despesa)
    print(mensagem)

def fluxo_atualizar_despesa(service):
 pass
    
# --- FUNÇÕES AUXILIARES ---

def verifica_data(data_texto):
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
def while_true(texto, tipo=str, validacao=None, opcoes=None, campo=None):
    while True:
        try:
            if campo == "categoria":
                resposta = input(f"{texto}:\n>>> ").strip()
                if not resposta:
                    resposta = None
                    return resposta

            if validacao == verifica_data:
                    print("\n📅 (Dica: O formato deve ser AAAA-MM-DD, ex: 2025-12-31)\n")
            
            resposta = input(f"{texto}:\n>>> ").strip()
            resposta = tipo(resposta)

            if opcoes is not None:
                if resposta not in opcoes:
                    raise Exception(f"Opção inválida!")

            if validacao is not None:              

                if not validacao(resposta):                    
                    if validacao == verifica_data:
                        raise Exception("Data inválida ou inexistente!")
                    else:
                        raise ValueError("Validação falhou")

            # print(f"{texto}: {resposta}")
            return resposta
        except ValueError:
            print("\n❌ Erro: Digite apenas números! (Use ponto em vez de vírgula, ex: 25.50)\n")

        except Exception as e:
            print(f"\nerro: {e} - Tente Novamente\n")

def despesa_service_db():
    db = DatabaseManager()
    categoria_service = CategoriaService(db)
    return DespesaService(db, categoria_service)

def service_db():
    db = DatabaseManager()
    return CategoriaService(db)

# --- FUNÇÃO PRINCIPAL ---

def main():

    while True:
        print("\n=== ORGANIZADOR DE DESPESAS ===")
        print("1. Listar Categorias")
        print("2. Cadastrar Categoria")
        print("3. Editar Categoria")
        print("4. Excluir Categoria")
        print("5. Cadastrar Despesa")
        print("6. Listar Despesas")
        print("7. Remover Despesa")
        print("8. Editar Despesa")
        print("\n\n0. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "0":
            print("Saindo... Até logo!")
            break
        elif opcao == "1":
            fluxo_listar_categorias(service_db())
        elif opcao == "2":
            fluxo_cadastrar_categoria(service_db())
        elif opcao == "3":
            fluxo_editar_categoria(service_db())    
        elif opcao == "4":
            fluxo_remover_categoria(service_db())
        elif opcao == "5":
            fluxo_cadastrar_despesa(despesa_service_db())
        elif opcao == "6":
            fluxo_listar_despesas(despesa_service_db())
        elif opcao == "7":
            fluxo_remover_despesa(despesa_service_db())
        elif opcao == "8":
            fluxo_atualizar_despesa(despesa_service_db())
        else:
            print("\n❌ Opção inválida!")

if __name__ == "__main__":
    main()