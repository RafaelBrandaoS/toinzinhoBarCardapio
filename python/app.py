from conexao import criar_conexao, fechar_conexao
from tkinter import *
from tkinter import ttk, messagebox, filedialog
import shutil
import pathlib
import os
from flask import Flask


def mostrar_produtos(con):
    cursor = con.cursor()
    sql = 'SELECT * FROM produtos order by sessao, nome'
    cursor.execute(sql)
    linhas = cursor.fetchall()
    cursor.close()
    return linhas


def imagem(con):
    for produto in mostrar_produtos(con):
        cursor = con.cursor()
        nome = produto[1].lower().replace(' ', '')
        id = produto[0]
        sql = f"update produtos set img = 'imagens/produtos/{nome}.jpg' where id = {id}"
        cursor.execute(sql)
        cursor.close()
        con.commit()


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
        
        
        def select_img():
            global caminho
            caminho = filedialog.askopenfilename(filetypes=[("Arquivos JPEG", "*.jpeg"), ("Arquivos PNG", "*.png"), ("Arquivos JPG", "*.jpg")])
            if caminho:
                imagem.config(text=caminho)
            else:
                print("Nenhum arquivo selecionado")
        
        def adicionar_imagem():
            global estenssao
            if caminho:
                destino_dir = '.\\static\\imagens\\produtos'
                
                estenssao = os.path.splitext(caminho)[1]
                nome_arquivo = f'{nome.get()}{estenssao}'
                
                destino = f'{destino_dir}\\{nome_arquivo}'
                
                shutil.copyfile(caminho, destino)
            else:
                print('erro!!!')
        
        
        ################################
        
        btn_voltar = Button(fr_adicionar, text='Voltar', command=voltar)
        btn_voltar.pack(padx=5, pady=5, anchor='w')
        
        ################################
        
        titulo = Label(fr_adicionar, text='ADICIONAR NOVO PRODUTO', bg='#fff')
        titulo.pack(padx=5, pady=10)
        
        fr_nome = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=28)
        fr_nome.pack(padx=5, pady=2)
        
        Label(fr_nome, text='Nome:', bg='#ddf').place(x=3, y=3, width=90, height=20)
        
        nome = Entry(fr_nome)
        nome.place(x=95, y=3, width=200, height=20)
        
        ################################
        
        fr_preco = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=28)
        fr_preco.pack(padx=5, pady=2)
        
        Label(fr_preco, text='Preço:', bg='#ddf').place(x=3, y=3, width=90, height=20)
        
        preco = Entry(fr_preco)
        preco.place(x=95, y=3, width=200, height=20)
        
        ################################
        
        fr_sessao = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=28)
        fr_sessao.pack(padx=5, pady=2)
        
        Label(fr_sessao, text='Sessão:', bg='#ddf').place(x=3, y=3, width=90, height=20)
        
        sessao = Entry(fr_sessao)
        sessao.place(x=95, y=3, width=200, height=20)
        
        ################################
        
        fr_imagem = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=30)
        fr_imagem.pack(padx=5, pady=2)
        
        Button(fr_imagem, text='Select IMG:', command=select_img).place(x=210, y=3, width=85, height=23)
        
        imagem = Label(fr_imagem, text='selecione uma imagem', bg='#fff', font=('arial', '7', 'bold'), anchor='w')
        imagem.place(x=3, y=3, width=200, height=20)
        
        ################################
        
        def salvar():
            nom = nome.get()
            prec = preco.get()
            ses = sessao.get()
            img = ''
            global caminho
            try:
                adicionar_imagem()
                img = f'imagens/produtos/{nom}{estenssao}'
            except:
                img = ''
            
            if '' not in [ses, nom, prec, ses, img]:
                cursor = con.cursor()
                sql_inserir = f"INSERT INTO produtos (id, nome, preco, sessao, img) VALUES {('', nom, prec, ses, img)}"
                cursor.execute(sql_inserir)
                cursor.close()
                con.commit()
                for item in tree.get_children():
                    tree.delete(item)
                tb_linhas()
                voltar()
                messagebox.showinfo(title='sucesso', message=f'Produto {nom} adicionado com sucesso!')
            else:
                messagebox.showinfo(title='ERRO', message='Digite todos os Dados!!!')
        
        
        ################################
        
        fr_btn = Frame(fr_adicionar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=30)
        fr_btn.pack(padx=5, pady=2)
        
        
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
            
            def select_nova_img():
                global novo_caminho
                novo_caminho = filedialog.askopenfilename(filetypes=[("Arquivos JPEG", "*.jpeg"), ("Arquivos PNG", "*.png"), ("Arquivos JPG", "*.jpg")])
                if novo_caminho:
                    imagem.config(text=novo_caminho)
                else:
                    print("Nenhum arquivo selecionado")
                
                
            def adicionar_nova_imagem():
                global novo_caminho
                global edit_estenssao
                destino_dir = '.\\static\\imagens\\produtos'
                
                edit_estenssao = os.path.splitext(novo_caminho)[1]
                nome_arquivo = f'{nome_produto}{edit_estenssao}'
                
                destino = f'{destino_dir}\\{nome_arquivo}'
                
                shutil.copyfile(novo_caminho, destino)
                novo_caminho = ''
            
            btn_voltar = Button(fr_editar, text='Voltar', command=voltar)
            btn_voltar.pack(padx=5, pady=5, anchor='w')
            
            Label(fr_editar, text=f"EDITANDO PRODUTO '{nome_produto}'", bg='#fff').pack(padx=5, pady=10)
            
            ################################
            
            ################################
            fr_nome = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=28)
            fr_nome.pack(padx=5, pady=2)
            
            Label(fr_nome, text='Novo Nome:', bg='#ddf').place(x=3, y=3, width=90, height=20)
            
            nome = Entry(fr_nome)
            nome.place(x=95, y=3, width=200, height=20)
            ################################
            
            ################################
            fr_preco = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=28)
            fr_preco.pack(padx=5, pady=2)
            
            Label(fr_preco, text='Novo Preço:', bg='#ddf').place(x=3, y=3, width=90, height=20)
            
            preco = Entry(fr_preco)
            preco.place(x=95, y=3, width=200, height=20)
            ################################
            
            ################################
            fr_sessao = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=28)
            fr_sessao.pack(padx=5, pady=2)
            
            Label(fr_sessao, text='Novo Sessão:', bg='#ddf').place(x=3, y=3, width=90, height=20)
            
            sessao = Entry(fr_sessao)
            sessao.place(x=95, y=3, width=200, height=20)
            #################################
            
            #################################
            fr_imagem = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=30)
            fr_imagem.pack(padx=5, pady=2)
            
            Button(fr_imagem, text='Nova IMG:', command=select_nova_img).place(x=210, y=3, width=85, height=23)
            
            imagem = Label(fr_imagem, text='', bg='#fff')
            imagem.place(x=3, y=3, width=200, height=20)
            ################################
            def salvar():
                global edit_estenssao
                global novo_caminho
                nom = nome.get()
                prec = preco.get()
                ses = sessao.get()
                try:
                    adicionar_nova_imagem()
                    img_atualizada = 'ok'
                except:
                    img_atualizada = ''
                if '' in nom and '' in prec and '' in ses and '' in img_atualizada:
                    cursor = con.cursor()
                    if nom != '':
                        sql_editar_nome = f"update produtos set nome = '{nom}' where id = {id}"
                        cursor.execute(sql_editar_nome)
                        messagebox.showinfo(title='SUCESSO', message='Nome atualizado com Sucesso!')
                    if prec != '':
                        sql_editar_preco = f"update produtos set preco = '{prec}' where id = {id}"
                        cursor.execute(sql_editar_preco)
                        messagebox.showinfo(title='SUCESSO', message='Preço atualizado com Sucesso!')
                    if ses != '':
                        sql_editar_sessao = f"update produtos set sessao = '{ses}' where id = {id}"
                        cursor.execute(sql_editar_sessao)
                        messagebox.showinfo(title='SUCESSO', message='Sessão atualizada com Sucesso!')
                    if img_atualizada != '':
                        sql_editar_caminho = f"update produtos set img = 'imagens/produtos/{nome_produto}{edit_estenssao}' where id = {id}"
                        cursor.execute(sql_editar_caminho)
                        messagebox.showinfo(title='SUCESSO', message='Imagem atualizada com Sucesso!')
                    
                    cursor.close()
                    con.commit()
                    
                    for item in tree.get_children():
                        tree.delete(item)
                    tb_linhas()
                    voltar()
                else:
                    messagebox.showinfo(title='ERRO', message='Atualize pelo menos um valor ou clique em cancelar.')
            ################################
            fr_btn = Frame(fr_editar, borderwidth=1, relief='solid', bg='#ddf', width=300, height=30)
            fr_btn.pack(padx=5, pady=2)
            
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
            if sn == 'yes':
                lista_id = []
                lista_nome = []
                for linha in linha_selecionada:
                    id = tree.item(linha, 'values')[0]
                    nome = tree.item(linha, 'values')[1]
                    lista_id.append(id)
                    lista_nome.append(nome)
                for id in lista_id:
                    cursor = con.cursor()
                    sql = f"delete from produtos where id = '{id}'"
                    cursor.execute(sql)
                    cursor.close()
                    con.commit()
                    for item in tree.get_children():
                        tree.delete(item)
                    tb_linhas()
                for nome in lista_nome:
                    try:
                        os.unlink(f'.\static\imagens\produtos\{nome}.jpg')
                    except:
                        try:
                            os.unlink(f'.\static\imagens\produtos\{nome}.png')
                        except:
                            try:
                                os.unlink(f'.\static\imagens\produtos\{nome}.jpeg')
                            except:
                                print(nome)
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