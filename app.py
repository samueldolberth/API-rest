from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

produtos = [
    {"nome": "Mouse", "preco": 49.90, "estoque": 10},
    {"nome": "Teclado", "preco": 89.90, "estoque": 5},
    {"nome": "Monitor", "preco": 599.90, "estoque": 2}
]

@app.route('/')
def index():
    return render_template("index.html", titulo="Catálogo de Produtos", produtos=produtos)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/novo", methods=["GET", "POST"])
def novo():
    if request.method == "POST":
        nome = request.form["nome"]
        preco = float(request.form["preco"])
        if preco <= 0:
            return render_template("novo.html", erro="O preço deve ser maior que zero.")
        
        estoque = int(request.form["estoque"])
        if estoque <= 0: # nessa versao não é possivel cadastrar item sem estoque
            return render_template("novo.html", erro="O estoque deve ser um número não negativo.")
        
        produtos.append({"nome": nome, "preco": preco, "estoque": estoque})
        return redirect(url_for("index"))
    return render_template("novo.html")

@app.route('/produtos_caros')
def produtos_caros():
    produtos_caros = [produto for produto in produtos if produto["preco"] > 100]
    return render_template("index.html", titulo="Produtos Caros", produtos=produtos_caros)

@app.route('/remover_produto/<int:index>', methods=["POST"])
def remover_produto(index):
    if 0 <= index < len(produtos):
        produtos.pop(index)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)