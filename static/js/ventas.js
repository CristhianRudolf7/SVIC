<<<<<<< HEAD
const configEl = document.getElementById('config-data');
const obtenerClientesURL = configEl.dataset.urlClientes;
const obtenerProductosURL = configEl.dataset.urlProductos;

=======
const urlObtenerProductos = document.getElementById('url-obtener-productos').value;
const urlObtenerClientes = document.getElementById('url-obtener-clientes').value;
>>>>>>> MVP
function roundTo(n, digits) {
    if (digits === undefined) {
        digits = 0;
    }

    var multiplicator = Math.pow(10, digits);
    n = parseFloat((n * multiplicator).toFixed(11));
    return Math.round(n) / multiplicator;
}

var numero = 1;

var sale = {
    venta: {
        cliente: "",
        total: 0.00,
        metodo_pago: $('select[name="metodo_pago"]').val(),
        estado_pago: $('select[name="estado_pago"]').val(),
        estado_envio: $('select[name="estado_envio"]').val(),
        productos: []
    },
    calcularCosto: function () {
        var total = 0.00;

        $.each(this.venta.productos, function (pos, dict) {
            dict.pos = pos;
            dict.subtotal = roundTo(dict.quantity * dict.precio, 2);
            total += roundTo(dict.subtotal, 2);
        });

        this.venta.total = roundTo(total, 2);

        $('input[name="total"]').val(this.venta.total);
        $('input[name="impuesto"]').val(roundTo(this.venta.total * 0.18, 2));
    },
    // Adds an item to the sale object
    agregarProducto: function (producto) {
        this.venta.productos.push(producto);
        this.listarProductos();
    },
    // Shows the selected item in the table
    listarProductos: function () {
        // Calculate the sale
        this.calcularCosto();

        tblItems = $("#table_items").DataTable({
            destroy: true,
            data: this.venta.productos,
            columns: [
                { "data": "numero" },
                { "data": "nombre" },
                { "data": "precio" },
                { "data": "quantity" },
                { "data": "total_product" },
                { "data": "id" },
            ],
            columnDefs: [
                {
                    class: 'text-center',
                    targets: [3],
                    render: function (data, type, row) {
                        return '<input name="quantity" type="text" class="form-control-xs text-center input-sm" autocomplete="off" value="' + row.quantity + '">';
                    },
                },
                {
                    class: 'text-right',
                    targets: [2, 4],
                    render: function (data, type, row) {
                        return parseFloat(data).toFixed(2) + ' $';
                    },
                },
                {
                    class: 'text-center',
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        return '<a rel="delete" type="button" class="btn btn-sm btn-danger" data-bs-toggle="tooltip" title="Delete item"> <i class="mdi mdi-delete"></i> </a>';
                    },
                },
            ],
            rowCallback(row, data, displayNun, displayIndex, dataIndex) {
                $(row).find("input[name='quantity']").TouchSpin({
                    min: 1,
                    max: 100, // Máximo de acuerdo al stock de cada itemo
                    step: 1,
                    decimals: 0,
                    boostat: 1,
                    maxboostedstep: 3,
                    postfix: ''
                });
            },
        });
    },
};

$(document).ready(function () {
    $('#searchbox_customers').select2({
        delay: 250,
        placeholder: "Seleccionar cliente",
        allowClear: true,
        minimumInputLength: 1,
        ajax: {
<<<<<<< HEAD
            url: obtenerClientesURL,
=======
            url: urlObtenerClientes,
>>>>>>> MVP
            type: 'POST',
            data: function (params) {
                return {
                    term: params.term,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val() // Include CSRF token
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            }
        }
    }).on('select2:select', function (e) {
        var data = e.params.data;
        sale.venta.cliente = data.cliente_id;
    });

    $('#searchbox_items').select2({
        delay: 250,
        placeholder: 'Buscar producto',
        minimumInputLength: 1,
        allowClear: true,
        templateResult: template_item_searchbox,
        ajax: {
<<<<<<< HEAD
            url: obtenerProductosURL,
=======
            url: urlObtenerProductos,
>>>>>>> MVP
            type: 'POST',
            data: function (params) {
                return {
                    term: params.term,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            }
        }
    }).on('select2:select', function (e) {
        var data = e.params.data;
        data.producto_id = data.id;
        data.total_product = data.precio
        data.numero = numero;
        numero++;
        console.log(`producto ${JSON.stringify(data)}`);
        sale.agregarProducto(data);
        $(this).val('').trigger('change.select2');
    });

    $('#table_items tbody').on('click', 'a[rel="delete"]', function () {
        var tr = tblItems.cell($(this).closest('td, li')).index();
        producto_nombre = (tblItems.row(tr.row).data().nombre);

        sale.venta.productos.splice(tr.row, 1);
        sale.listarProductos();
        alert(`El producto ${producto_nombre} ha sido eliminado de la venta`);

    }).on('change keyup', 'input[name="quantity"]', function () {
        var quantity = parseInt($(this).val());
        var tr = tblItems.cell($(this).closest('td, li')).index();
        sale.venta.productos[tr.row].quantity = quantity;
        sale.calcularCosto();
        $('td:eq(4)', tblItems.row(tr.row).node()).html(sale.venta.productos[tr.row].subtotal + ' $');
    });

    $('.deleteAll').on('click', function () {
        if (sale.venta.productos.length === 0) return false;
<<<<<<< HEAD
            sale.venta.productos = [];
            sale.listarProductos();
            alert("Todos los productos han sido eliminados de la venta");
=======
        sale.venta.productos = [];
        sale.listarProductos();
        alert('Todos los productos han sido eliminados de la venta');
>>>>>>> MVP
    });

    tblItems = $('#table_items').DataTable({
        columnDefs: [
            {
                targets: [-1],
                orderable: false,
            }
        ],
    });

    function template_item_searchbox(repo) {
        return $(`
                <div class="card mb-3">
                    <div class="card-body">
                        <small class="card-title">${repo.nombre}</small>
                    </div>
                </div>
            `);
    }

    function getAjax(type, url, data, successCallback, errorCallback) {
        $.ajax({
            type: type,
            url: url,
            data: data,
            success: successCallback,
            error: errorCallback
        });
    }

    function roundTo(value, decimals) {
        const factor = Math.pow(10, decimals);
        return Math.round(value * factor) / factor;
    }

    $('form#form_sale').on('submit', function (event) {
        event.preventDefault();

        var amountPaid = parseFloat($('input[name="amount_paid"]').val());
        var grandTotal = parseFloat($('input[name="grand_total"]').val());
        var amountChange = roundTo(amountPaid - grandTotal, 2);
        var metodo_pago = $('select[name="metodo_pago"]').val();
        var estado_pago = $('select[name="estado_pago"]').val();
        var estado_envio = $('select[name="estado_envio"]').val();

        // Gather sale details
        var formData = {
            cliente: $('select[name="customer"]').val(),
            total: $('input[name="total"]').val(),
            metodo_pago: metodo_pago,
            estado_pago: estado_pago,
            estado_envio: estado_envio,
            productos: sale.venta.productos
        };

        var csrftoken = $('input[name="csrfmiddlewaretoken"]').val();

        // Submit the form data via AJAX
        $.ajax({
            url: $(this).attr('action'),
            type: 'POST',
            contentType: 'application/json',
            headers: {
                'X-CSRFToken': csrftoken
            },
            data: JSON.stringify(formData),
            success: function (response) {
                sale.venta.productos = [];
                sale.listarProductos();
                $('form#form_sale').trigger('reset');
<<<<<<< HEAD
                alert("La venta se completó exitosamente");
            },
            error: function (xhr) {
                alert("Error al realizar la venta: " + xhr.responseJSON.message);
=======
                alert('Venta procesada exitosamente');
            },
            error: function (xhr) {
                alert('Error al procesar la venta: ' + xhr.responseText);
>>>>>>> MVP
            }
        });
    });
});