from customtkinter import *
from tkinter import *
from tkinter import ttk
import sqlite3

janela = CTk()

class Funcs():
    def limpa_tela(self):
        self.entr_codigo.delete(0, END)
        self.entr_nome.delete(0, END)
        self.entr_tel.delete(0, END)
        self.entr_cidade.delete(0, END)
    def conecta_bd(self):
        self.conn = sqlite3.connect("clientes.bd")
        self.cursor = self.conn.cursor(); print("Conectando ao Banco de Dados...")
    def desconecta_bd(self):
        self.conn.close(); print("Banco de Dados desconectado...")
    def monta_tabelas(self):
        self.conecta_bd();
        ### criando tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes (
                cod INTEGER PRIMARY KEY,
                nome_cliente VARCHAR (40) NOT NULL,
                telefone INTEGER (11),
                cidade VARCHAR (20)
            
        );""")
        self.conn.commit(); print("Banco de Dados criado!")
        self.desconecta_bd()
    def variaveis(self):
        self.codigo = self.entr_codigo.get()
        self.nome = self.entr_nome.get()
        self.tel = self.entr_tel.get()
        self.cidade = self.entr_cidade.get()
    def duplo_click(self, event):
        self.limpa_tela()
        self.lista_cli.selection()

        for n in self.lista_cli.selection():
            col1, col2, col3, col4 = self.lista_cli.item(n, 'values')
            self.entr_codigo.insert(END, col1)
            self.entr_nome.insert(END, col2)
            self.entr_tel.insert(END, col3)
            self.entr_cidade.insert(END, col4)


    def add_cliente(self):
        self.variaveis()
        self.conecta_bd()

        self.cursor.execute("""INSERT INTO clientes (nome_cliente, telefone, cidade)
                            VALUES (?, ?, ?)""", (self.nome, self.tel, self.cidade))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela
    def altera_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
                            WHERE cod = ? """, (self.nome, self.tel, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.select_lista()
        self.limpa_tela()

    
    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? ;""", [self.codigo])
        self.conn.commit() 
        self.desconecta_bd()
        self.limpa_tela()
        self.select_lista()
    
    def select_lista(self):
        self.lista_cli.delete(*self.lista_cli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute("""SELECT cod, nome_cliente, telefone, cidade FROM clientes
                                    ORDER BY nome_cliente ASC; """)
        for i in lista:
            self.lista_cli.insert("", END, values=i)
        self.desconecta_bd()
    def buscar_cliente(self):
        self.conecta_bd()
        self.lista_cli.delete(*self.lista_cli.get_children())

        self.entr_nome.insert(END, '%')
        nome = self.entr_nome.get()
        self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
                            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
        buscar_nome_cli = self.cursor.fetchall()
        for i in buscar_nome_cli:
            self.lista_cli.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_bd()
        
    


class Aplication(Funcs):
    def __init__(self):
        self.janela = janela    # variavel janela
        self.tela()              # chama a função tela
        self.frames_Da_tela()     # chama os frames
        self.widgets_frame1()
        self.lista_frame2()
        self.monta_tabelas()
        self.select_lista()
        self.Menus()
        janela.mainloop()          # mantem  a janela aberta

    def tela(self):
        self.janela.title('Cadastro de Clientes')
        self.janela.geometry('700x500')               # tamanho da tela
        self.janela.configure(fg_color='#272D2D')      # fg_color altera cor de fundo da janela
        self.janela.resizable(True, True)  # para aumentar e diminuir o tamanho da janela
        self.janela.maxsize(width= 900, height= 700)    # tamanho max para aumentar janela
        self.janela.minsize(width= 500, height= 400)     # tamanho min

    def frames_Da_tela(self):
            # primeiro frame                        # fg_color muda cor do frame
        self.frame_1 = CTkFrame(master=self.janela, fg_color='#1B2A41',
                                bg_color='transparent', border_width= 5, border_color='#0C1821') # bg_color altera cor das quinas
        self.frame_1.place(relx= 0.02, rely=0.02, relwidth= 0.96, relheight= 0.46)
            # segundo frame
        self.frame_2 = CTkFrame(master=self.janela, fg_color='#1B2A41', bg_color='transparent', border_width=5,
                                border_color='#0C1821')
        self.frame_2.place(relx=0.02, rely=0.5, relwidth=0.96, relheight=0.46)

    def widgets_frame1(self):
        ### botao limpar
        self.bt_limpar = CTkButton(self.frame_1, text= 'Limpar', border_width= 2, corner_radius= 8,bg_color='transparent', border_color='#0C1821', fg_color= '#324A5F', text_color= 'white', font= ('poppins', 11, 'bold'), command=self.limpa_tela)
        self.bt_limpar.place(relx= 0.055, rely= 0.7, relwidth= 0.1, relheight= 0.15)
        ### botao Buscar
        self.bt_buscar = CTkButton(self.frame_1, text= 'Buscar', border_width= 2, corner_radius= 8, bg_color='transparent',border_color='#0C1821', fg_color= '#324A5F', text_color= 'white', font= ('poppins', 11, 'bold'), command= self.buscar_cliente)
        self.bt_buscar.place(relx= 0.6, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        ### botao salvar
        self.bt_salvar = CTkButton(self.frame_1, text= 'Salvar', border_width= 2, corner_radius= 8, bg_color='transparent',border_color='#0C1821', fg_color= '#324A5F', text_color= 'white', font= ('poppins', 11, 'bold'), command= self.add_cliente)
        self.bt_salvar.place(relx= 0.352, rely= 0.7, relwidth= 0.1, relheight= 0.15)
        ### botao alterar
        self.bt_alterar = CTkButton(self.frame_1, text= 'Alterar', border_width= 2, corner_radius= 8,       bg_color='transparent',border_color='#0C1821', fg_color= '#324A5F', text_color= 'white', font= ('poppins', 11, 'bold'), command= self.altera_cliente)
        self.bt_alterar.place(relx= 0.71, rely= 0.1, relwidth= 0.1, relheight= 0.15)
        ### botao apagar
        self.bt_apagar = CTkButton(self.frame_1, text= 'Apagar',border_width= 2, corner_radius= 8, bg_color='transparent',border_color='#0C1821', fg_color= '#324A5F', text_color= 'white', font= ('poppins', 11, 'bold'), command=self.deleta_cliente)
        self.bt_apagar.place(relx= 0.82, rely= 0.1, relwidth= 0.1, relheight= 0.15)



        self.entr_codigo = CTkEntry(self.frame_1, fg_color='white', text_color='black', border_color='#C5C5C5', placeholder_text= 'Código', font= ('poppins', 12, 'bold'))
        self.entr_codigo.place(relx= 0.05, rely= 0.12,relwidth= 0.1)

        

        self.entr_nome = CTkEntry(self.frame_1, fg_color='white', text_color='black', border_color='#C5C5C5', placeholder_text= 'Nome', font= ('poppins', 12, 'bold'))
        self.entr_nome.place(relx= 0.05, rely= 0.32,relwidth= 0.4)

        
        self.entr_tel = CTkEntry(self.frame_1, fg_color='white', text_color='black', border_color='#C5C5C5', placeholder_text= 'Telefone', font= ('poppins', 12, 'bold'))
        self.entr_tel.place(relx= 0.05, rely= 0.5,relwidth= 0.2)


        self.entr_cidade = CTkEntry(self.frame_1, fg_color='white', text_color='black', border_color='#C5C5C5', placeholder_text= 'Cidade', font= ('poppins', 12, 'bold'))
        self.entr_cidade.place(relx= 0.27, rely= 0.5,relwidth= 0.181)

    
    def lista_frame2(self):
        self.lista_cli = ttk.Treeview(self.frame_2, height= 3, column=('col1', 'col2', 'col3', 'col4'))
        self.lista_cli.heading("#0", text= '')
        self.lista_cli.heading("#1", text= 'Código')
        self.lista_cli.heading("#2", text= 'Nome')
        self.lista_cli.heading("#3", text= 'Telefone')
        self.lista_cli.heading("#4", text= 'Cidade')


        self.lista_cli.column("#0", width= 1)
        self.lista_cli.column("#1", width= 50)         ### a proporção total é 500, de acordo com a quantidade
        self.lista_cli.column("#2", width= 200)        ### de colunas podemos escolher a proporção correspondente
        self.lista_cli.column("#3", width= 125)        ### para cada uma.
        self.lista_cli.column("#4", width= 125)

        self.lista_cli.place(relx= 0.01, rely= 0.1, relwidth= 0.95, relheight= 0.85)
        
        self.scrool_lista = CTkScrollbar(self.frame_2, orientation='vertical', command=self.lista_cli.yview)
        self.lista_cli.configure(yscroll=self.scrool_lista.set)
        self.scrool_lista.place(relx= 0.96, rely= 0.1, relwidth= 0.033, relheight= 0.86)
        self.lista_cli.bind("<Double-1>", self.duplo_click)

    def Menus(self):
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        filemenu = Menu(menubar)
        filemenu2 = Menu(menubar)

        def Sair(): self.janela.destroy()

        menubar.add_cascade(label= "Opções", menu= filemenu)
        menubar.add_cascade(label= "Sobre", menu= filemenu2)

        filemenu.add_command(label= "Sair", command= Sair)
        filemenu2.add_command(label= "Limpa Tela", command= self.limpa_tela)

Aplication()
 
