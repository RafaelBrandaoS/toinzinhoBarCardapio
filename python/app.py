from conexao import criar_conexao, fechar_conexao
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from flask import Flask


def mostrar_produtos(con):
    cursor = con.cursor()
    sql = 'SELECT * FROM produtos order by sessao, nome'
    cursor.execute(sql)
    linhas = cursor.fetchall()
    cursor.close()
    return linhas


def interfacie(con):
    janela = Tk()
    janela.title('Gerenciamento do Cardápio')
    janela.geometry('800x600')
    janela.resizable(width=False, height=False)
    
    ####################################
    fr_botoes = Frame(janela, borderwidth=1, relief='raised', bg='#fff')
    fr_botoes.place(x=2, y=2, width=315, height=597)
    
    
    def adicionar():
        janela.title('Adicionar Novo Produto')
        fr_botoes.place(height=0)
        fr_adicionar = Frame(janela, borderwidth=1, relief='raised', bg='#fff')
        fr_adicionar.place(x=2, y=2, width=315, height=597)
        
        def voltar():
            janela.title('Gerenciamento do Cardápio')
            fr_adicionar.place(height=0)
            fr_botoes.place(x=2, y=2, width=315, height=597)
        
        
        btn_voltar = Button(fr_adicionar, text='Voltar', command=voltar)
        btn_voltar.place(x=5, y=5)
        
        Label(fr_adicionar, text='ADICIONAR NOVO PRODUTO', bg='#fff', width=300, height=45).place(x=5, y=33, width=300, height=45)
        
        ################################
        fr_nome = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf')
        fr_nome.place(x=5, y=80, width=300, height=28)
        
        Label(fr_nome, text='Nome:', bg='#ddf').place(x=3, y=3, width=90, height=20)
        
        nome = Entry(fr_nome)
        nome.place(x=95, y=3, width=200, height=20)
        ################################
        
        ################################
        fr_preco = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf')
        fr_preco.place(x=5, y=110, width=300, height=28)
        
        Label(fr_preco, text='Preço:', bg='#ddf').place(x=3, y=3, width=90, height=20)
        
        preco = Entry(fr_preco)
        preco.place(x=95, y=3, width=200, height=20)
        ################################
        
        ################################
        fr_sessao = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf')
        fr_sessao.place(x=5, y=140, width=300, height=28)
        
        Label(fr_sessao, text='Sessão:', bg='#ddf').place(x=3, y=3, width=90, height=20)
        
        sessao = Entry(fr_sessao)
        sessao.place(x=95, y=3, width=200, height=20)
        ################################
        
        
        
        def salvar():
            nom = nome.get()
            prec = preco.get()
            ses = sessao.get()
            
            if '' not in [ses, nom, prec, ses]:
                cursor = con.cursor()
                sql_inserir = f"INSERT INTO produtos (id, nome, preco, sessao) VALUES {('', nom, prec, ses)}"
                cursor.execute(sql_inserir)
                cursor.close()
                con.commit()
                for item in tree.get_children():
                    tree.delete(item)
                tb_linhas()
                messagebox.showinfo(title='sucesso', message=f'Produto {nom} adicionado com sucesso!')
            else:
                messagebox.showinfo(title='ERRO', message='Digite todos os Dados!!!')
        
        
        ################################
        fr_btn = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf')
        fr_btn.place(x=5, y=170, width=300, height=30)
        
        cancel = Button(fr_btn, text='Cancelar', command=voltar)
        cancel.place(x=2, y=2, width=96, height=24)
        
        salv = Button(fr_btn, text='Adicionar', command=salvar)
        salv.place(x=200, y=2, width=96, height=24)
        ################################
        
    
    
    def editar():
        linha_selecionada = tree.selection()
        if len(linha_selecionada) == 1:
            nome_produto = tree.item(linha_selecionada, 'values')[1]
            id = tree.item(linha_selecionada, 'values')[0]
            janela.title(f'Editar o produto {nome_produto}')
            fr_botoes.place(height=0)
            fr_editar = Frame(janela, borderwidth=1, relief='raised', bg='#fff')
            fr_editar.place(x=2, y=2, width=315, height=597)
            
            def voltar():
                fr_editar.place(height=0)
                fr_botoes.place(x=2, y=2, width=315, height=597)
            
            btn_voltar = Button(fr_editar, text='Voltar', command=voltar)
            btn_voltar.place(x=5, y=5)
            
            Label(fr_editar, text=f"EDITANDO PRODUTO '{nome_produto}'", bg='#fff', width=300, height=45).place(x=5, y=33, width=300, height=45)
            
            ################################
            fr_nome = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf')
            fr_nome.place(x=5, y=80, width=300, height=28)
            
            Label(fr_nome, text='Novo Nome:', bg='#ddf').place(x=3, y=3, width=90, height=20)
            
            nome = Entry(fr_nome)
            nome.place(x=95, y=3, width=200, height=20)
            ################################
            
            ################################
            fr_preco = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf')
            fr_preco.place(x=5, y=110, width=300, height=28)
            
            Label(fr_preco, text='Novo Preço:', bg='#ddf').place(x=3, y=3, width=90, height=20)
            
            preco = Entry(fr_preco)
            preco.place(x=95, y=3, width=200, height=20)
            ################################
            
            ################################
            fr_sessao = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf')
            fr_sessao.place(x=5, y=140, width=300, height=28)
            
            Label(fr_sessao, text='Novo Sessão:', bg='#ddf').place(x=3, y=3, width=90, height=20)
            
            sessao = Entry(fr_sessao)
            sessao.place(x=95, y=3, width=200, height=20)
            #################################
            def salvar():
                nom = nome.get()
                prec = preco.get()
                ses = sessao.get()
                if nom in '' and prec in '' and ses in '':
                    messagebox.showinfo(title='ERRO', message='Atualize pelo menos um valor ou clique em cancelar.')
                else:
                    cursor = con.cursor()
                    if nom != '':
                        sql_editar_nome = f"update produtos set nome = '{nom}' where id = {id}"
                        cursor.execute(sql_editar_nome)
                        messagebox.showinfo(title='SUCESSO', message='Atualizado com Sucesso!')
                    if prec != '':
                        sql_editar_preco = f"update produtos set preco = '{prec}' where id = {id}"
                        cursor.execute(sql_editar_preco)
                        messagebox.showinfo(title='SUCESSO', message='Atualizado com Sucesso!')
                    if ses != '':
                        sql_editar_sessao = f"update produtos set sessao = '{ses}' where id = {id}"
                        cursor.execute(sql_editar_sessao)
                        messagebox.showinfo(title='SUCESSO', message='Atualizado com Sucesso!')
                    cursor.close()
                    con.commit()
                    
                    for item in tree.get_children():
                        tree.delete(item)
                    tb_linhas()
                    voltar()
                    
            ################################
            fr_btn = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf')
            fr_btn.place(x=5, y=170, width=300, height=30)
            
            cancel = Button(fr_btn, text='Cancelar', command=voltar)
            cancel.place(x=2, y=2, width=96, height=24)
            
            salv = Button(fr_btn, text='Atualizar', command=salvar)
            salv.place(x=200, y=2, width=96, height=24)
            ################################
            
        elif len(linha_selecionada) < 1:
            messagebox.showinfo(title='ERRO', message='Selecione um item a ser editado')
        else:
            messagebox.showinfo(title='ERRO', message='Selecione apenas um item a ser editado')
    
    
    def remover():
        linha_selecionada = tree.selection()
        if linha_selecionada != ():
            nomes = []
            for i in linha_selecionada:
                nome = tree.item(i, 'values')[1]
                nomes.append(nome)
            sn = messagebox.askquestion(title='CONFIRMAR', message=f"Tem certeza que Deseja excluir os produtos '{nomes}'?")
            sn
            if sn == 'yes':
                lista_id = []
                for linha in linha_selecionada:
                    id = tree.item(linha, 'values')[0]
                    lista_id.append(id)
                for id in lista_id:
                    cursor = con.cursor()
                    sql = f"delete from produtos where id = '{id}'"
                    cursor.execute(sql)
                    cursor.close()
                    con.commit()
                    for item in tree.get_children():
                        tree.delete(item)
                    tb_linhas()
        else:
            messagebox.showinfo(title='ERRO', message='Selecione um ou mais produtos a sere excluidos!')
    
    
    texto = Label(fr_botoes, text='Gerenciamento de Cardápio', bg='#fff', width=310, pady=10)
    texto.pack()
    
    btn_add = Button(fr_botoes, text='Adicionar', bg='#fff', command=adicionar, width=310, pady=10)
    btn_add.pack(pady=5, padx=5)
    
    btn_edit = Button(fr_botoes, text='Editar', bg='#fff', command=editar, width=310, pady=10)
    btn_edit.pack(pady=5, padx=5)
    
    btn_remove = Button(fr_botoes, text='remover', bg='#fff', command=remover, width=310, pady=10)
    btn_remove.pack(pady=5, padx=5)
    
    ####################################
    
    
    def tb_linhas():
        linhas = mostrar_produtos(con)
        
        for i, linha in enumerate(linhas):
            if i % 2 == 0:
                tree.insert('', 'end', values=linha)
            else:
                tree.insert('', 'end', values=linha, tags=('bg'))
                tree.tag_configure('bg', background='#ddd')
    
    
    fr_tabelas = Frame(janela, borderwidth=1, relief='raised', bg='#fff')
    fr_tabelas.place(x=319, y=2, width=480, height=597)
    
    nome_tabela = Label(fr_tabelas, text='produtos', bg='#fff', width=314, pady=10)
    nome_tabela.pack()
    
    tree = ttk.Treeview(fr_tabelas, columns=['id', 'Nome', 'Preço', 'Sessão'], show='headings', height=90)
    tree.pack(pady=5, padx=5)
    
    tree.column('id', width=45, minwidth=50, stretch=NO)
    tree.heading('id', text='id')
    tree.column('Nome', width=190, minwidth=50, stretch=NO)
    tree.heading('Nome', text='Nome')
    tree.column('Preço', width=65, minwidth=50, stretch=NO)
    tree.heading('Preço', text='Preço')
    tree.column('Sessão', width=160, minwidth=50, stretch=NO)
    tree.heading('Sessão', text='Sessão')
    
    tb_linhas()
    
    ####################################
    janela.mainloop()


def main():
    con = criar_conexao('localhost', 'root', '', 'produtos')
    
    interfacie(con)
    
    fechar_conexao(con)


if __name__ == '__main__':
    main()