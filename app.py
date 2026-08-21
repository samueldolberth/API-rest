from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

produtos = [
    {
        "nome": "Mouse", 
        "preco": 49.90, 
        "estoque": 10,
        "categoria": "Periféricos",
        "descricao": "Mouse óptico com fio."
    },
    {
        "nome": "Teclado", 
        "preco": 89.90, 
        "estoque": 5,
        "categoria": "Periféricos",
        "descricao": "Teclado mecânico com iluminação RGB."
    },
    {
        "nome": "Monitor", 
        "preco": 599.90, 
        "estoque": 2,
        "categoria": "Informática",
        "descricao": "Monitor LED de 24 polegadas."
    }
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

        produtos.append({"nome": nome, "preco": preco, "estoque": estoque, "categoria": categoria, "descricao": descricao})
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