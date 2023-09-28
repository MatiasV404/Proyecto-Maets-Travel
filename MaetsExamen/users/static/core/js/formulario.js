var selectDay = document.getElementById("selectDay");
var selectMonth = document.getElementById("selectMonth");
var selectYear = document.getElementById("selectYear");
var messageInput = document.getElementById("messageInput");

function fillSelect(select, start, end) {
    for (var i = start; i <= end; i++) {
        var option = document.createElement("option");
        option.text = i;
        select.add(option);
    }
}

// Obtener referencias a los selectores
var selectDay = document.getElementById("selectDay");
var selectMonth = document.getElementById("selectMonth");
var selectYear = document.getElementById("selectYear");

// Llenar los selectores con valores
fillSelect(selectDay, 1, 31);
fillSelect(selectMonth, 1, 12);
fillSelect(selectYear, 2023, 2030);

// Agregar evento de cambio al select "selectMonth"
selectMonth.addEventListener("change", function() {
    var selectedMonth = parseInt(selectMonth.value);
    var selectValue = document.getElementById("lvisita").value;
    var messageInput = document.getElementById("messageInput");

    fetch(`/api/lugares/${selectValue}/temporadas/`)
        .then(response => response.json())
        .then(data => {
            var valorTemporadaAlta = data.valor_temporada_alta;
            var valorTemporadaBaja = data.valor_temporada_baja;

            if (selectedMonth === 1 || selectedMonth === 2 || selectedMonth === 7 || selectedMonth === 11 || selectedMonth === 12) {
                messageInput.textContent = `Fecha seleccionada en temporada alta. Valor de servicio en temporada alta: ${valorTemporadaAlta}$`;
            } else {
                messageInput.textContent = `Fecha seleccionada en temporada baja. Valor de servicio en temporada baja: ${valorTemporadaBaja}$`;
            }

            messageInput.style.display = "block";
        })
        .catch(error => {
            console.error("Error al obtener los datos de temporada:", error);
        });
});

// Agregar evento de cambio al select "lvisita"
document.getElementById("lvisita").addEventListener("change", function() {
    var selectedMonth = parseInt(selectMonth.value);
    var selectValue = this.value;
    var messageInput = document.getElementById("messageInput");

    fetch(`/api/lugares/${selectValue}/temporadas/`)
        .then(response => response.json())
        .then(data => {
            var valorTemporadaAlta = data.valor_temporada_alta;
            var valorTemporadaBaja = data.valor_temporada_baja;

            if (selectedMonth === 1 || selectedMonth === 2 || selectedMonth === 7 || selectedMonth === 11 || selectedMonth === 12) {
                messageInput.textContent = `Fecha seleccionada en temporada alta. Valor de servicio en temporada alta: ${valorTemporadaAlta}$`;
            } else {
                messageInput.textContent = `Fecha seleccionada en temporada baja. Valor de servicio en temporada baja: ${valorTemporadaBaja}$`;
            }

            messageInput.style.display = "block";
        })
        .catch(error => {
            console.error("Error al obtener los datos de temporada:", error);
        });
});