$(document).ready(function () {
    $('#consultarPedido').click(function () {
        var orderId = $('#order_id').val();  // Pega o valor do input

        if (orderId) {
            $.ajax({
                url: `https://ygvabeqe2g.execute-api.us-east-2.amazonaws.com/prod/orders?orderId=${orderId}`,
                method: 'GET',
                success: function (data) {
                    // Se a resposta vier como string JSON, faça o parse
                    if (typeof data === 'string') {
                        data = JSON.parse(data);
                    }

                    var tableBody = $('#orderDetails tbody');
                    tableBody.empty();

                    // Percorrer cada pedido e adicionar à tabela
                    data.forEach(function (item) {
                        tableBody.append(`
                            <tr>
                                <td>${item.orderId}</td>
                                <td>${item.customerName}</td>
                                <td>${item.customerEmail}</td>
                                <td>${item.status}</td>
                                <td>${item.orderDate}</td>
                                <td>${item.totalAmount}</td>
                            </tr>
                        `);
                    });
                },
                error: function (error) {
                    alert('Erro ao consultar pedido!');
                }
            });
        } else {
            alert('Por favor, insira o código do pedido.');
        }
    });
});
