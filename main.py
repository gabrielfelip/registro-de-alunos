import sqlite3
from tkinter import messagebox

from click import confirm


class SistemaDeRegistro:
    def __init__(self):
        self.conn = sqlite3.connect('estudantes.db')
        self.c = self.conn.cursor()
        self.create_table()
    def create_table(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS estudantes(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       nome TEXT NOT NULL,
                       email TEXT NOT NULL,
                       tel TEXT NOT NULL,
                       sexo TEXT NOT NULL,
                       data_nascimento TEXT NOT NULL,
                       endereco TEXT NOT NULL,
                       curso TEXT NOT NULL,
                       picture TEXT NOT NULL)''')
    def register_student(self, estudantes):
        self.c.execute("INSERT INTO estudantes(nome, email, tel, sexo, data_nascimento, endereco, curso, picture) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", estudantes)
        self.conn.commit()

        #mensagem de sucesso
        messagebox.showinfo("Sucesso", "Estudante registrado com sucesso!")

    def view_all_students(self):
        self.c.execute("SELECT * FROM estudantes")
        dados = self.c.fetchall()
        
        for i in dados:
            print(f'ID: {i[0]} | Nome: {i[1]} | email: {i[2]} | Telefone: {i[3]} | Sexo: {i[4]} | Data de Nascimento: {i[5]} | Endereço: {i[6]} | Curso: {i[7]} | Foto: {i[8]}')
    
    def search_student(self, id):
        self.c.execute("SELECT * FROM estudantes WHERE id=?", (id,))
        dados = self.c.fetchone()
        print(f'ID: {dados[0]} | Nome: {dados[1]} | email: {dados[2]} | Telefone: {dados[3]} | Sexo: {dados[4]} | Data de Nascimento: {dados[5]} | Endereço: {dados[6]} | Curso: {dados[7]} | Foto: {dados[8]}')

    def update_student(self, novo_valor):
        query = "UPDATE estudantes SET nome=?, email=?, tel=?, sexo=?, data_nascimento=?, endereco=?, curso=?, picture=? WHERE id=?"
        self.c.execute(query, novo_valor)
        self.conn.commit()
        messagebox.showinfo("Sucesso", "Estudante atualizado com sucesso!")

    def delete_student(self, id):
       confirm = messagebox.askyesno("Confirmar exclusão", "Tem certeza que deseja excluir este estudante?")
       if confirm:
           self.c.execute("DELETE FROM estudantes WHERE id=?", (id,))
           self.conn.commit()
           messagebox.showinfo("Sucesso", "Estudante excluído com sucesso!")

#criando instancia do sistema de registro
sistema_de_registro = SistemaDeRegistro()

#informações

#estudante = ('Sofia', 'sofia@example.com', '123456', 'Feminino', '01/01/2002', 'Brasil, RJ', 'Letras', 'foto.jpg')
#sistema_de_registro.register_student(estudante)

#ver estudantes
#todos_alunos = sistema_de_registro.view_all_students()

#procurar aluno
#aluno = sistema_de_registro.search_student(2)

#atualizar aluno
#estudante = sistema_de_registro.update_student(('Sofia Silva', 'sofia.silva@example.com', '987654', 'Feminino', '02/02/2002', 'Espanha, Madrid', 'Letras', 'nova_foto.jpg', 2))
#aluno = sistema_de_registro.update_student(estudante)  

sistema_de_registro.delete_student(2)

#ver estudantes
#todos_alunos = sistema_de_registro.view_all_students()