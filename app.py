from flask import Flask, make_response, render_template, request, url_for, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+pymysql://root:@localhost:3306/catalogo_produtos"
)
db = SQLAlchemy(app)

app.secret_key = "troque-esta-chave-em-producao"

class Tarefa(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(50))
    descricao = db.Column(db.Text)


def popular_banco():
    if Produto.query.count() == 0:
        db.session.add(Produto(
            nome = "Mouse", 
            preco = 49.90, 
            estoque = 10,
            categoria = "Periféricos",
            descricao = "Mouse óptico com fio."
        ))
        db.session.add(Produto(
            nome = "Teclado",
            preco = 89.90,
            estoque = 5,
            categoria = "Periféricos",
            descricao = "Teclado mecânico com iluminação RGB."
        ))
        db.session.add(Produto(
            nome = "Monitor",
            preco = 599.90,
            estoque = 2,
            categoria = "Informática",
            descricao = "Monitor LED de 24 polegadas."
        ))
        db.session.commit()


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        nome_visitante = request.form.get("nome_visitante", "").strip()
        resp = make_response(redirect(url_for("index")))
        resp.set_cookie("nome_visitante", nome_visitante, max_age=60*60*24*30)  # Cookie válido por 30 dias (seg*min*horas*dias)
        return resp

    nome_visitante = request.cookies.get("nome_visitante")

    produtos = Produto.query.all()

    return render_template(
        "index.html", 
        produtos=produtos, 
        nome_visitante=nome_visitante
    )

@app.route("/esquecer")
def esquecer():
    resp = make_response(redirect(url_for("index")))
    resp.delete_cookie("nome_visitante")
    return resp

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        preco_texto = request.form.get("preco", "")
        estoque_texto = request.form.get("estoque", "")
        categoria = request.form.get("categoria", "")
        descricao = request.form.get("descricao", "").strip()

        erros = []
        if not nome:
            erros.append("O nome do produto é obrigatório.")
        if not categoria:
            erros.append("Selecione uma categoria para o produto.")

        preco = None
        try:
            preco = float(preco_texto)
            if preco <= 0:
                erros.append("O preço deve ser maior que zero.")
        except ValueError:
            erros.append("Preço inválido.")

        estoque = None                                           
        try:
            estoque = int(estoque_texto)
            if estoque <= 0:
                erros.append("O estoque deve ser maior que zero.")
        except ValueError:
            erros.append("Estoque inválido.")

        if erros:
            return render_template("novo.html", erros=erros)

        novo_produto = Produto(
            nome = nome,
            preco = preco,
            estoque = estoque,
            categoria = categoria,
            descricao = descricao
        )

        db.session.add(novo_produto)
        db.session.commit()

        session["cadastrados_na_sessao"] = (
            session.get("cadastrados_na_sessao", 0) + 1
        )
        flash("Produto cadastrado com sucesso!", "sucesso")
        return redirect(url_for("index"))
    return render_template("novo.html")

@app.route('/produtos_caros')
def produtos_caros():
    produtos_caros = Produto.query.filter(Produto.preco > 100).all()

    return render_template("index.html", titulo="Produtos Caros", produtos=produtos_caros)

@app.route('/remover_produto/<int:id>', methods=["POST"])
def remover_produto(id):
    produto = db.get_or_404(Produto, id)

    db.session.delete(produto)
    db.session.commit()

    flash("Produto removido.", "sucesso")

    return redirect(url_for("index"))

@app.route("/produto/<int:produto_id>")
def detalhe_produto(produto_id):
    produto = db.get_or_404(Produto, produto_id)
    return render_template("detalhe.html", produto=produto)

@app.route("/produto/<int:produto_id>/editar", methods=["GET", "POST"])
def editar_produto(produto_id):
    produto = db.get_or_404(Produto, produto_id)
    if request.method == "POST":
        produto.nome = request.form.get("nome", "").strip()
        produto.preco = float(request.form.get("preco", ""))
        produto.estoque = int(request.form.get("estoque", ""))
        produto.descricao = request.form.get("descricao", "").strip()
        db.session.commit()
        flash("Produto atualizado com sucesso!", "sucesso")
        return redirect(url_for("index"))
    return render_template("editar.html", produto=produto)


# teste de coockies
@app.route('/cor', methods=["GET", "POST"])
def cor():
    if request.method == "POST":
        cor_escolhida = request.form.get("cor", "")
        resp = make_response(redirect(url_for("cor")))
        resp.set_cookie("cor_favorita", cor_escolhida)
        return resp

    cor_salva = request.cookies.get(
        "cor_favorita", "nenhuma cor salva ainda"
    )
    return f"""
    <p>Cor salva atualmente: {cor_salva}</p>
    <form method="POST">
        <input type="text" name="cor">
        <button type="submit">Salvar cor</button>
    </form>
"""

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        popular_banco()
    app.run(debug=True)

