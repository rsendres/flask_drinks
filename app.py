from flask import Flask, render_template, request, redirect, url_for, flash, g
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ChaVeSecreTApRoEx2022'
BANCO = 'receitas_de_drinks.db'


def criar_banco():
    db = sqlite3.connect(BANCO)
    db.execute(
        ''' CREATE TABLE IF NOT EXISTS receitas(
                ID INTEGER PRIMARY KEY AUTOINCREMENT,
                NOME VARCHAR NOT NULL,
                TEMPO VARCHAR,
                INGREDIENTES TEXT NOT NULL,
                GUARNICAO VARCHAR,
                MODOPREPARO TEXT NOT NULL,
                HISTORIA TEXT,
                IMAGEM TEXT,
                VIDEO TEXT
            )'''
    )
    db.close()


def db():
    # Conecta com o banco sempre que necessário
    # Guarda a conexão na variável da requisição "g"
    if 'db' not in g:
        g.db = sqlite3.connect(BANCO)
    return g.db


@app.teardown_appcontext #fecha a conexão automaticamente toda vez que usuario terminar o serviço
def close_db(exception):
    # Fechar a conexão depois de cada request
    if 'db' in g:
        g.db.close()


@app.route("/")
@app.route("/index") #rota principal
def index():
    db().row_factory = sqlite3.Row
    data = db().execute("SELECT * FROM receitas").fetchall() #retorna do DB todas as receitas

    return render_template("index.html", datas=data)


@app.route("/add_receita", methods=["POST", "GET"])#rota para adicionar receita
def add_receita():
    if request.method == "POST": #tras do html o formulario
        NOME = request.form["NOME"]
        TEMPO = request.form["TEMPO"]
        INGREDIENTES = request.form["INGREDIENTES"]
        GUARNICAO = request.form["GUARNICAO"]
        MODOPREPARO = request.form["MODOPREPARO"]
        HISTORIA = request.form["HISTORIA"]
        IMAGEM = request.form["IMAGEM"]
        VIDEO = request.form["VIDEO"]

        db().execute("INSERT INTO receitas(NOME, TEMPO, INGREDIENTES, GUARNICAO, MODOPREPARO, HISTORIA, IMAGEM, VIDEO) values (?,?,?,?,?,?,?,?)", (NOME, TEMPO, INGREDIENTES, GUARNICAO, MODOPREPARO, HISTORIA, IMAGEM, VIDEO))
        db().commit()#adiciona no banco de dados os dados fornecidos no formulario
        flash("Receita cadastrada com sucesso!", "success")#informa em tela ao usuario que a operação foi efetuada com sucesso
        return redirect(url_for("index"))
    return render_template("add_receita.html")


@app.route("/editar_receita/<string:id>", methods=["POST", "GET"])#rota para edição de uma receita
def editar_receita(id):
    if request.method == "POST":
        NOME = request.form["NOME"]
        TEMPO = request.form["TEMPO"]
        INGREDIENTES = request.form["INGREDIENTES"]
        GUARNICAO = request.form["GUARNICAO"]
        MODOPREPARO = request.form["MODOPREPARO"]
        HISTORIA = request.form["HISTORIA"]
        IMAGEM = request.form["IMAGEM"]
        VIDEO = request.form["VIDEO"]

        db().execute("UPDATE receitas SET NOME=?, TEMPO=?, INGREDIENTES=?, GUARNICAO=?, MODOPREPARO=?, HISTORIA=?, IMAGEM=?, VIDEO=? WHERE ID=?", (NOME, TEMPO, INGREDIENTES, GUARNICAO, MODOPREPARO, HISTORIA, IMAGEM, VIDEO, id))
        db().commit()#executa o updade no banco de dados com as novas informações
        flash("Dados de receita atualizada!", "success")#informa em tela ao usuario que a operação foi efetuada com sucesso
        return redirect(url_for("index"))

    db().row_factory = sqlite3.Row
    data = db().execute("SELECT * FROM receitas WHERE ID = ?", (id,)).fetchone()
    return render_template("editar_receita.html", datas=data)


@app.route("/ver_receita/<string:id>", methods=["POST", "GET"])
def ver_receita(id):
    db().row_factory = sqlite3.Row
    data = db().execute("SELECT * FROM receitas WHERE ID = ?", (id,)).fetchone()
    return render_template("ver_receita.html", datas=data)


@app.route("/deletar_receita/<string:id>", methods=["GET"])
def deletar_receita(id):
    db().execute("DELETE FROM receitas WHERE ID=?", (id,))
    db().commit()
    flash("Receita foi apagada!", "warning")
    return redirect(url_for("index"))


if __name__ == '__main__':
    criar_banco()
    app.run(port=80, debug=True)