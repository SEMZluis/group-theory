const tableInput = document.getElementById("table-input")
const updateButton = document.getElementById("update-button")
const errorSpan = document.getElementById("input-error")
const inputPattern = /^\s*[^,\s]+\s*(,\s*[^,\s]+\s*)*$/;

/**
 * Constrói a estrutura da tabela HTML no elemento `#table-body`.]
 * 
 * @param {string[]} input - Lista com os nomes dos elementos do conjunto.
 * @param {string[][]} [tabelaExistente=null] - Matriz com os valores já salvos/preenchidos.
 */
function makeTable(input, tabelaExistente = null) {
    const tableBody = document.getElementById("table-body")
    tableBody.innerHTML = ""

    let headerRow = document.createElement('tr')

    let cornerTh = document.createElement("th")
    let cornerInput = document.createElement("input")
    cornerInput.type = "hidden"
    cornerInput.name = "linha_0"
    cornerInput.value = "○"
    cornerTh.appendChild(cornerInput)
    cornerTh.appendChild(document.createTextNode("○"))
    headerRow.appendChild(cornerTh)

    for (let h = 0; h < input.length; h++) {
        let th = document.createElement("th")
        let txt = document.createElement("input")
        txt.classList.add("input-head", "manrope-medium")
        txt.name = "linha_0"
        txt.value = input[h]
        th.appendChild(txt)
        headerRow.appendChild(th)
    }

    tableBody.appendChild(headerRow)

    for (let i = 0; i < input.length; i++) {
        let tr = document.createElement("tr")
        const rowName = `linha_${i + 1}`

        let firstTd = document.createElement("td")
        let labelInput = document.createElement("input")
        labelInput.type = "hidden"
        labelInput.name = rowName
        labelInput.value = input[i]
        firstTd.appendChild(labelInput)
        firstTd.appendChild(document.createTextNode(input[i]))
        tr.appendChild(firstTd)

        for (let j = 0; j < input.length; j++) {
            let td = document.createElement("td")
            let txt = document.createElement("input")
            txt.type = "text"
            txt.name = rowName
            if (tabelaExistente && tabelaExistente[i] && tabelaExistente[i][j] !== undefined) {
                txt.value = tabelaExistente[i][j]
            }
            td.appendChild(txt)
            tr.appendChild(td)
        }

        tableBody.appendChild(tr)
    }
}
/**
 * Valida o texto digitado, aplica as restrições de formato/tamanho e solicita a montagem da tabela.
 * 
 * @param {string[][]} [tabelaExistente=null] - Matriz contendo a tabela de operação.
 * @returns {void} 
 */
function updateTable(tabelaExistente = null) {
    const rawValue = tableInput.value

    if (!inputPattern.test(rawValue)) {
        errorSpan.textContent = "Formato inválido. Use: elemento, elemento, elemento (ex: e, a, b, c)"
        errorSpan.style.display = "block"
        tableInput.classList.add("input-error-border")
        return
    }

    errorSpan.style.display = "none"
    tableInput.classList.remove("input-error-border")

    const inputValue = rawValue.replace(/\s+/g, '').split(",");

    if (inputValue.length > 12) {
        errorSpan.textContent = "Máximo de 12 elementos."
        errorSpan.style.display = "block"
        tableInput.classList.add("input-error-border")
        return
    }

    errorSpan.style.display = "none"
    tableInput.classList.remove("input-error-border")

    makeTable(inputValue, tabelaExistente)
}

// Event Listeners e Inicialização

updateButton.addEventListener("click", () => updateTable())


/**
 * Verifica se já existe uma matriz previamente carregada.
 * Caso exista, preenche os campos e monta a tabela. 
 * Se não, inicializa com o grupo padrão `{e, a, b, c}`.
 */
if (window.matrizExistente) {
    const conjuntoExistente = window.matrizExistente[0].slice(1)
    const tabelaExistente = window.matrizExistente.slice(1).map(linha => linha.slice(1))
    tableInput.value = conjuntoExistente.join(", ")
    updateTable(tabelaExistente)
} else {
    tableInput.value = "e, a, b, c"
    updateTable()
}