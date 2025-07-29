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

// Función para mostrar notificaciones
function mostrarToast(tipo, mensaje) {
    const toastContainer = document.getElementById('toastContainer');
    const toastEl = document.createElement('div');
    toastEl.className = `toast align-items-center text-white bg-${tipo} border-0`;
    toastEl.innerHTML = `
        <div class="d-flex">
            <div class="toast-body">${DOMPurify.sanitize(mensaje)}</div>
            <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
        </div>
    `;
    toastContainer.appendChild(toastEl);
    new bootstrap.Toast(toastEl).show();
    setTimeout(() => toastEl.remove(), 10000);
}