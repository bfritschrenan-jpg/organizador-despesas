import sqlite3
from src.domain.categoria import Categoria


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