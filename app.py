from flask import Flask, render_template_string, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Arthurjr.10",
        database="cafeteria_db"
    )

pagina = """
<!DOCTYPE html>
<html>
<head>
    <title>Cafeteria Gourmet</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 20px; background: #f9f6f0; color: #333; }
        .container { max-width: 900px; margin: 0 auto; }
        header { background: #4a2c2a; color: white; padding: 15px 20px; border-radius: 6px; margin-bottom: 20px; }
        h1 { margin: 0; font-size: 22px; }
        .box { background: white; padding: 20px; margin-bottom: 20px; border-radius: 6px; border: 1px solid #e0e0e0; }
        .item-lista { padding: 10px 0; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
        .preco { color: #2e7d32; font-weight: bold; }
        input { width: 100%; max-width: 300px; padding: 8px; margin: 5px 0 12px 0; border: 1px solid #ccc; border-radius: 4px; display: block; }
        button { background: #4a2c2a; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; }
        button:hover { background: #36201e; }
        .btn-excluir { background: #c62828; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer; text-decoration: none; font-size: 13px; }
        .btn-excluir:hover { background: #b71c1c; }
        .grid-forms { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
        .alerta { background: #ffebee; color: #c62828; padding: 10px 15px; border-radius: 4px; margin-bottom: 20px; border: 1px solid #ef9a9a; font-weight: bold; }
        @media (max-width: 768px) { .grid-forms { grid-template-columns: 1fr; } }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>☕ Cafeteria Gourmet - Gestão</h1>
        </header>

        {% if mensagem %}
            <div class="alerta">{{ mensagem }}</div>
        {% endif %}

        <div class="box">
            <h2>Cardápio (Produtos Cadastrados)</h2>
            {% for p in produtos %}
                <div class="item-lista">
                    <div>
                        <strong>{{ p[1] }}</strong> - {{ p[2] }} | <span class="preco">R$ {{ p[3] }}</span>
                    </div>
                    <form action="/excluir_produto/{{ p[0] }}" method="POST" style="margin:0;">
                        <button type="submit" class="btn-excluir" onclick="return confirm('Tem certeza que deseja excluir este produto?')">Excluir</button>
                    </form>
                </div>
            {% else %}
                <p>Nenhum produto cadastrado no momento.</p>
            {% endfor %}
        </div>

        <div class="box">
            <h2>Clientes Cadastrados</h2>
            {% for c in clientes %}
                <div class="item-lista">
                    <div>
                        <strong>{{ c[1] }}</strong> | CPF: {{ c[2] }} | Endereço: {{ c[3] }}
                    </div>
                    <form action="/excluir_cliente/{{ c[0] }}" method="POST" style="margin:0;">
                        <button type="submit" class="btn-excluir" onclick="return confirm('Tem certeza que deseja excluir este cliente?')">Excluir</button>
                    </form>
                </div>
            {% else %}
                <p>Nenhum cliente cadastrado no momento.</p>
            {% endfor %}
        </div>

        <div class="grid-forms">
            <div class="box">
                <h2>Cadastrar Produto</h2>
                <form action="/cadastrar_produto" method="POST">
                    <label>Nome do Produto:</label>
                    <input type="text" name="nome" placeholder="Ex: Capuccino Gelado" required>
                    
                    <label>Descrição:</label>
                    <input type="text" name="descricao" placeholder="Ex: Com chantilly e calda" required>
                    
                    <label>Preço (R$):</label>
                    <input type="number" step="0.01" name="preco" placeholder="15.00" required>
                    
                    <button type="submit">Salvar Produto</button>
                </form>
            </div>

            <div class="box">
                <h2>Cadastrar Cliente</h2>
                <form action="/cadastrar_cliente" method="POST">
                    <label>Nome Completo:</label>
                    <input type="text" name="nome" placeholder="Ex: Ana Silva" required>
                    
                    <label>CPF:</label>
                    <input type="text" name="cpf" placeholder="000.000.000-00" required>
                    
                    <label>Endereço:</label>
                    <input type="text" name="endereco" placeholder="Rua Exemplo, 123" required>
                    
                    <button type="submit">Salvar Cliente</button>
                </form>
            </div>
        </div>
    </div>
</body>
</html>
"""

@app.route("/")
def inicio():
    mensagem = request.args.get("mensagem")
    try:
        con = conectar()
        cursor = con.cursor()
        
        cursor.execute("SELECT * FROM produtos")
        produtos = cursor.fetchall()
        
        cursor.execute("SELECT * FROM clientes")
        clientes = cursor.fetchall()
        
        con.close()
        
        return render_template_string(pagina, produtos=produtos, clientes=clientes, mensagem=mensagem)
    except Exception as e:
        return f"Erro ao conectar no banco de dados: {str(e)}"

@app.route("/cadastrar_produto", methods=["POST"])
def cadastrar_produto():
    nome = request.form["nome"]
    descricao = request.form["descricao"]
    preco = request.form["preco"]

    try:
        con = conectar()
        cursor = con.cursor()
        sql = "INSERT INTO produtos (nome, descricao, preco) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, descricao, preco))
        con.commit()
        con.close()
    except Exception as e:
        return redirect(url_for("inicio", mensagem="Erro: Um produto com este nome já está cadastrado no cardápio!"))

    return redirect(url_for("inicio"))

@app.route("/cadastrar_cliente", methods=["POST"])
def cadastrar_cliente():
    nome = request.form["nome"]
    cpf = request.form["cpf"]
    endereco = request.form["endereco"]

    try:
        con = conectar()
        cursor = con.cursor()
        sql = "INSERT INTO clientes (nome, cpf, endereco) VALUES (%s, %s, %s)"
        cursor.execute(sql, (nome, cpf, endereco))
        con.commit()
        con.close()
    except Exception as e:
        return redirect(url_for("inicio", mensagem="Erro: Este cliente ou CPF já está cadastrado no sistema!"))

    return redirect(url_for("inicio"))

@app.route("/excluir_produto/<int:id>", methods=["POST"])
def excluir_produto(id):
    try:
        con = conectar()
        cursor = con.cursor()
        sql = "DELETE FROM produtos WHERE id = %s"
        cursor.execute(sql, (id,))
        con.commit()
        con.close()
    except Exception as e:
        return redirect(url_for("inicio", mensagem="Erro ao excluir produto."))

    return redirect(url_for("inicio"))

@app.route("/excluir_cliente/<int:id>", methods=["POST"])
def excluir_cliente(id):
    try:
        con = conectar()
        cursor = con.cursor()
        sql = "DELETE FROM clientes WHERE id = %s"
        cursor.execute(sql, (id,))
        con.commit()
        con.close()
    except Exception as e:
        return redirect(url_for("inicio", mensagem="Erro ao excluir cliente."))

    return redirect(url_for("inicio"))

if __name__ == "__main__":
    app.run(debug=True)
