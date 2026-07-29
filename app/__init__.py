from flask import Flask, render_template

# Inicialização
app = Flask(__name__)

app.run(debug=True)

# Rotas

# Exibe a página principal do sistema com um formulário simples que servirá para a formação da tabela de operação.
@app.route('/')
def index():
    return render_template('index.html')

# Descreve o sistema e seu propósito. 
@app.route('/about')
def about():
    return render_template('about.html')

# Recebe e processa os dados da tabela de operação fornecida pelo usuário.
@app.route('/verify-group', methods=['POST'])
def verifyGroup():
    pass