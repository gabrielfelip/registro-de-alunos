# tela.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog as fd, TclError
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import date
from main import SistemaDeRegistro

class StudentRegistrationApp:
    def __init__(self, root):
        self.root = root
        self.backend = SistemaDeRegistro()
        
        self.root.title("Sistema de Registro de Alunos")
        self.root.geometry("810x560") # Altura ajustada para a barra de status
        self.root.resizable(width=False, height=False)
        
        self.colors = {
            "white": "#feffff", "black": "#2e2d2b", "dark_text": "#403d3d",
            "blue": "#146C94", "status_bg": "#e9edf5"
        }
        self.root.configure(background=self.colors['white'])
        
        style = ttk.Style(self.root)
        style.theme_use("clam")
        
        self.student_photo_path = "logo.png"
        self.status_after_id = None

        # --- CORREÇÃO PRINCIPAL DO LAYOUT ---
        # Configura as colunas da janela principal para que o frame de detalhes (coluna 1) se expanda
        self.root.columnconfigure(0, weight=0) # Coluna dos botões não expande
        self.root.columnconfigure(1, weight=1) # Coluna do formulário expande para preencher o espaço

        self._create_frames()
        self._create_widgets()
        self.update_student_list()
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_frames(self):
        """Cria os frames principais. A estrutura é a mesma, mas agora respeitará a configuração da janela."""
        self.header_frame = tk.Frame(self.root, height=52, bg=self.colors['blue'])
        self.header_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.controls_frame = tk.Frame(self.root, width=170, bg=self.colors['white'], relief=tk.RAISED)
        self.controls_frame.grid(row=1, column=0, padx=0, pady=1, sticky="ns")

        self.details_frame = tk.Frame(self.root, bg=self.colors['white'], relief=tk.SOLID, bd=1)
        self.details_frame.grid(row=1, column=1, padx=10, pady=1, sticky="nsew")

        self.table_frame = tk.Frame(self.root, bg=self.colors['white'])
        self.table_frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="nsew")
        self.root.grid_rowconfigure(2, weight=1)

        self.status_frame = tk.Frame(self.root, bg=self.colors['status_bg'], relief=tk.SUNKEN, bd=1)
        self.status_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

    def _create_widgets(self):
        """Cria todos os widgets da aplicação."""
        self._create_header_widgets()
        self._create_controls_widgets()
        self._create_details_widgets()
        self._create_table_widgets()
        self._create_status_bar_widgets()

    def _create_header_widgets(self):
        self.logo_img = Image.open('logo.png').resize((50, 50))
        self.logo_photo = ImageTk.PhotoImage(self.logo_img)
        app_logo = tk.Label(self.header_frame, image=self.logo_photo, text="Sistema de Registro de Alunos",
                            padx=20, compound=tk.LEFT, anchor=tk.NW, font=("Verdana", 14, "bold"),
                            fg=self.colors['white'], bg=self.colors['blue'])
        app_logo.place(x=5, y=0, relheight=1, width=850)

    def _create_controls_widgets(self):
        search_frame = tk.Frame(self.controls_frame, bg=self.colors['white'])
        search_frame.grid(row=0, column=0, pady=10, padx=10)
        tk.Label(search_frame, text="Procurar aluno [ID]", anchor=tk.NW, font=('Ivy 10'), bg=self.colors['white']).grid(row=0, column=0, columnspan=2, sticky='w')
        self.search_entry = tk.Entry(search_frame, width=7, justify='center', font=('Ivy 10'), relief='solid')
        self.search_entry.grid(row=1, column=0, pady=5, padx=(0,5))
        tk.Button(search_frame, command=self.search_student, text='Procurar', width=10, font=('Ivy 7 bold')).grid(row=1, column=1, pady=5)
        
        self.button_images = {}
        actions = {'add': (' Adicionar aluno ', self.add_student, 'add.png'), 'update': (' Atualizar aluno ', self.update_student, 'update.png'), 'delete': (' Deletar aluno ', self.delete_student, 'delete.png')}
        row_num = 1
        for key, (text, command, img_file) in actions.items():
            img = Image.open(img_file).resize((25, 25))
            self.button_images[key] = ImageTk.PhotoImage(img)
            tk.Button(self.controls_frame, command=command, image=self.button_images[key], relief=tk.GROOVE, text=text, width=130, compound=tk.LEFT, font=('Ivy 11')).grid(row=row_num, column=0, pady=5, padx=10, sticky='w')
            row_num += 1

    def _create_details_widgets(self):
        """ Widgets de detalhes usando .place() exatamente como no seu layout original."""
        tk.Label(self.details_frame, text="Nome *", font=('Ivy 10'), bg=self.colors['white']).place(x=4, y=10)
        self.name_entry = tk.Entry(self.details_frame, width=30, relief='solid')
        self.name_entry.place(x=7, y=40)
        tk.Label(self.details_frame, text="E-mail *", font=('Ivy 10'), bg=self.colors['white']).place(x=4, y=70)
        self.email_entry = tk.Entry(self.details_frame, width=30, relief='solid')
        self.email_entry.place(x=7, y=100)
        tk.Label(self.details_frame, text="Telefone *", font=('Ivy 10'), bg=self.colors['white']).place(x=4, y=130)
        self.tel_entry = tk.Entry(self.details_frame, width=15, relief='solid')
        self.tel_entry.place(x=7, y=160)
        self.tel_entry.bind('<KeyRelease>', self._format_phone)

        tk.Label(self.details_frame, text="Sexo *", font=('Ivy 10'), bg=self.colors['white']).place(x=127, y=130)
        self.gender_combo = ttk.Combobox(self.details_frame, width=7, font=('Ivy 8 bold'), justify='center', values=('M', 'F', 'Outro'))
        self.gender_combo.place(x=130, y=160)
        tk.Label(self.details_frame, text="Data de Nascimento *", font=('Ivy 10'), bg=self.colors['white']).place(x=220, y=10)
        self.birth_date_entry = DateEntry(self.details_frame, width=18, background='darkblue', foreground='white', date_pattern='dd/MM/yyyy')
        self.birth_date_entry.place(x=224, y=40)
        tk.Label(self.details_frame, text="Endereço *", font=('Ivy 10'), bg=self.colors['white']).place(x=220, y=70)
        self.address_entry = tk.Entry(self.details_frame, width=22, relief='solid')
        self.address_entry.place(x=224, y=100)
        cursos = ['Engenharia', 'Medicina', 'Direito', 'Letras', 'Ciência da Computação', 'Análise de Dados']
        tk.Label(self.details_frame, text="Curso *", font=('Ivy 10'), bg=self.colors['white']).place(x=220, y=130)
        self.course_combo = ttk.Combobox(self.details_frame, width=19, font=('Ivy 8 bold'), values=cursos)
        self.course_combo.place(x=224, y=160)

        # A coordenada X da foto foi ajustada para um valor mais central no frame expandido
        self.photo_label = tk.Label(self.details_frame, bg=self.colors['white'])
        self.photo_label.place(x=450, y=10)
        self._set_student_image(self.student_photo_path)
        self.upload_button = tk.Button(self.details_frame, command=self.choose_image, text='Carregar Foto'.upper(), width=20, font=('Ivy 7 bold'))
        self.upload_button.place(x=450, y=160)

    def _create_table_widgets(self):
        search_name_frame = tk.Frame(self.table_frame, bg=self.colors['white'])
        search_name_frame.pack(fill='x', padx=5, pady=5)
        tk.Label(search_name_frame, text="Buscar por nome:", font=('Ivy 10 bold'), bg=self.colors['white']).pack(side='left', padx=(0,10))
        self.name_search_entry = tk.Entry(search_name_frame, width=40, relief='solid')
        self.name_search_entry.pack(side='left', fill='x', expand=True)
        self.name_search_entry.bind('<KeyRelease>', self._search_by_name)
        tree_container = tk.Frame(self.table_frame)
        tree_container.pack(fill='both', expand=True)
        list_header = ['ID', 'Nome', 'Email', 'Telefone', 'Sexo', 'Nascimento', 'Endereço', 'Curso']
        self.tree = ttk.Treeview(tree_container, columns=list_header, show="headings")
        vsb = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(side='left', fill='both', expand=True)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')
        self.tree.bind('<ButtonRelease-1>', self._on_tree_select)
        col_widths = {'ID': 40, 'Nome': 150, 'Email': 150, 'Telefone': 100, 'Sexo': 50, 'Nascimento': 90, 'Endereço': 150, 'Curso': 150}
        for col, width in col_widths.items():
            self.tree.heading(col, text=col.title(), anchor=tk.CENTER)
            self.tree.column(col, width=width, anchor='w' if col in ['Nome', 'Email', 'Endereço'] else 'center')

    def _create_status_bar_widgets(self):
        self.status_bar = tk.Label(self.status_frame, text="Pronto", anchor='w', bg=self.colors['status_bg'], fg=self.colors['dark_text'])
        self.status_bar.pack(fill='x', padx=5)

    def _on_tree_select(self, event):
        selection = self.tree.selection()
        if not selection: return
        item_id = self.tree.item(selection[0], 'values')[0]
        self.search_entry.delete(0, tk.END); self.search_entry.insert(0, item_id)
        self.search_student()
        self._update_status(f"Aluno(a) '{self.name_entry.get()}' carregado(a).")

    def _update_status(self, message, duration=4000):
        self.status_bar.config(text=message)
        if self.status_after_id: self.root.after_cancel(self.status_after_id)
        self.status_after_id = self.root.after(duration, lambda: self.status_bar.config(text="Pronto"))
    
    def _search_by_name(self, event=None):
        search_term = self.name_search_entry.get().lower()
        all_students = self.backend.view_all_students()
        if not search_term: self._populate_tree(all_students)
        else:
            filtered_list = [s for s in all_students if search_term in s[1].lower()]
            self._populate_tree(filtered_list)

    # --- FUNÇÃO DA MÁSCARA DE TELEFONE CORRIGIDA ---
    def _format_phone(self, event=None):
        """Formata o campo de telefone para (XX) XXXXX-XXXX ou (XX) XXXX-XXXX."""
        if self._is_formatting_phone:
            return

        self._is_formatting_phone = True

    def _clear_entries(self):
        self.search_entry.delete(0, tk.END); self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END); self.tel_entry.delete(0, tk.END)
        self.gender_combo.set(''); self.birth_date_entry.set_date(date.today())
        self.address_entry.delete(0, tk.END); self.course_combo.set('')
        self._set_student_image('logo.png'); self.upload_button['text'] = 'Carregar Foto'.upper()

    def _get_form_data(self):
        return [self.name_entry.get(), self.email_entry.get(), self.tel_entry.get(), self.gender_combo.get(),
                self.birth_date_entry.get(), self.address_entry.get(), self.course_combo.get(), self.student_photo_path]

    def _populate_form(self, data):
        self._clear_entries()
        self.search_entry.insert(0, data[0]); self.name_entry.insert(0, data[1])
        self.email_entry.insert(0, data[2]); self.tel_entry.insert(0, data[3])
        self.gender_combo.set(data[4]); self.birth_date_entry.set_date(data[5])
        self.address_entry.insert(0, data[6]); self.course_combo.set(data[7])
        self._set_student_image(data[8]); self.upload_button['text'] = 'Alterar Foto'.upper()
        self._format_phone()

    def _set_student_image(self, image_path):
        try:
            self.student_photo_path = image_path
            img = Image.open(image_path).resize((130, 130))
            self.student_photo_image = ImageTk.PhotoImage(img)
            self.photo_label.configure(image=self.student_photo_image)
        except Exception:
            if image_path != 'logo.png': self._set_student_image('logo.png')

    def _populate_tree(self, student_list):
        self.tree.delete(*self.tree.get_children())
        for item in student_list: self.tree.insert('', 'end', values=item)

    def update_student_list(self):
        self._populate_tree(self.backend.view_all_students())

    def add_student(self):
        data = self._get_form_data()
        if any(f == '' for f in data[:-1]):
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")
            return
        self.backend.register_student(data)
        self._update_status(f"Aluno(a) '{data[0]}' registrado(a) com sucesso!")
        self._clear_entries(); self.update_student_list()

    def search_student(self):
        try:
            student_id = int(self.search_entry.get())
            data = self.backend.search_student(student_id)
            if data: self._populate_form(data)
            else:
                messagebox.showerror("Erro", f"Nenhum aluno encontrado com o ID {student_id}.")
                self._clear_entries()
        except (ValueError, TclError): messagebox.showerror("Erro de Formato", "O ID deve ser um número inteiro.")

    def update_student(self):
        try: student_id = int(self.search_entry.get())
        except (ValueError, TclError):
            messagebox.showerror("Erro", "Nenhum aluno selecionado. Busque ou clique em um aluno para atualizar.")
            return
        data = self._get_form_data()
        if any(f == '' for f in data[:-1]):
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")
            return
        self.backend.update_student(data + [student_id])
        self._update_status(f"Dados do aluno(a) '{data[0]}' atualizados com sucesso!")
        self._clear_entries(); self.update_student_list()

    def delete_student(self):
        try: student_id = int(self.search_entry.get())
        except (ValueError, TclError):
            messagebox.showerror("Erro", "Nenhum aluno selecionado. Busque ou clique em um aluno para deletar.")
            return
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja deletar o aluno ID {student_id}?"):
            self.backend.delete_student(student_id)
            self._update_status("Aluno deletado com sucesso.")
            self._clear_entries(); self.update_student_list()

    def choose_image(self):
        fp = fd.askopenfilename(title="Escolha uma foto", filetypes=[("Imagens", "*.jpg;*.jpeg;*.png")])
        if fp: self._set_student_image(fp); self.upload_button['text'] = 'Alterar Foto'

    def _on_closing(self):
        if messagebox.askokcancel("Sair", "Deseja sair da aplicação?"):
            self.backend.close_connection()
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = StudentRegistrationApp(root)
    root.mainloop()