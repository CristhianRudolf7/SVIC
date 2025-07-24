// Función para cargar datos de unidad en el modal
function cargarDatosUnidad(categoriaId) {
    fetch(`/inventario/categorias/${categoriaId}/`, {
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
            document.getElementById('categoria_id').value = data.categoria.categoria_id;
            document.getElementById('nombreUnidad').value = data.categoria.nombre;
            document.getElementById('simboloUnidad').value = data.categoria.descripcion || '';
            
            // Actualizar título del modal
            document.getElementById('modalTitle').textContent = 'Editar unidad de medida';
            
            // Mostrar modal
            const ventana = new bootstrap.Modal(document.getElementById("ventanaUnidad"));
            ventana.show();
        } else {
            mostrarToast('danger', 'Error al cargar datos de la unidad');
        }
    })
    .catch(error => {
        mostrarToast('danger', 'Error en la conexión, values no encontrados: ' + error.message);
    });
}

// Función para actualizar fila en la tabla
function actualizarFilaUnidad(categoria) {
    const fila = document.querySelector(`button[data-id="${categoria.categoria_id}"]`).closest('tr');

    
    if (fila) {
        // Actualizar celdas específicas
        fila.querySelector('td:nth-child(1)').textContent = categoria.nombre;
        fila.querySelector('td:nth-child(2)').textContent = categoria.descripcion || '';
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
function agregarUnidadATabla(categoria) {
    const tabla = document.querySelector('#products-datatable tbody');
    const nuevaFila = document.createElement('tr');
    
    nuevaFila.innerHTML = `
        <td>${DOMPurify.sanitize(categoria.nombre)}</td>
        <td>${DOMPurify.sanitize(categoria.descripcion || '')}</td>
        <td>${DOMPurify.sanitize(formatearFecha(categoria.fecha_creacion))}</td>
        <td class="table-action d-flex justify-content-center gap-2">
            <button type="button" 
                class="btn btn-bg font-14 btn-success btn-editar-unidad d-inline-flex" 
                data-id="${DOMPurify.sanitize(categoria.id)}">
                <i class="mdi mdi-square-edit-outline"></i> Editar
            </button>
            <button type="button" class="btn btn-danger btn-sm btn-eliminar d-inline-flex"
                data-id="${DOMPurify.sanitize(categoria.id)}">
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
    const categoriaId= formData.get('categoria_id');
    const data = {};
    formData.forEach((value, key) => data[key] = value);
    
    const urlBaseMetodos = form.dataset.metodoUrl;
    const urlLista = form.dataset.listaUrl;

    const method = categoriaId ? 'PUT' : 'POST';
    const url = categoriaId
        ? urlBaseMetodos.replace('00000000-0000-0000-0000-000000000000', categoriaId)
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
            const ventana = bootstrap.Modal.getInstance(document.getElementById("ventanaUnidad"));
            ventana.hide();
            
            mostrarToast('success', data.message);

            if (categoriaId) {
                actualizarFilaUnidad(data.categoria);
            } else {
                agregarUnidadATabla(data.categoria);
            }
            form.reset();
            form.classList.remove('was-validated');
            document.getElementById('categoria_id').value = '';
        } else {
            mostrarToast('danger', data.message || 'Error al guardar');
        }
    })
    .catch(error => {
        mostrarToast('danger', 'Error en la conexión: unidad: ' + error.message);
    });
}

// Función para eliminar una categoría
function eliminarUnidad(btnEliminar) {
    const categoriaId = btnEliminar.getAttribute('data-id');
    const fila = btnEliminar.closest('tr');

    console.log("ID a eliminar:", categoriaId);  // ← Agrega esto
    const configDiv = document.getElementById('categorias-config');
    if (!configDiv) {
        console.error('No se encontró el elemento productos-config');
        return;
    }
    
    const urlBase = configDiv.dataset.metodoUrl;
    const url = urlBase.replace('00000000-0000-0000-0000-000000000000', categoriaId);

    if (confirm('¿Estás seguro de que deseas eliminar esta unidad?')) {
        // Deshabilitar botón durante la solicitud
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
            mostrarToast('danger', 'Error en la conexión: ' + error.message);
        });
    }
}

// Eventos cuando el DOM está listo
document.addEventListener("DOMContentLoaded", function () {
    const agregarBtn = document.getElementById("agregarCategoria");
    const cancelarBtn = document.getElementById("cancelarUnidad");
    const ventana = new bootstrap.Modal(document.getElementById("ventanaUnidad"));
    const form = document.getElementById("formUnidad");

    document.addEventListener('click', function(event) {
        const btnEditar = event.target.closest('.btn-editar-unidad');
        if (btnEditar) {
            const categoriaId = btnEditar.getAttribute('data-id');
            cargarDatosUnidad(categoriaId);
        }
    });

    // Abrir modal
    if (agregarBtn) {
        agregarBtn.addEventListener("click", function () {
            form.reset();
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
    document.addEventListener('click', function(event) {
        const btnEliminar = event.target.closest('.btn-eliminar');
        if (btnEliminar) {
            eliminarUnidad(btnEliminar);
        }
    });
});