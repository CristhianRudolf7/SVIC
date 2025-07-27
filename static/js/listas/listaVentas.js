function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function eliminarVenta(btnEliminar) {
    const ventaId = btnEliminar.getAttribute('data-id');
    const fila = btnEliminar.closest('tr');

    if (confirm('¿Estás seguro de que deseas eliminar esta venta?')) {
        btnEliminar.disabled = true;
        btnEliminar.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Eliminando...';

        fetch(`/ventas/${ventaId}/eliminar`, {
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
                } else {
                    btnEliminar.disabled = false;
                    btnEliminar.innerHTML = '<i class="mdi mdi-delete"></i> Eliminar';
                    console.log('Error al eliminar el servidor:', data.message);
                }
            })
            .catch(error => {
                btnEliminar.disabled = false;
                btnEliminar.innerHTML = '<i class="mdi mdi-delete"></i> Eliminar';
                console.error('Error al eliminar el producto:', error);
            });
    }
}

document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener('click', function (event) {
        const btnEliminar = event.target.closest('.btn-eliminar');
        if (btnEliminar) {
            eliminarVenta(btnEliminar);
        }
    });
});