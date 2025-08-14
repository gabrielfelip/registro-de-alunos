# main.py
import sqlite3

class SistemaDeRegistro:
    """
    Classe responsável exclusivamente pela comunicação com o banco de dados 'estudantes.db'.
    Não contém nenhum código de interface gráfica.
    """
    def __init__(self, db_name='estudantes.db'):
        """Inicializa a conexão com o banco de dados e cria a tabela se não existir."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Cria a tabela 'estudantes' se ela ainda não existir."""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS estudantes(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                tel TEXT NOT NULL,
                sexo TEXT NOT NULL,
                data_nascimento TEXT NOT NULL,
                endereco TEXT NOT NULL,
                curso TEXT NOT NULL,
                picture TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def register_student(self, student_data):
        """
        Insere um novo estudante no banco de dados.
        :param student_data: Uma tupla ou lista com os dados do estudante, sem o ID.
        """
        query = "INSERT INTO estudantes(nome, email, tel, sexo, data_nascimento, endereco, curso, picture) VALUES(?, ?, ?, ?, ?, ?, ?, ?)"
        self.cursor.execute(query, student_data)
        self.conn.commit()

    def view_all_students(self):
        """Retorna uma lista de todos os estudantes no banco de dados."""
        self.cursor.execute("SELECT id, nome, email, tel, sexo, data_nascimento, endereco, curso FROM estudantes")
        return self.cursor.fetchall()

    def search_student(self, student_id):
        """
        Busca um estudante pelo seu ID.
        :param student_id: O ID do estudante a ser procurado.
        :return: Uma tupla com os dados completos do estudante ou None se não for encontrado.
        """
        self.cursor.execute("SELECT * FROM estudantes WHERE id=?", (student_id,))
        return self.cursor.fetchone()

    def update_student(self, student_data):
        """
        Atualiza os dados de um estudante.
        :param student_data: Uma tupla ou lista com os novos dados, ONDE O ID É O ÚLTIMO ELEMENTO.
        """
        # A ordem dos '?' deve corresponder à ordem dos dados em student_data
        query = "UPDATE estudantes SET nome=?, email=?, tel=?, sexo=?, data_nascimento=?, endereco=?, curso=?, picture=? WHERE id=?"
        self.cursor.execute(query, student_data)
        self.conn.commit()

    def delete_student(self, student_id):
        """
        Deleta um estudante do banco de dados pelo seu ID.
        :param student_id: O ID do estudante a ser deletado.
        """
        self.cursor.execute("DELETE FROM estudantes WHERE id=?", (student_id,))
        self.conn.commit()
    
    def close_connection(self):
        """Fecha a conexão com o banco de dados de forma segura."""
        if self.conn:
            self.conn.close()
            print("Conexão com o banco de dados fechada.")