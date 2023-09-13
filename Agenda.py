import PySimpleGUI as sg
import sqlite3
import re 

# Função chamada para verificar se o telefone fornecido é válido
def verificaTel(tel):
    if(tel.isnumeric() == True and len(tel)==11):
        return True
    else:
        return False

# Função chamada para verificar se o nome fornecido é válido
def verificaNome(nome):
    nome2 = nome.replace(' ','')
    if(nome2.isalpha() == True):
        return True
    else:
        return False


# Função chamada para verificar se o email fornecido é válido
def verificaEmail(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
    
    if(re.search(regex,email)):  
        return True  
    else:
        return False

# Função chamada para verificar se há registros na tabela
def verificaAgenda():
    cursor.execute('select * from contatos')
    contatos = cursor.fetchall()
    if(len(contatos)==0):
        return 0
    else:
        return 1

# Função chamada para construir a tela de Exclusão de Contato
def ExcluirContato():
    
    layout = []

    # Pegando todos os registros da tabela Contatos
    cursor.execute('select * from contatos')
    contatos = cursor.fetchall()



    for contato in contatos:
        layout.append([sg.Text('Id: '), sg.InputText(contato[0],readonly=True)])
        layout.append([sg.Text('Nome: '), sg.InputText(contato[1],readonly=True)])
        layout.append([sg.Text('Email: '), sg.InputText(contato[2],readonly=True)])
        layout.append([sg.Text('Telefone: '), sg.InputText(contato[3],readonly=True)])
        layout.append([sg.Check('Marcar para Excluir',key=f'excluirId{contato[0]}')])

    layout.append([sg.Button('Excluir',button_color="green")]) 
    layout.append([sg.Button('Voltar',button_color="red")])    
    
    window = sg.Window('Agenda: Excluir Contato', layout, finalize=True)

    while True:
        
        event,values = window.read()
        
        if(event == 'Excluir'):
            for contato in contatos:
                if(values[f'excluirId{contato[0]}'] == True):
                    cursor.execute(f'delete from contatos where id={contato[0]}')
                    conn.commit()
            
            sg.popup('Exclusão feita!')
            window.close()

        if event==sg.WINDOW_CLOSED or event == 'Voltar':
            break
        
    window.close()

# Função chamada para construir a tela de Edição de Contato
def EditarContato():
    
    layout = []

    # Pegando todos os registros da tabela Contatos
    cursor.execute('select * from contatos')
    contatos = cursor.fetchall()
    nContatos = -1
    for contato in contatos:
        nContatos += 1
        layout.append([sg.Text('Id: '), sg.InputText(contato[0],key=f'idUsuarioEditar{nContatos}',readonly=True)])
        layout.append([sg.Text('Nome: '), sg.InputText(contato[1],key=f'nomeUsuarioEditar{nContatos}')])
        layout.append([sg.Text('Email: '), sg.InputText(contato[2],key=f'emailUsuarioEditar{nContatos}')])
        layout.append([sg.Text('Telefone: '), sg.InputText(contato[3],key=f'telUsuarioEditar{nContatos}')])

    layout.append([sg.Button('Editar',button_color='green')]) 
    layout.append([sg.Button('Voltar',button_color='red')])    
    
    window = sg.Window('Agenda: Editar Contato', layout, finalize=True)
    
    while True:
        
        event,values = window.read()

        if event == 'Editar':
            msgErro = 0
            for i in range(nContatos+1):
                if(verificaTel(values[f'telUsuarioEditar{i}']) == False):
                    sg.popup(f"Atenção! Insira telefone válido para o contato {values[f'idUsuarioEditar{i}']}.")
                    msgErro=1
                else:
                    if(verificaNome(values[f'nomeUsuarioEditar{i}']) == False):
                        sg.popup(f"Atenção! Insira nome válido para o contato {values[f'idUsuarioEditar{i}']}.")
                        msgErro=1
                    else:
                        if(verificaEmail(values[f'emailUsuarioEditar{i}']) == False):
                            sg.popup(f"Atenção! Insira e-mail válido para o contato {values[f'idUsuarioEditar{i}']}.")
                            msgErro=1
                        else:
                            cursor.execute(f"update contatos set nome='{values[f'nomeUsuarioEditar{i}']}',email='{values[f'emailUsuarioEditar{i}']}',telefone='{values[f'telUsuarioEditar{i}']}' where id={values[f'idUsuarioEditar{i}']}")
                            conn.commit()

            if(msgErro==0):
                sg.popup('Edição feita!')
                window.close()
        
        if event==sg.WINDOW_CLOSED or event == 'Voltar':
            break
        
    window.close()

# Função chamada para construir a tela de Visualização de Contatos
def ListagemContatos():
    
    layout = []

    # Pegando todos os registros da tabela Contatos
    cursor.execute('select * from contatos')
    contatos = cursor.fetchall()
    
    for contato in contatos:
        layout.append([sg.Text('Id: '), sg.InputText(contato[0],readonly=True)])
        layout.append([sg.Text('Nome: '), sg.InputText(contato[1],readonly=True)])
        layout.append([sg.Text('Email: '), sg.InputText(contato[2],readonly=True)])
        layout.append([sg.Text('Telefone: '), sg.InputText(contato[3],readonly=True)])

    layout.append([sg.Button('Voltar',button_color='red')])    
    
    window = sg.Window('Agenda: Relatório de Contatos', layout, finalize=True)
    
    while True:
        
        event,values = window.read()

        if event==sg.WINDOW_CLOSED or event == 'Voltar':
            break
        
    window.close()

# Função chamada para construir a tela de Adição de Contato
def AdicionarContato():
    layout = [
            [sg.Text('Nome: '), sg.InputText(key='nomeUsuario')],
            [sg.Text('Email: '), sg.InputText(key='emailUsuario')],
            [sg.Text('Telefone: '), sg.InputText(key='telUsuario')],
            [sg.Button('Adicionar',button_color="green")],
            [sg.Button('Voltar',button_color="red")]
        ]
        
    window = sg.Window('Agenda: Adicionar Contato', layout,finalize=True)
    
    while True:

        event,values = window.read()

        if event == 'Adicionar':
            
            if(verificaTel(values['telUsuario']) == False):
                sg.popup("Atenção! Insira telefone válido.")
            else:
                if(verificaNome(values['nomeUsuario']) == False):
                    sg.popup("Atenção! Insira nome válido.")
                else:
                    if(verificaEmail(values['emailUsuario']) == False):
                        sg.popup("Atenção! Insira e-mail válido.")
                    else:

                        cursor.execute(f"insert into contatos values(NULL,'{values['nomeUsuario']}','{values['emailUsuario']}','{values['telUsuario']}')")
                        conn.commit()
            
                        sg.popup('Contato adicionado!')
                        break
        
        if event == sg.WINDOW_CLOSED or event == 'Voltar':
            break
    
    window.close()

# TELA INICIAL

# Criando o Banco de Dados, se não existir
conn = sqlite3.connect('BDAgenda.db')
cursor = conn.cursor()

# Criando tabela de contatos, se não existir
cursor.execute('CREATE TABLE IF NOT EXISTS contatos (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, nome TEXT NOT NULL, email TEXT NOT NULL, telefone TEXT NOT NULL);')

layout = [
    [sg.Button('Contatos',button_color="green",)],
    [sg.Button('Adicionar'), sg.Button('Editar'), sg.Button('Excluir')],
    [sg.Button('Sair',button_color="red")]
]

window = sg.Window('Agenda: Tela Inicial', layout, size=(280,120), finalize=True)

while True:
    event,values = window.read()

    if event == sg.WINDOW_CLOSED or event=='Sair':
        break

    if event == 'Adicionar':
        window.hide()
        AdicionarContato()
        window.un_hide()
    
    if event == 'Contatos':
        # Se a agenda estiver vazia, uma mensagem é mostrada
        if(verificaAgenda() == 0):
            sg.popup('A agenda está vazia!')
        else:
            window.hide()
            ListagemContatos()
            window.un_hide()

    if event == 'Editar':
        # Se a agenda estiver vazia, uma mensagem é mostrada
        if(verificaAgenda() == 0):
            sg.popup('A agenda está vazia!')
        else:
            window.hide()
            EditarContato()
            window.un_hide()
    
    if event == 'Excluir':

        # Se a agenda estiver vazia, uma mensagem é mostrada
        if(verificaAgenda() == 0):
            sg.popup('A agenda está vazia!')
        else:
            window.hide()
            ExcluirContato()
            window.un_hide()

window.close()