from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:senha@db/meu_banco'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Pessoa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    idade = db.Column(db.Integer, nullable=False)


@app.route('/')
def index():
    pessoas = Pessoa.query.all()
    return render_template('form.html', pessoas=pessoas)


@app.route('/create', methods=['POST'])
def create():
    nome = request.form['nome']
    idade = request.form['idade']
    pessoa = Pessoa(nome=nome, idade=idade)
    db.session.add(pessoa)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    pessoa = Pessoa.query.get(id)
    if request.method == 'POST':
        pessoa.nome = request.form['nome']
        pessoa.idade = request.form['idade']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', pessoa=pessoa)


@app.route('/delete/<int:id>')
def delete(id):
    pessoa = Pessoa.query.get(id)
    db.session.delete(pessoa)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
