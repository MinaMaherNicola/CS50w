// document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);

    socket.on('connect', () => {

        document.querySelectorAll('button').forEach(button => {
            button.onclick = () => {
                let type = document.querySelector("#selectionValue").value;
                let description = document.querySelector("#description").value;
                let value = document.querySelector("#value").value;

                if (type != null || description != null || value != null) {
                    if (type === "income") {
                        // Add to income
                        if (value > 0) {
                            socket.emit('add income', {'description': description, 'value': value});
                            document.querySelector("#description").value = '';
                            document.querySelector("#value").value = '';
                            document.querySelector("#description").focus();
                        }
                    } else {
                        // Add to expense
                        if (value > 0) {
                            socket.emit('add expense', {'description': description, 'value': value});
                            document.querySelector("#description").value = '';
                            document.querySelector("#value").value = '';
                            document.querySelector("#description").focus();
                        }
                    }
                }
            };
        });

        document.addEventListener('keypress', function(e) {
            if (e.keyCode === 13 || e.which === 13) {
                let type = document.querySelector("#selectionValue").value;
                let description = document.querySelector("#description").value;
                let value = document.querySelector("#value").value;

                if (type != null || description != null || value != null) {
                    if (type === "income") {
                        // Add to income
                        if (value > 0) {
                            socket.emit('add income', {'description': description, 'value': value});
                            document.querySelector("#description").value = '';
                            document.querySelector("#value").value = '';
                            document.querySelector("#description").focus();
                        }
                    } else {
                        // Add to expense
                        if (value > 0) {
                            socket.emit('add expense', {'description': description, 'value': value});
                            document.querySelector("#description").value = '';
                            document.querySelector("#value").value = '';
                            document.querySelector("#description").focus();
                        }
                    }
                }
            }
        });
    });

    socket.on('show income', function(income){
        let html, newHtml;
        html = '<li class="income__item" id=%id%>%description%<span class="text-earning">+$%value%<a class="remove-item" href="#">&#10005;</a></span></li>'
        if (income["description"] != null){
            newHtml = html.replace('%id%', income['id']);
            newHtml = newHtml.replace('%description%', income['description']);
            newHtml = newHtml.replace("%value%", income["value"]);
            document.querySelector(".incomes__list").insertAdjacentHTML('beforeend', newHtml);
        }
        
        document.querySelector('.total__Income--value').innerText = 'Total Income: +$' + income["totalIncome"];
        document.querySelector('.budget__totals--total').innerText = 'Available Budget: $' + income["totalBudget"];
    });

    socket.on('show expense', function(expense){
        let html, newHtml;
        html = '<li class="expense__item" id=%id%>%description%<span class="text-losing">-$%value%<a class="remove-item" href="#">&#10005;</a></span></li>'
        if (expense["description"] != null){
            newHtml = html.replace('%id%', expense['id']);
            newHtml = newHtml.replace('%description%', expense['description']);
            newHtml = newHtml.replace("%value%", expense["value"]);
            document.querySelector(".expenses__list").insertAdjacentHTML('beforeend', newHtml)
        }

        document.querySelector('.total__Expense--value').innerText = 'Total Expense: -$' + expense["totalExpense"] 
        document.querySelector('.budget__totals--total').innerText = 'Available Budget: $' + expense["totalBudget"]
    });

    document.querySelectorAll('.remove-item').forEach(link => {
        link.onclick = () => {
            const type = link.parentElement.parentElement.className;
            const number = link.parentElement.parentElement.id;
            if (type === "income__item"){
                document.getElementById(number).remove();
                socket.emit('remove income', {'index': number});
            } else if (type === "expense__item"){
                document.getElementById(number).remove();
                socket.emit('remove expense', {'index': number});
            }
            
        };
    });
// });