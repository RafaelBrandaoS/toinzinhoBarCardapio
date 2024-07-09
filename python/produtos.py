from python.conexao import criar_conexao, fechar_conexao
from werkzeug.utils import secure_filename
import shutil
import os


def lista_produtos():
    con = criar_conexao('localhost', 'root', '', 'produtos')
    cursor = con.cursor()
    sql = 'SELECT * FROM produtos order by sessao, nome'
    cursor.execute(sql)
    produtos = cursor.fetchall()
    cursor.close()
    con.commit()
    fechar_conexao(con) 
    return produtos


def lista_sessoes():
    produtos = lista_produtos()
    sessao = []
    for produto in produtos:
        if produto[3] not in sessao:
            sessao.append(produto[3])
    return sessao


def salvar_dados(imagem, nome, preco, sessao):
    con = criar_conexao('localhost', 'root', '', 'produtos')
    nome_imagem = imagem.filename
    estenssao = nome_imagem.split('.')[1]
    cursor = con.cursor()
    img = f'imagens/produtos/{nome}.{estenssao}'
    sql = "insert into produtos (id, nome, preco, sessao, img) values (%s, %s, %s, %s, %s)"
    valores = ('', nome, preco, sessao, img)
    cursor.execute(sql, valores)
    cursor.close()
    con.commit()
    fechar_conexao(con)


def salva_imagem(imagem, nome):
        nome_imagem = imagem.filename
        estenssao = nome_imagem.split('.')[1]
        novo_nome = f'{nome}.{estenssao}'
        
        destino_final =  f'.\\static\\imagens\\produtos\\{novo_nome}'
        destino_temp = '.\\temp'
        
        save = os.path.join(destino_temp, secure_filename(imagem.filename))
        imagem.save(save)
        
        shutil.move(f'.\\temp\\{nome_imagem}', destino_final)
        
def pegar_dados(produto_id):
    con = criar_conexao('localhost', 'root', '', 'produtos')
    cursor = con.cursor()
    sql = f'select * from produtos where id = {produto_id}'
    cursor.execute(sql)
    d = cursor.fetchall()
    cursor.close()
    fechar_conexao(con)
    dados = {'id': d[0][0], 'nome': d[0][1], 'preco': d[0][2], 'sessao': d[0][3], 'imagem': d[0][4]}
    return dados
    