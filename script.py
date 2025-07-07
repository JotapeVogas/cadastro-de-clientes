# Importações necessárias para o sistema funcionar
import os          
import sqlite3     
import json      
import tkinter as tk
from tkinter import messagebox 

# pega o primeiro cliente do banco e salva em JSON
def exportar_para_json():
    """
    Eu criei essa função para pegar o primeiro cliente cadastrado no banco
    e exportar para um arquivo JSON que será usado no site.
    """
    try:
        conn = sqlite3.connect('banco.db', detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA encoding = 'UTF-8'")  # ccoloquei isso para usar acentos
        
        # pega primeira linha da tabela
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CLIENTES LIMIT 1")
        
        # pega nome das colunas e dados do cliente da primeira linha
        coluna_nome = [description[0] for description in cursor.description]
        linha_1 = cursor.fetchone()
        conn.close()

        if linha_1:
            # coloca os dados em dicionário
            chaves_cliente = dict(zip(coluna_nome, linha_1))
            
            # salva no .json
            with open('clientes.json', 'w', encoding='utf-8') as json_file:
                json.dump(chaves_cliente, json_file, ensure_ascii=False, indent=4)
            print("Dados exportados com sucesso para clientes.json")
        else:
            print("Nenhum dado encontrado na tabela CLIENTES")
    except Exception as e:
        print(f"Deu erro: {e}")

# função para cadastrar clientes
def insert_client(nome, email, telefone, cidade):
    """
    Essa função é chamada quando confirmamos os dados do formulário.
    Ela recebe os dados e tenta salvar no banco.
    """
    try:
        conn = sqlite3.connect('banco.db', detect_types=sqlite3.PARSE_DECLTYPES)
        conn.execute("PRAGMA encoding = 'UTF-8'")
        
        # insere no banco
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO CLIENTES (nome, email, telefone, cidade) VALUES (?, ?, ?, ?)",
            (nome, email, telefone, cidade)
        )
        conn.commit()
        conn.close()
        
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
    except Exception as e:
        # se der erro, mostra qual foi o problema
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# cria interface principal
def abrir_formulario():
    """
    Essa função cria a janela principal com o formulário de cadastro.
    """
    
    # função do botão salvar
    def salvar():
        """
        Essa função é chamada quando o usuário clica em Salvar.
        Ela valida os dados e mostra a janela de confirmação.
        """
        # puxando valores da interface
        nome = entry_nome.get()
        email = entry_email.get()
        telefone = entry_telefone.get()
        cidade = entry_cidade.get()

        # garante que os campos obrigatórios foram preenchidos
        if not nome or not email or not cidade:
            messagebox.showwarning("Atenção", "Preencha todos os campos obrigatórios.")
            return

        # janela de confirmação
        confirm_window = tk.Toplevel(janela)
        confirm_window.title("Confirmação de Dados")
        confirm_window.geometry("400x250")
        confirm_window.resizable(False, False)  # limito o tamanho da janela
        
        # fontes
        font_title = ("Arial", 12, "bold")
        font_data = ("Arial", 10)
        
        # título
        tk.Label(confirm_window, text="Por favor, confira os dados:", font=font_title).pack(pady=10)
        
        # frame para organizar os dados
        data_frame = tk.Frame(confirm_window)
        data_frame.pack(pady=10, padx=20, fill="x")
        
        # mosstra os dados digitados
        tk.Label(data_frame, text=f"Nome: {nome}", font=font_data, anchor="w").pack(fill="x")
        tk.Label(data_frame, text=f"Email: {email}", font=font_data, anchor="w").pack(fill="x")
        tk.Label(data_frame, text=f"Telefone: {telefone}", font=font_data, anchor="w").pack(fill="x")
        tk.Label(data_frame, text=f"Cidade: {cidade}", font=font_data, anchor="w").pack(fill="x")
        
        # frame dos botões Confirmar/Corrigir
        button_frame = tk.Frame(confirm_window)
        button_frame.pack(pady=20)
        
        # confirmar - salva no banco e fecha janelas
        btn_confirm = tk.Button(button_frame, text="Confirmar", width=10,
            command=lambda: [
                insert_client(nome, email, telefone, cidade),
                confirm_window.destroy(),
                janela.destroy()
            ]
        )
        btn_confirm.pack(side="left", padx=10)
        
        # corrigir - volta no formulário
        btn_correct = tk.Button(
            button_frame,
            text="Corrigir",
            width=10,
            command=confirm_window.destroy
        )
        btn_correct.pack(side="left", padx=10)

    # janela principal
    janela = tk.Tk()
    janela.title("Cadastro de Cliente")
    janela.geometry("500x400")
    janela.resizable(False, False)  # limito o tamanho da janela
    
    # fontes
    default_font = ("Arial", 10)
    janela.option_add("*Font", default_font)
    
    main_frame = tk.Frame(janela, padx=20, pady=20)
    main_frame.pack(fill="both", expand=True)
    
    # formulário:
    
    # nome
    tk.Label(main_frame, text="Nome:*").grid(row=0, column=0, sticky="e", pady=5)
    entry_nome = tk.Entry(main_frame, width=40)
    entry_nome.grid(row=0, column=1, pady=5)
    
    # email
    tk.Label(main_frame, text="Email:*").grid(row=1, column=0, sticky="e", pady=5)
    entry_email = tk.Entry(main_frame, width=40)
    entry_email.grid(row=1, column=1, pady=5)
    
    # telefone    
    tk.Label(main_frame, text="Telefone:").grid(row=2, column=0, sticky="e", pady=5)
    entry_telefone = tk.Entry(main_frame, width=40)
    entry_telefone.grid(row=2, column=1, pady=5)
    
    # cidade
    tk.Label(main_frame, text="Cidade:*").grid(row=3, column=0, sticky="e", pady=5)
    entry_cidade = tk.Entry(main_frame, width=40)
    entry_cidade.grid(row=3, column=1, pady=5)
    
    # salvar
    btn_salvar = tk.Button(main_frame, text="Salvar", width=15, command=salvar)
    btn_salvar.grid(row=4, column=0, columnspan=2, pady=20)

    # loop da interface
    janela.mainloop()

# main do programa
if __name__ == "__main__":
    """
    Quando o programa é executado, primeiro verifico se o banco existe.
    Se não existir, eu crio a estrutura necessária.
    """
    
    # verifica se o banco existe
    if not os.path.exists('banco.db'):
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE CLIENTES (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nome TEXT NOT NULL,
                        email TEXT NOT NULL UNIQUE,
                        telefone TEXT,
                        cidade TEXT NOT NULL
                        )''')
        conn.commit()
        conn.close()
        print("Banco de dados criado com sucesso!")
    
    abrir_formulario()
    
    # verifica se é necessário criar o arquivo .json e se é necessário preenchê-lo
    if not os.path.exists('clientes.json') or os.path.getsize('clientes.json') == 0:
        exportar_para_json()