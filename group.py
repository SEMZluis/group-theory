"""
Recebe uma tabela em forma de matriz e extrai o conjunto originario dela, ou seja, a primeira linha e coluna.
A partir disso, verifica fechamento, associatividade, identidade, inverso e comutatividade,
determinando se é grupo abeliano. As funções de verificação retornam as violações encontradas,
para caso a tabela não forme grupo.
"""

from itertools import product


def extrair_conjunto(tabela_completa):
    """
    Extrai o conjunto a partir da primeira linha da tabela completa (ignorando o
    primeiro elemento, que é a operação arbitrária).
    """
    return tabela_completa[0][1:]


def extrair_tabela(tabela_completa):
    """
    Extrai os elementos da tabela, removendo a primeira linha e coluna, que são os elementos do conjunto.
    """
    tabela = []
    for linha in tabela_completa[1:]:
        tabela.append(linha[1:])
    return tabela


def operar(tabela, conjunto, a, b):
    """
    Pega a posição dos elementos a e b no conjunto e retorna o resultado da
    operação na tabela. Necessário para verificar associatividade.
    """
    id_a = conjunto.index(a)
    id_b = conjunto.index(b)
    return tabela[id_a][id_b]


def fechamento(tabela, conjunto):
    """
    Verifica se todos os elementos da tabela estão no conjunto.
    Coloca nas violações os elementos que não estão no conjunto.
    """
    violacoes = []
    for linha in (tabela):
        for elemento in (linha):
            if elemento not in conjunto:
                violacoes.append(elemento)
    return violacoes


def associatividade(tabela, conjunto):
    """
    Usa operar para verificar se a operação é associativa para todos os
    elementos do conjunto. Usa product para gerar todas as combinações
    possíveis de 3 elementos do conjunto.
    """
    violacoes = []
    for a, b, c in product(conjunto, repeat=3):
        if operar(tabela, conjunto, operar(tabela, conjunto, a, b), c) != operar(
            tabela, conjunto, a, operar(tabela, conjunto, b, c)
        ):
            violacoes.append((a, b, c))
    return violacoes


def identidade(tabela, conjunto):
    """
    Verifica se existe uma linha específica na tabela que seja igual ao
    conjunto. Retorna o elemento do conjunto correspondente ao elemento
    gerador da linha (identidade).
    """
    for id, linha in enumerate(tabela):
        if linha == conjunto:
            return conjunto[id]
    return False


def inverso(tabela, conjunto):
    """
    Verifica, para cada combinação de elementos do conjunto, se possui um
    resultado na tabela que seja igual à identidade.
    Retorna os elementos do conjunto que não possuem inverso.
    """
    violacoes = []
    id_elemento = identidade(tabela, conjunto)
    for i, elemento in enumerate(conjunto):
        tem_inverso = False
        for j, inv in enumerate(conjunto):
            if tabela[i][j] == id_elemento and tabela[j][i] == id_elemento:
                tem_inverso = True
                break
        if not tem_inverso:
            violacoes.append(elemento)
    return violacoes


def comutatividade(tabela, conjunto):
    """
    Compara cada linha da tabela com a coluna correspondente ao mesmo
    elemento. Se forem diferentes, adiciona a violação.
    """
    violacoes = []
    for i in range(len(conjunto)):
        for j in range(len(conjunto)):
            if tabela[i][j] != tabela[j][i]:
                violacoes.append((conjunto[i], conjunto[j]))
    return violacoes


def grupo(tabela_completa):
    """
    Recebe a tabela completa, extrai o conjunto e a tabela de operações, e
    verifica os axiomas de grupo em ordem: fechamento, associatividade,
    identidade e inverso. Interrompe a verificação assim que um axioma falha,
    e imprime as violações.

    Se todos os axiomas forem satisfeitos, verifica
    também a comutatividade para informar se o grupo é abeliano.

    Retorna True se for grupo e False caso contrário.
    """
    conjunto = extrair_conjunto(tabela_completa)
    tabela = extrair_tabela(tabela_completa)

    resultado = {"fechamento": [], "associatividade": [], "identidade": None, "inverso": [], "comutatividade": []}

    resultado["fechamento"] = fechamento(tabela, conjunto)
    if resultado["fechamento"]:
        return resultado

    resultado["associatividade"] = associatividade(tabela, conjunto)
    if resultado["associatividade"]:
        return resultado

    resultado["identidade"] = identidade(tabela, conjunto)
    if not resultado["identidade"]:
        return resultado

    resultado["inverso"] = inverso(tabela, conjunto)
    if resultado["inverso"]:
        return resultado

    resultado["comutatividade"] = comutatividade(tabela, conjunto)

    return resultado

def ordem_elemento(tabela, conjunto, elemento):
    """
    Calcula a ordem de um elemento no grupo. A ordem é o menor número de vezes que o elemento
    operado com ele mesmo resulta na identidade do grupo. Se o elemento não tiver ordem finita, retorna None
    """
    id_elemento = identidade(tabela, conjunto)
    resultado = elemento
    ordem = 1

    while resultado != id_elemento:
        resultado = operar(tabela, conjunto, resultado, elemento)
        ordem += 1
        if ordem > len(conjunto):  # Quebra loop infinito
            return None  # Elemento não tem ordem finita dentro do grupo

    return ordem

def ordem_elementos(conjunto, tabela):
    """
    Calcula a ordem de todos os elementos do grupo e retorna um dicionário
    com os elementos como chaves e suas ordens como valores.
    """
    ordens = {}
    for elemento in conjunto:
        ordens[elemento] = ordem_elemento(tabela, conjunto, elemento)
    return ordens

def ciclicidade(tabela, conjunto):
    """
    Verifica se o grupo é cíclico. Um grupo é cíclico se existe um elemento
    cujo ordem é igual à ordem do grupo. 
    Retorna uma lista de geradores se o grupo for cíclico, ou False caso contrário.
    """
    geradores = []
    ordem_grupo = len(conjunto)
    for elemento in conjunto:
        if ordem_elemento(tabela, conjunto, elemento) == ordem_grupo:
            geradores.append(elemento)
    return geradores