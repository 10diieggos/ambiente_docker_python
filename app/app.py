from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)

# Configurações do banco de dados
db = mysql.connector.connect(
  host="db",
  user="root",
  password="senha",
  database="meu_banco"
)

# Rota principal que exibe o formulário para adicionar uma pessoa
@app.route('/')
def index():
    return render_template('form.html')

# Rota que adiciona uma pessoa ao banco de dados
@app.route('/add', methods=['POST'])
def add_person():
    cursor = db.cursor()
    nome = request.form['nome']
    idade = request.form['idade']
    sql = "INSERT INTO pessoas (nome, idade) VALUES (%s, %s)"
    val = (nome, idade)
    cursor.execute(sql, val)
    db.commit()
    return 'Registro inserido com sucesso!'

# Rota que atualiza uma pessoa no banco de dados
@app.route('/update', methods=['POST'])
def update_person():
    cursor = db.cursor()
    nome = request.form['nome']
    idade = request.form['idade']
    id = request.form['id']
    sql = "UPDATE pessoas SET nome = %s, idade = %s WHERE id = %s"
    val = (nome, idade, id)
    cursor.execute(sql, val)
    db.commit()
    return 'Registro atualizado com sucesso!'

# Rota que remove uma pessoa do banco de dados
@app.route('/delete', methods=['POST'])
def delete_person():
    cursor = db.cursor()
    id = request.form['id']
    sql = "DELETE FROM pessoas WHERE id = %s"
    val = (id,)
    cursor.execute(sql, val)
    db.commit()
    return 'Registro removido com sucesso!'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
