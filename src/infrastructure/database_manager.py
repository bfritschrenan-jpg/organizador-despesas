import sqlite3
from src.domain.categoria import Categoria
from src.domain.despesa import Despesa

class DatabaseManager:
    def __init__(self, db_name="src/data/organizador.db"):
        self.db_name = db_name
        self.criar_tabelas()

    def conectar(self):
        """Cria uma conexão com o banco de dados."""
        return sqlite3.connect(self.db_name)

    def criar_tabelas(self):
        """Cria as tabelas de Categoria e Despesa se elas não existirem."""
        conn = self.conectar()
        cursor = conn.cursor()

        # Tabela de Categorias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorias (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                cor TEXT
            )
        ''')

        # Tabela de Despesas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS despesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                descricao TEXT NOT NULL,
                valor REAL NOT NULL,
                data_vencimento TEXT,
                status TEXT,
                tipo TEXT,
                total_parcelas INTEGER,
                parcela_atual INTEGER,
                categoria_id INTEGER,
                FOREIGN KEY (categoria_id) REFERENCES categorias (id)
            )
        ''')

        conn.commit()
        conn.close()

    def salvar_categoria(self, categoria):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO categorias (nome, cor)  VALUES (?, ?)
        ''',
        (categoria.nome, categoria.cor)
        )
       
       
        conn.commit()
        conn.close()

    def buscar_categoria_por_nome(self, nome):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM categorias WHERE nome = ?
        ''',
        (nome,)
        )
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    
    def listar_categorias(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM categorias
        '''
        )
        categorias = cursor.fetchall()
        conn.close()
        return categorias
    
    def remover_categoria(self, id_categoria):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM categorias WHERE ID = ?
        ''',
        (id_categoria,)
        )

        linhas_afetadas = cursor.rowcount
        conn.commit()
        conn.close()
        return linhas_afetadas > 0
    
    def atualizar_categoria(self, id_categoria, novo_nome, nova_cor):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE categorias SET nome = ?, cor = ? WHERE ID = ?
        ''',
        (novo_nome, nova_cor, id_categoria)
        )

        linhas_afetadas = cursor.rowcount
        conn.commit()
        conn.close()
        return linhas_afetadas > 0
    
    # FUNÇÕES DESPESAS

    def salvar_despesa(self, despesa):
        conn = self.conectar()
        cursor = conn.cursor()
        print(despesa.categoria)
        # O SQL precisa ter a mesma ordem dos valores na tupla abaixo
        cursor.execute('''
            INSERT INTO despesas (
                descricao, valor, data_vencimento, status, 
                tipo, total_parcelas, parcela_atual, categoria_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        (despesa.descricao,
            despesa.valor,
            despesa.data_vencimento,
            despesa.status,
            despesa.tipo,
            despesa.total_parcelas,
            despesa.parcela_atual,
            despesa.categoria.id)
        )
        
        conn.commit()
        conn.close()

    def listar_despesas(self):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT 
                despesas.id, 
                despesas.descricao, 
                despesas.valor, 
                despesas.data_vencimento,
                despesas.categoria_id, 
                despesas.status, 
                despesas.tipo, 
                despesas.total_parcelas, 
                despesas.parcela_atual,
                categorias.nome
            FROM despesas
            INNER JOIN categorias ON despesas.categoria_id = categorias.id 
        ''')

        despesas = cursor.fetchall()
        conn.close()
        return despesas
    
    def remover_despesa(self, id_despesa):
        conn = self.conectar()
        cursor = conn.cursor()

        cursor.execute('''
            DELETE FROM despesas WHERE ID = ?
        ''',
        (id_despesa,)
        )
        linhas_afetadas = cursor.rowcount
        conn.commit()
        conn.close()
        return linhas_afetadas > 0