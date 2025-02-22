$(document).ready(function () {
// document.getElementById('filterButtonByDate').addEventListener('click', function() {
//     var inputDate = prompt('Enter date (YYYY-MM-DD):');
//     var table = document.getElementById('dataTable');
//     var rows = table.getElementsByTagName('tr');
//     for (var i = 0; i < rows.length; i++) {
//         var actualDateCell = rows[i].querySelectorAll('td')[rows[i].querySelectorAll('td').length - rows[i].querySelectorAll('td').length + 1]; // Last column (... .length - 1 )
//         if (actualDateCell) {
//             var actualDate = actualDateCell.textContent.trim().split(' ')[0]; // Extracting date part
//             if (inputDate === actualDate) {
//                 rows[i].style.display = '';
//             } else {
//                 rows[i].style.display = 'none';
//             }
//         }
//     }
// });

document.getElementById('filterButtonByDate').addEventListener('click', function() {

    var inputSerialNo = prompt('Copy and paste date from row:');
    var table = document.getElementById('dataTable');
    var rows = table.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
    
            var serialNoCell = rows[i].querySelectorAll('td')[rows[i].querySelectorAll('td').length - rows[i].querySelectorAll('td').length + 1 ]; // Material column
            if (serialNoCell) {
                var serialNo = serialNoCell.textContent.trim();
                if (inputSerialNo === serialNo) {
                    rows[i].style.display = '';
                } else {
                    rows[i].style.display = 'none';
                }
            }
    
    
    }
    });

document.getElementById('filterButtonBySerialNo').addEventListener('click', function() {

var inputSerialNo = prompt('Enter Serial No.:');
var table = document.getElementById('dataTable');
var rows = table.getElementsByTagName('tr');
for (var i = 0; i < rows.length; i++) {

        var serialNoCell = rows[i].querySelectorAll('td')[rows[i].querySelectorAll('td').length - rows[i].querySelectorAll('td').length + 2 ]; // Material column
        if (serialNoCell) {
            var serialNo = serialNoCell.textContent.trim();
            if (inputSerialNo === serialNo) {
                rows[i].style.display = '';
            } else {
                rows[i].style.display = 'none';
            }
        }


}
});

document.getElementById('resetButton').addEventListener('click', function() {
    var table = document.getElementById('dataTable');
    var rows = table.getElementsByTagName('tr');
    for (var i = 0; i < rows.length; i++) {
        rows[i].style.display = ''; // Resetuje wyświetlanie wszystkich wierszy
    }
});

       // Funkcja do dodawania zdarzeń kliknięcia w wiersze
       function addRowClickEvents() {
        const table = document.getElementById('dataTable');
        if (!table) return; // Jeśli tabela nie istnieje, zakończ

        const rows = table.querySelectorAll('tr');
        rows.forEach(row => {
            row.addEventListener('click', () => {
                // Usuń zaznaczenie z innych wierszy
                rows.forEach(r => r.classList.remove('selected'));
                
                // Dodaj zaznaczenie do klikniętego wiersza
                row.classList.add('selected');
            });
        });
    }

    // Pobieranie danych z API
    fetch('/data/get')
    .then(response => response.json())
    .then(responseData => {
        const { columns, data } = responseData; // Rozdzielenie kolumn i danych
        console.log('Kolumny:', columns);
        console.log('Dane:', data);

        const container = document.getElementById('table-container');
        
        // Generowanie tabeli
        const table = document.createElement('table');
        table.border = 1;
        table.id = 'dataTable'; // Dodajemy id tabeli

        // Nagłówki tabeli
        const headerRow = document.createElement('tr');
        headerRow.className = "header";
        columns.forEach(column => {
            const th = document.createElement('th');
            th.textContent = column;
            headerRow.appendChild(th);
        });
        table.appendChild(headerRow);

        // Wiersze tabeli
        data.forEach(row => {
            const tr = document.createElement('tr');
            columns.forEach(column => {
                const td = document.createElement('td');
                td.textContent = row[column]; // Wartości po kluczach
                tr.appendChild(td);
            });
            table.appendChild(tr);
        });

        // Wstawianie tabeli do kontenera
        container.textContent = ''; // Wyczyść poprzednie dane
        container.appendChild(table);

        // Dodajemy obsługę kliknięć po załadowaniu tabeli
        addRowClickEvents();
    })
    .catch(error => {
        console.error('Błąd:', error);
        document.getElementById('table-container').textContent = 'Wystąpił błąd podczas ładowania danych.';
    });  
});