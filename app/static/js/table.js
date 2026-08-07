const tableInput = document.getElementById("table-input")
const updateButton = document.getElementById("update-button")
const errorSpan = document.getElementById("input-error")
const inputPattern = /^\s*[^,\s]+\s*(,\s*[^,\s]+\s*)*$/;

function makeTable(input) {
    const tableBody = document.getElementById("table-body")
    tableBody.innerHTML = ""

    let headerRow = document.createElement('tr')

    let emptyTh = document.createElement("th")
    emptyTh.innerHTML = "○"
    headerRow.appendChild(emptyTh)

    for (let h = 0; h < input.length; h++) {
        let th = document.createElement("th")
        th.innerHTML = input[h]
        headerRow.appendChild(th)
    }

    tableBody.appendChild(headerRow)

    for (let i = 0; i < input.length; i++) {
        let tr = document.createElement("tr")
        let firstTxt = document.createElement("td")
        firstTxt.innerHTML = input[i]
        tr.appendChild(firstTxt)

        for(let j = 0; j < input.length; j++) {
            let td = document.createElement("td")
            let txt = document.createElement("input")
            txt.type = "text"
            txt.name = `${i}#${j}`
            txt.id = `${i}#${j}`
            td.appendChild(txt)
            tr.appendChild(td)
        }

        tableBody.appendChild(tr)   
    }
    
}

//Deve fazer as verificações para saber se a tabela pode ser feita
function updateTable() {
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

    makeTable(inputValue)
    
}

updateButton.addEventListener("click", () => updateTable())

updateTable()