from tkinter import *
from tkinter import ttk
import sqlite3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Image
import webbrowser
import base64

root = Tk()

class relatorios():
    def printCliente(self):
        webbrowser.open("cliente.pdf")
    
    def geraRelatCliente(self):
        self.c = canvas.Canvas("cliente.pdf")
        self.codigoRel = self.codigo_entry.get()
        self.clienteRel = self.cliente_entry.get()
        self.telefoneRel = self.telefone_entry.get()
        self.cpfRel = self.cpf_entry.get()

        self.c.setFont("Helvetica-Bold",24)
        self.c.drawString(200, 790, "Ficha do Cliente" )
        self.c.setFont("Helvetica-Bold",14)
        self.c.drawString(100, 750, 'Nome: ')        
        self.c.drawString(100, 720, 'Telefone: ')
        self.c.drawString(100, 690, 'Cpf: ')

        self.c.setFont("Helvetica",14)
        self.c.drawString(200, 750, self.clienteRel)        
        self.c.drawString(200, 720, self.telefoneRel)
        self.c.drawString(200, 690, self.cpfRel)

        self.c.rect(20, 630, 550, 200, fill=False, stroke=True)

        
        self.c.showPage()
        self.c.save()
        self.printCliente()

class funcs():

    def limpa_tela(self):
        self.codigo_entry.delete(0, END)
        self.cliente_entry.delete(0, END)
        self.telefone_entry.delete(0, END)
        self.cpf_entry.delete(0, END)

    def conecta_db(self):
        self.conn=sqlite3.connect("LCBL.db")
        self.cursor=self.conn.cursor()

    def desconecta_db(self):
        self.conn.close()

    def monta_tabelas(self):
        self.conecta_db()
        self.cursor.execute("CREATE TABLE if not exists clientes(nome_do_cliente text, telefone text, cpf text )")
        self.conn.commit()
        self.desconecta_db()

    def variaveis(self):
        self.cod=self.codigo_entry.get()
        self.cliente=self.cliente_entry.get()
        self.telefone=self.telefone_entry.get()
        self.cpf=self.cpf_entry.get()

    def add_clientes(self):
        #self.codigo=self.codigo=self.codigo_enrty.get()
        self.variaveis()
        self.conecta_db()
        self.cursor.execute("INSERT INTO clientes (nome_do_cliente, telefone, cpf) values (?, ?, ?)",(self.cliente, self.telefone, self.cpf))
        self.conn.commit()
        
        self.desconecta_db()
        self.select_lista()
        self.limpa_tela()

    def select_lista(self):
        self.l_cliente.delete(*self.l_cliente.get_children())
        self.conecta_db()
        lista=self.cursor.execute("SELECT rowid, * FROM clientes ORDER BY rowid ASC;")
        for i in lista:
            self.l_cliente.insert("", END, values=i)
        self.desconecta_db()

    def onDoubleClick(self, event):
        self.limpa_tela()
        self.l_cliente.selection()

        for n in self.l_cliente.selection():
            col1 ,col2, col3, col4= self.l_cliente.item(n, 'values')
            self.codigo_entry.insert(END,col1)
            self.cliente_entry.insert(END,col2)
            self.telefone_entry.insert(END,col3)
            self.cpf_entry.insert(END,col4)

    def deletar(self):
        self.variaveis()
        self.conecta_db()
        self.cursor.execute("DELETE FROM clientes WHERE rowid = "+self.cod+" ")
        self.conn.commit()
        self.desconecta_db()
        self.limpa_tela()
        self.select_lista()
    
    def alterar(self):
        self.variaveis()
        self.conecta_db()
        self.cursor.execute("UPDATE clientes SET nome_do_cliente = (?), telefone = (?), cpf = (?) WHERE rowid = "+self.cod+" ", (self.cliente, self.telefone, self.cpf))
        self.conn.commit()
        self.desconecta_db()
        self.select_lista()
        self.limpa_tela()

    def buscar(self):
        self.conecta_db()
        self.l_cliente.delete(*self.l_cliente.get_children())
        self.cliente_entry.insert(END, '%')
        nome=self.cliente_entry.get()
        self.cursor.execute("SELECT rowid, * FROM clientes WHERE nome_do_cliente LIKE '%s' ORDER BY nome_do_cliente ASC" % nome)
        buscanome=self.cursor.fetchall()
        for i in buscanome:
            self.l_cliente.insert("", END, values=i)
        self.limpa_tela()
        self.desconecta_db()

class Application(funcs, relatorios):

    def __init__(self) -> None:
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame_1()
        self.lista_frame2()
        self.select_lista()
        self.menus()
        root.mainloop()
        pass

    def tela(self):
        self.root.title("Cadastro de clientes")
        self.root.configure(background='black')
        self.root.geometry('800x600')
        self.root.resizable(True,True)
        self.root.maxsize(width=1000, height=700)
        self.root.minsize(width=700, height=600)

    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bg="#B6B4E6" ,bd=4, highlightbackground='gray',highlightthickness=2)
        self.frame_2 = Frame(self.root, bd=4, highlightbackground='gray',highlightthickness=2)
        self.frame_1.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.46 )
        self.frame_2.place(relx=0.02, rely=0.50, relwidth=0.96, relheight=0.46 )
        
    def widgets_frame_1(self):

        self.bt_limpar = Button(self.frame_1, text= 'Limpar', bd= 6, fg='#003233', font= ('arial',10,'bold'), command= self.limpa_tela )
        self.bt_limpar.place(relx=0.2, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_buscar = Button(self.frame_1, text= 'Buscar',  bd= 6, fg='#003233', font= ('arial',10,'bold'), command=self.buscar)
        self.bt_buscar.place(relx=0.3, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_inserir = Button(self.frame_1, text= 'Inserir',  bd= 6, fg='#003233',  font= ('arial',10,'bold'), command= self.add_clientes)
        self.bt_inserir.place(relx=0.6, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_alterar = Button(self.frame_1, text= 'Alterar',  bd= 6, fg='#003233', font= ('arial',10,'bold'), command= self.alterar)
        self.bt_alterar.place(relx=0.7, rely=0.1, relwidth=0.1, relheight=0.15)

        self.bt_apagar = Button(self.frame_1, text= 'Apagar',  bd= 6, fg='#003233', font= ('arial',10,'bold'), command= self.deletar)
        self.bt_apagar.place(relx=0.8, rely=0.1, relwidth=0.1, relheight=0.15)

        self.lb_codigo=Label(self.frame_1, text= "Código", bg="#B6B4E6", fg='#003233', font= ('arial',10,'bold'))
        self.lb_codigo.place(relx= 0.05 ,rely= 0.05)

        self.codigo_entry=Entry(self.frame_1, bd= 4)
        self.codigo_entry.place(relx=0.05 ,rely=0.15, relwidth= 0.1)

        self.lb_cliente=Label(self.frame_1, text= "Nome", bg="#B6B4E6", fg='#003233', font= ('arial',10,'bold'))
        self.lb_cliente.place(relx= 0.05 ,rely= 0.25)

        self.cliente_entry=Entry(self.frame_1, bd= 4)
        self.cliente_entry.place(relx=0.05 ,rely=0.35,relwidth=0.25)

        self.lb_telefone=Label(self.frame_1, text= "Telefone", bg="#B6B4E6", fg='#003233', font= ('arial',10,'bold'))
        self.lb_telefone.place(relx= 0.05 ,rely= 0.45)

        self.telefone_entry=Entry(self.frame_1, bd= 4)
        self.telefone_entry.place(relx=0.05 ,rely=0.55,relwidth=0.25)

        self.lb_cpf=Label(self.frame_1, text= "CPF", bg="#B6B4E6", fg='#003233', font= ('arial',10,'bold'))
        self.lb_cpf.place(relx= 0.05 ,rely= 0.65)

        self.cpf_entry=Entry(self.frame_1, bd= 4)
        self.cpf_entry.place(relx=0.05 ,rely=0.75,relwidth=0.25)

    def lista_frame2(self):
        self.l_cliente= ttk.Treeview(self.frame_2, height=5, columns=("col1","col2","col3","col4"))
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("TkDefaultFont", 9, "bold"))
        
        self.l_cliente.heading("#0", text="")
        self.l_cliente.heading("#1", text="Código")
        self.l_cliente.heading("#2", text="Nome")
        self.l_cliente.heading("#3", text="Telefone")
        self.l_cliente.heading("#4", text="CPF")

        self.l_cliente.column("#0", width=1)
        self.l_cliente.column("#1", width=50, anchor="center")
        self.l_cliente.column("#2", width=200, anchor="center")
        self.l_cliente.column("#3", width=125, anchor="center")
        self.l_cliente.column("#4", width=125, anchor="center")

        self.l_cliente.place(relx="0.02", rely="0.1", relwidth="0.95", relheight="0.85")
    
        self.scrollLista=Scrollbar(self.frame_2, orient="vertical")
        self.l_cliente.configure(yscroll=self.scrollLista.set)
        self.scrollLista.configure(command=self.l_cliente.yview)
        self.scrollLista.place(relx="0.96", rely="0.1", relwidth="0.02", relheight="0.85")
        self.l_cliente.bind("<Double-1>", self.onDoubleClick)

    def menus(self):
        menubar= Menu(self.root)
        self.root.config(menu=menubar)
        filemenu=Menu(menubar)
        filemenu2=Menu(menubar)

        def quit():  
            self.root.destroy()

        menubar.add_cascade(label="Opções", menu= filemenu)
        menubar.add_cascade(label="Relatórios", menu= filemenu2)

        filemenu.add_command(label="Sair", command=quit)
        filemenu.add_command(label="Limpa campos", command=self.limpa_tela)

        filemenu2.add_command(label="Ficha do cliente", command=self.geraRelatCliente)

    
Application()
