import os
from src.infrastructure.database_manager import DatabaseManager
from src.domain.categoria import Categoria

def testar_persistência_real():
    print("\n🔍 Iniciando Teste de Persistência Profissional...")
    
    # Garantir que a pasta data existe (prevenção de erros)
    os.makedirs("src/data", exist_ok=True)
    
    # 1. Instanciar o gerente do banco
    db = DatabaseManager()
    
    # 2. CRIAR O OBJETO CATEGORIA (O que faltou no meu exemplo anterior!)
    # Aqui estamos usando a sua classe Categoria
    categoria_para_salvar = Categoria(nome="Viagens", cor="#0000FF")
    
    print(f"🛠️ Criado objeto: {categoria_para_salvar.nome} (Cor: {categoria_para_salvar.cor})")
    
    # 3. Salvar o objeto
    db.salvar_categoria(categoria_para_salvar)
    print(f"✅ Objeto enviado para o método salvar_categoria.")
    
    # 4. Simular fechamento total do sistema
    del db 
    print("🔌 Conexão encerrada. Simulando reinicialização do sistema...")

    # 5. Criar uma NOVA instância e validar se o dado "sobreviveu" no arquivo .db
    novo_db = DatabaseManager()
    conn = novo_db.conectar()
    cursor = conn.cursor()
    
    cursor.execute("SELECT nome, cor FROM categorias WHERE nome = ?", (categoria_para_salvar.nome,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        nome_db, cor_db = resultado
        print(f"\n🏆 VITÓRIA! O banco retornou: Nome: {nome_db} | Cor: {cor_db}")
        print("A persistência está 100% funcional.")
    else:
        print("\n❌ ERRO: O dado evaporou. Verifique o caminho da pasta 'src/data'.")

if __name__ == "__main__":
    testar_persistência_real()