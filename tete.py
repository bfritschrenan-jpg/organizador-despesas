from datetime import datetime


def verifica_data(data_texto):
    try:
        datetime.strptime(data_texto, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def while_true(texto, tipo=str, validacao=None, opcoes=None):
    while True:
        try:
           
            if validacao == verifica_data:
                    print("\n📅 (Dica: O formato deve ser AAAA-MM-DD, ex: 2025-12-31)\n")

            resposta = tipo(input(f"{texto}:\n>>> "))

            if opcoes is not None:
                if resposta not in opcoes:
                    raise Exception(f"Opção inválida!")

            if validacao is not None:              

                if not validacao(resposta):                    
                    if validacao == verifica_data:
                        raise Exception("Data inválida ou inexistente!")
                    else:
                        raise ValueError("Validação falhou")
                
            print(f"{texto}: {resposta}")
            return
        except ValueError:
            print("\n❌ Erro: Digite apenas números! (Use ponto em vez de vírgula, ex: 25.50)\n")

        except Exception as e:
            print(f"\nerro: {e} - Tente Novamente\n")





descricao = while_true("Descrição")
valor = while_true("Valor", tipo=float, validacao=lambda valor_inteiro: valor_inteiro > 0)
data_vencimento = while_true("Data de vencimento (ano-mês-dia)", validacao=verifica_data)
status = while_true("digite 1 para paga e 2 para pendente", opcoes=["1", "2"])
tipo = while_true("Digite 1 para despesa fixa e 2 para unica e 3 para parcelada", opcoes=["1", "2", "3"])
total_parcelas = while_true("Digite o total de parcelas", tipo=int, validacao=lambda valor_inteiro: valor_inteiro > 0)
