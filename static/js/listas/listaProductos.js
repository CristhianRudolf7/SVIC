// Función para cargar datos de unidad en el modal
function cargarDatosUnidad(productoId) {
    fetch(`/inventario/productos/${productoId}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
        .then(response => {
            if (!response.ok) throw new Error("Error en la respuesta del servidor");
            return response.json();
        })
        .then(data => {

            if (data.success) {
                // Actualizar campos del formulario
                document.getElementById('producto_id').value = data.producto.producto_id;
                document.getElementById('nombre').value = data.producto.nombre;
                document.getElementById('descripcion').value = data.producto.descripcion || '';
                document.querySelector(`select[name="categoria_id"] option[value="${data.producto.categoria_id}"]`).selected = true;
                document.getElementById('precio').value = data.producto.precio || '';
                document.getElementById('stock').value = data.producto.stock || '';
                document.getElementById('fecha_expiracion').value = data.producto.fecha_expiracion || '';
                if (data.producto.unidad_id) {
                    document.querySelector(`select[name="unidad_id"] option[value="${data.producto.unidad_id}"]`).selected = true;
                } else {
                    document.querySelector(`select[name="unidad_id"] option[value=""]`).selected = true;
                }
                document.getElementById('codigo_barras').value = data.producto.codigo_barras || '';

                const vistaPrevia = document.getElementById('vista_previa');

                // Actualizar título del modal
                document.getElementById('modalTitle').textContent = 'Editar producto';

                // Mostrar modal
                const ventana = new bootstrap.Modal(document.getElementById("ventana"));
                ventana.show();
            } else {
                console.log('Error al cargar datos del producto:', data.message);
                mostrarToast('danger', 'Error al cargar datos del producto');
            }
        })
        .catch(error => {
            console.error('Error al cargar datos del producto:', error);
            mostrarToast('danger', 'Error en la conexión, values no encontrados: ' + error.message);
        });
}

function agregarUnidadATabla(producto) {
    const tabla = document.querySelector('#productos-datatable tbody');
    const nuevaFila = document.createElement('tr');

    nuevaFila.innerHTML = `
            <td>${DOMPurify.sanitize(producto.nombre)}</td>
            <td>${DOMPurify.sanitize(producto.categoria || '')}</td>
            <td>${DOMPurify.sanitize(producto.precio)}</td>
            <td>${DOMPurify.sanitize(producto.stock)}</td>
            <td>${DOMPurify.sanitize(producto.unidad || '-')}</td>
            <td class="table-action d-flex justify-content-center gap-2">
                <button type="button"
                    class="btn btn-bg font-14 btn-success btn-ver d-inline-flex"
                    data-id="${DOMPurify.sanitize(producto.producto_id)}">
                    <i class="mdi mdi-eye-outline"></i> Ver
                </button>
                <button type="button"
                    class="btn btn-bg font-14 btn-warning btn-editar d-inline-flex"
                    data-id="${DOMPurify.sanitize(producto.producto_id)}">
                    <i class="mdi mdi-square-edit-outline"></i> Editar
                </button>
                <button type="button" class="btn btn-danger btn-sm btn-eliminar d-inline-flex"
                    data-id="${DOMPurify.sanitize(producto.producto_id)}"
                    data-metodo-url="{% url 'metodosProductos' '00000000-0000-0000-0000-000000000000' %}">
                    <i class="mdi mdi-delete"></i> Eliminar
                </button>
            </td>
        `;

    // Agregar al inicio de la tabla
    if (tabla.children.length > 0) {
        tabla.insertBefore(nuevaFila, tabla.firstChild);
    } else {
        tabla.appendChild(nuevaFila);
    }
}

function formatearFecha(fechaISO) {
    const fecha = new Date(fechaISO);
    return new Intl.DateTimeFormat('es-PE', {
        day: 'numeric',
        month: 'long',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false
    }).format(fecha).replace(',', ' a las');
}

// Función para agregar nueva categoría a la tabla
function actualizarFilaUnidad(producto) {
    const fila = document.querySelector(`button[data-id="${producto.producto_id}"]`).closest('tr');

    if (fila) {
        fila.querySelector('td:nth-child(1)').textContent = producto.nombre || '';
        fila.querySelector('td:nth-child(2)').textContent = producto.categoria || '';
        fila.querySelector('td:nth-child(3)').textContent = producto.precio || '';
        fila.querySelector('td:nth-child(4)').textContent = producto.stock || '';
        fila.querySelector('td:nth-child(5)').textContent = producto.unidad || '-';
    }
}

// Función para guardar cambios de unidad
function guardarUnidad(event) {
    event.preventDefault();
    const form = event.target;

    if (!form.checkValidity()) {
        event.stopPropagation();
        form.classList.add('was-validated');
        return;
    }

    const formData = new FormData(form);
    const productoId = formData.get('producto_id');
    const data = {};
    formData.forEach((value, key) => data[key] = value);

    // Obtener URLs desde los atributos del formulario
    const urlBaseMetodos = form.dataset.metodoUrl;
    const urlLista = form.dataset.listaUrl;

    const method = productoId ? 'PUT' : 'POST';
    const url = productoId
        ? urlBaseMetodos.replace('00000000-0000-0000-0000-000000000000', productoId)
        : urlLista;

    fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify(data)
    })
        .then(response => {
            if (!response.ok) {
                return response.json().then(errData => {
                    throw new Error(errData.message || 'Error en la respuesta del servidor');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                const ventana = bootstrap.Modal.getInstance(document.getElementById("ventana"));
                ventana.hide();

                mostrarToast('success', data.message);

                if (productoId) {
                    actualizarFilaUnidad(data.producto);
                } else {
                    agregarUnidadATabla(data.producto);
                }
                form.reset();
                form.classList.remove('was-validated');
            } else {
                console.log('Error al guardar unidad:', data.message);
                mostrarToast('danger', data.message || 'Error al guardar');
            }
        })
        .catch(error => {
            console.log('Error al guardar unidad:', error);
            mostrarToast('danger', 'Error en la conexión: unidad: ' + error.message);
        });
}


// Función para eliminar una categoría
function eliminarUnidad(btnEliminar) {
    const productoId = btnEliminar.getAttribute('data-id');
    const fila = btnEliminar.closest('tr');

    const configDiv = document.getElementById('productos-config');
    if (!configDiv) {
        console.error('No se encontró el elemento productos-config');
        return;
    }

    const urlBase = configDiv.dataset.metodoUrl;
    const url = urlBase.replace('00000000-0000-0000-0000-000000000000', productoId);

    if (confirm('¿Estás seguro de que deseas eliminar este producto?')) {
        btnEliminar.disabled = true;
        btnEliminar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Eliminando...';

        fetch(url, {
            method: 'DELETE',
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => {
            if (!response.ok) throw new Error("Error en la respuesta del servidor");
            return response.json();
        })
        .then(data => {
            if (data.success) {
                fila.remove();
                mostrarToast('success', data.message);
            } else {
                btnEliminar.disabled = false;
                btnEliminar.innerHTML = '<i class="mdi mdi-delete"></i> Eliminar';
                mostrarToast('danger', data.message || 'Error al eliminar');
            }
        })
        .catch(error => {
            btnEliminar.disabled = false;
            btnEliminar.innerHTML = '<i class="mdi mdi-delete"></i> Eliminar';
            console.error('Error al eliminar unidad:', error);
            mostrarToast('danger', 'Error en la conexión: ' + error.message);
        });
    }
}



// Eventos cuando el DOM está listo
document.addEventListener("DOMContentLoaded", function () {
    const agregarBtn = document.getElementById("agregarProducto");
    const cancelarBtn = document.getElementById("cancelarProducto");
    const ventana = new bootstrap.Modal(document.getElementById("ventana"));
    const form = document.getElementById("formUnidad");

    document.addEventListener('click', function (event) {
        const btnEditar = event.target.closest('.btn-editar');
        if (btnEditar) {
            const productoId = btnEditar.getAttribute('data-id');
            cargarDatosUnidad(productoId);
        }
    });

    // Abrir modal
    if (agregarBtn) {
        agregarBtn.addEventListener("click", function () {
            form.reset();
            document.getElementById('producto_id').value = '';
            ventana.show();
        });
    }

    // Cerrar modal
    if (cancelarBtn) {
        cancelarBtn.addEventListener("click", function () {
            ventana.hide();
        });
    }

    // Guardar nueva categoría
    if (form) {
        form.addEventListener('submit', guardarUnidad);
    }

    // Delegación de eventos para los botones eliminar
    document.addEventListener('click', function (event) {
        const btnEliminar = event.target.closest('.btn-eliminar');
        if (btnEliminar) {
            eliminarUnidad(btnEliminar);
        }
    });
});