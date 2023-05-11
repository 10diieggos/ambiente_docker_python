from flask import Flask, render_template, request, flash, redirect, url_for
import mysql.connector

app = Flask(__name__)
app.secret_key = 'mysecretkey'

# Configuração do banco de dados
db_config = {
    'host': 'db',
    'user': 'root',
    'password': 'senha',
    'database': 'meu_banco'
}

# Conexão com o banco de dados
mysql = mysql.connector.connect(**db_config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/form')
def form():
    cursor = mysql.cursor(dictionary=True)
    cursor.execute('SELECT * FROM pessoas')
    pessoas = cursor.fetchall()
    cursor.close()
    return render_template('form.html', pessoas=pessoas)

@app.route('/add', methods=['POST'])
def add_person():
    nome = request.form['nome']
    idade = request.form['idade']
    cursor = mysql.cursor()
    cursor.execute('INSERT INTO pessoas (nome, idade) VALUES (%s, %s)', (nome, idade))
    mysql.commit()
    cursor.close()
    flash('Pessoa adicionada com sucesso!')
    return redirect(url_for('form'))

@app.route('/update', methods=['POST'])
def update_person():
    id = request.form['id']
    nome = request.form['nome']
    idade = request.form['idade']
    cursor = mysql.cursor()
    cursor.execute('UPDATE pessoas SET nome = %s, idade = %s WHERE id = %s', (nome, idade, id))
    mysql.commit()
    cursor.close()
    flash('Pessoa atualizada com sucesso!')
    return redirect(url_for('form'))

@app.route('/delete', methods=['POST'])
def delete_person():
    id = request.form['id']
    cursor = mysql.cursor()
    cursor.execute('DELETE FROM pessoas WHERE id = %s', (id,))
    mysql.commit()
    cursor.close()
    flash('Pessoa removida com sucesso!')
    return redirect(url_for('form'))

if __name__ == '__main__':
    app.run(debug=True)
