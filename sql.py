import sqlite3
import tkinter as tk
from tkinter import ttk

# Função para criar a tabela se ela não existir
def criar_tabela():
    conn = sqlite3.connect('exemplo.db')
    cursor = conn.cursor()
    
    # Verificar se a tabela já existe
    cursor.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='usuarios' ''')
    
    # Se não existir, criar a tabela
    if cursor.fetchone()[0] == 0:
        cursor.execute('''CREATE TABLE usuarios (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            nome TEXT,
                            idade INTEGER,
                            email TEXT,
                            telefone TEXT
                        )''')
        conn.commit()
    
    conn.close()

# Função para inserir um novo usuário
def inserir_usuario(nome, idade, email, telefone):
    conn = sqlite3.connect('exemplo.db')
    cursor = conn.cursor()
    
    # Executar um comando SQL para inserir um novo usuário
    cursor.execute('''INSERT INTO usuarios (nome, idade, email, telefone) VALUES (?, ?, ?, ?)''', (nome, idade, email, telefone))
    conn.commit()
    
    conn.close()

# Função para atualizar um usuário existente
def atualizar_usuario(id_usuario, nome, idade, email, telefone):
    conn = sqlite3.connect('exemplo.db')
    cursor = conn.cursor()
    
    # Executar um comando SQL para atualizar o usuário
    cursor.execute('''UPDATE usuarios SET nome=?, idade=?, email=?, telefone=? WHERE id=?''', (nome, idade, email, telefone, id_usuario))
    conn.commit()
    
    conn.close()

# Função para excluir um usuário
def excluir_usuario(id_usuario):
    conn = sqlite3.connect('exemplo.db')
    cursor = conn.cursor()
    
    # Executar um comando SQL para excluir o usuário
    cursor.execute('''DELETE FROM usuarios WHERE id=?''', (id_usuario,))
    conn.commit()
    
    conn.close()

# Função para ler os dados da tabela e atualizar a treeview com opção de busca
def ler_dados(tree, termo_busca=None):
    conn = sqlite3.connect('exemplo.db')
    cursor = conn.cursor()
    
    # Limpar a treeview antes de atualizar
    for item in tree.get_children():
        tree.delete(item)
    
    # Executar uma query para selecionar todos os dados da tabela
    if termo_busca:
        # Busca por nome ou ID (case-insensitive e parte do termo)
        cursor.execute('SELECT id, nome, idade, email, telefone FROM usuarios WHERE lower(nome) LIKE ? OR id LIKE ?', ('%' + termo_busca.lower() + '%', '%' + termo_busca + '%'))
    else:
        cursor.execute('SELECT id, nome, idade, email, telefone FROM usuarios')
        
    rows = cursor.fetchall()
    
    # Adicionar os dados na treeview
    for row in rows:
        tree.insert('', 'end', values=row)
    
    conn.close()

# Função para lidar com o botão de inserção de dados
def inserir_dados_entry(entry_nome, entry_idade, entry_email, entry_telefone, tree):
    nome = entry_nome.get()
    idade = int(entry_idade.get())
    email = entry_email.get()
    telefone = entry_telefone.get()
    
    # Inserir o novo usuário no banco de dados
    inserir_usuario(nome, idade, email, telefone)
    
    # Limpar os campos de entrada após a inserção
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    
    # Atualizar os dados exibidos na treeview
    ler_dados(tree)

# Função para lidar com o botão de atualização de dados
def atualizar_dados_entry(entry_id, entry_nome, entry_idade, entry_email, entry_telefone, tree):
    id_usuario = int(entry_id.get())
    nome = entry_nome.get()
    idade = int(entry_idade.get())
    email = entry_email.get()
    telefone = entry_telefone.get()
    
    # Atualizar o usuário no banco de dados
    atualizar_usuario(id_usuario, nome, idade, email, telefone)
    
    # Limpar os campos de entrada após a atualização
    entry_id.delete(0, tk.END)
    entry_nome.delete(0, tk.END)
    entry_idade.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_telefone.delete(0, tk.END)
    
    # Atualizar os dados exibidos na treeview
    ler_dados(tree)

# Função para lidar com o botão de exclusão de dados
def excluir_dados_entry(entry_id, tree):
    id_usuario = int(entry_id.get())
    
    # Excluir o usuário do banco de dados
    excluir_usuario(id_usuario)
    
    # Limpar os campos de entrada após a exclusão
    entry_id.delete(0, tk.END)
    
    # Atualizar os dados exibidos na treeview
    ler_dados(tree)

# Função para lidar com a busca
def buscar_dados_entry(entry_busca, tree):
    termo_busca = entry_busca.get()
    
    # Atualizar os dados exibidos na treeview com o termo de busca
    ler_dados(tree, termo_busca)

# Função principal que configura a interface Tkinter
def main():
    # Criar a tabela se ela não existir
    criar_tabela()
    
    # Configuração da janela Tkinter
    root = tk.Tk()
    root.title('Cadastro de Usuários')
    
    # Frame para o formulário de inserção
    frame_inserir = ttk.Frame(root)
    frame_inserir.pack(padx=10, pady=10)
    
    # Labels e Entradas para nome, idade, email e telefone (inserção)
    ttk.Label(frame_inserir, text='Nome:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_nome = ttk.Entry(frame_inserir, width=30)
    entry_nome.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frame_inserir, text='Idade:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_idade = ttk.Entry(frame_inserir, width=10)
    entry_idade.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(frame_inserir, text='Email:').grid(row=2, column=0, padx=5, pady=5, sticky='w')
    entry_email = ttk.Entry(frame_inserir, width=30)
    entry_email.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(frame_inserir, text='Telefone:').grid(row=3, column=0, padx=5, pady=5, sticky='w')
    entry_telefone = ttk.Entry(frame_inserir, width=15)
    entry_telefone.grid(row=3, column=1, padx=5, pady=5)
    
    # Botão para inserir dados
    btn_inserir = ttk.Button(frame_inserir, text='Inserir', command=lambda: inserir_dados_entry(entry_nome, entry_idade, entry_email, entry_telefone, tree))
    btn_inserir.grid(row=4, column=1, padx=5, pady=5)
    
    # Frame para o formulário de atualização e exclusão
    frame_atualizar_excluir = ttk.Frame(root)
    frame_atualizar_excluir.pack(padx=10, pady=10)
    
    # Labels e Entradas para ID, nome, idade, email, telefone (atualização e exclusão)
    ttk.Label(frame_atualizar_excluir, text='ID:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_id = ttk.Entry(frame_atualizar_excluir, width=10)
    entry_id.grid(row=0, column=1, padx=5, pady=5)
    
    ttk.Label(frame_atualizar_excluir, text='Novo Nome:').grid(row=1, column=0, padx=5, pady=5, sticky='w')
    entry_novo_nome = ttk.Entry(frame_atualizar_excluir, width=30)
    entry_novo_nome.grid(row=1, column=1, padx=5, pady=5)
    
    ttk.Label(frame_atualizar_excluir, text='Nova Idade:').grid(row=2, column=0, padx=5, pady=5, sticky='w')
    entry_nova_idade = ttk.Entry(frame_atualizar_excluir, width=10)
    entry_nova_idade.grid(row=2, column=1, padx=5, pady=5)
    
    ttk.Label(frame_atualizar_excluir, text='Novo Email:').grid(row=3, column=0, padx=5, pady=5, sticky='w')
    entry_novo_email = ttk.Entry(frame_atualizar_excluir, width=30)
    entry_novo_email.grid(row=3, column=1, padx=5, pady=5)
    
    ttk.Label(frame_atualizar_excluir, text='Novo Telefone:').grid(row=4, column=0, padx=5, pady=5, sticky='w')
    entry_novo_telefone = ttk.Entry(frame_atualizar_excluir, width=15)
    entry_novo_telefone.grid(row=4, column=1, padx=5, pady=5)
    
    # Botões para atualizar e excluir dados
    btn_atualizar = ttk.Button(frame_atualizar_excluir, text='Atualizar', command=lambda: atualizar_dados_entry(entry_id, entry_novo_nome, entry_nova_idade, entry_novo_email, entry_novo_telefone, tree))
    btn_atualizar.grid(row=5, column=1, padx=5, pady=5)
    
    btn_excluir = ttk.Button(frame_atualizar_excluir, text='Excluir', command=lambda: excluir_dados_entry(entry_id, tree))
    btn_excluir.grid(row=5, column=2, padx=5, pady=5)
    
    # Frame para a busca
    frame_busca = ttk.Frame(root)
    frame_busca.pack(padx=10, pady=10)
    
    # Label e Entry para a busca
    ttk.Label(frame_busca, text='Buscar por Nome ou ID:').grid(row=0, column=0, padx=5, pady=5, sticky='w')
    entry_busca = ttk.Entry(frame_busca, width=30)
    entry_busca.grid(row=0, column=1, padx=5, pady=5)
    
    # Botão para buscar dados
    btn_buscar = ttk.Button(frame_busca, text='Buscar', command=lambda: buscar_dados_entry(entry_busca, tree))
    btn_buscar.grid(row=0, column=2, padx=5, pady=5)
    
    # Frame para exibir os dados em uma treeview
    frame_treeview = ttk.Frame(root)
    frame_treeview.pack(padx=10, pady=10)
    
    # Configuração da treeview
    tree = ttk.Treeview(frame_treeview, columns=('ID', 'Nome', 'Idade', 'Email', 'Telefone'), show='headings')
    tree.heading('ID', text='ID')
    tree.heading('Nome', text='Nome')
    tree.heading('Idade', text='Idade')
    tree.heading('Email', text='Email')
    tree.heading('Telefone', text='Telefone')
    tree.pack()
    
    # Atualizar os dados iniciais na treeview
    ler_dados(tree)
    
    # Iniciar o loop principal da aplicação Tkinter
    root.mainloop()

# Verificar se o script está sendo executado diretamente
if __name__ == "__main__":
    main()
