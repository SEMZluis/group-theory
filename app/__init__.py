from flask import Flask, render_template, request, redirect, url_for
from .group import grupo, ordem_elementos, ciclicidade, extrair_conjunto, extrair_tabela


# Inicialização
app = Flask(__name__)

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
@app.route('/verify-group', methods=['GET', 'POST'])
def verifyGroup():
    conjunto = None
    matriz = None
    resultado = None
    ordens = None
    ciclico = None
    eh_grupo = True

    if request.method == "POST":
        matriz = []
        ind = 0
        while f'linha_{ind}' in request.form:
            matriz.append(request.form.getlist(f'linha_{ind}'))
            ind += 1

        conjunto = extrair_conjunto(matriz)
        tabela = extrair_tabela(matriz)

        resultado = grupo(matriz)
        eh_grupo = (not resultado["fechamento"] and not resultado["associatividade"]
                    and resultado["identidade"] and not resultado["inverso"])

        if eh_grupo:
            ordens = ordem_elementos(conjunto, tabela)
            ciclico = ciclicidade(tabela, conjunto)

    return render_template('verify.html',
                           eh_grupo=eh_grupo,
                           conjunto=conjunto,
                           matriz=matriz,
                           resultado=resultado,
                           ordens=ordens,
                           ciclo=ciclico)
