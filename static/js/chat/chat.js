function actualizarHora(nombre) {
    const ahora = new Date();
    let horas = ahora.getHours();
    let minutos = ahora.getMinutes();
    const ampm = horas >= 12 ? 'PM' : 'AM';

    horas = horas % 12;
    horas = horas ? horas : 12;
    minutos = minutos < 10 ? '0' + minutos : minutos;

    const horaFormateada = `${horas}:${minutos} ${ampm}`;
    document.getElementById(nombre).textContent = horaFormateada;
}

actualizarHora('hora-actual');

document.getElementById('enviar').addEventListener('click', enviarMensaje);

function enviarMensaje() {
    const mensajeInput = document.getElementById('mensaje');
    const mensajeTexto = mensajeInput.value.trim();
    if (!mensajeTexto) return;

    const ahora = new Date();
    let horas = ahora.getHours();
    let minutos = ahora.getMinutes();
    const ampm = horas >= 12 ? 'PM' : 'AM';

    horas = horas % 12;
    horas = horas ? horas : 12;
    minutos = minutos < 10 ? '0' + minutos : minutos;

    const horaFormateada = `${horas}:${minutos} ${ampm}`;

    const mensajeHTML = `
      <div class="d-flex justify-content-end text-end mb-1">
        <div class="max-75 w-auto">
          <div class="d-flex flex-column align-items-end">
            <div class="bg-primary text-white p-2 px-3 rounded-2">${mensajeTexto}</div>
            <div class="d-flex my-2">
              <div class="small text-secondary">${horaFormateada}</div>
              <div class="small ms-2"><i class="fa-solid fa-check-double text-info"></i></div>
            </div>
          </div>
        </div>
      </div>`;

    document.getElementById('chat-mensajes').insertAdjacentHTML('beforeend', mensajeHTML);
    mensajeInput.value = '';
    fetch("{% url 'chat_api' %}", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: mensajeTexto })
    })
        .then(res => res.json())
        .then(data => {
            const botHTML = `
        <div class="d-flex mb-1">
          <div class="flex-shrink-0 avatar avatar-xs me-2">
            <img class="avatar-img rounded-circle max-100" src="{% static 'imagenes/bot.png' %}">
          </div>
          <div class="flex-grow-1">
            <div class="max-75 w-auto">
              <div class="d-flex flex-column align-items-start">
                <div class="bg-light text-secondary p-2 px-3 rounded-2">
                  ${marked.parse(data.text)}
                </div>
                <div class="small my-2">${horaFormateada}</div>
              </div>
            </div>
          </div>
        </div>`;
            document.getElementById('chat-mensajes').insertAdjacentHTML('beforeend', botHTML);
        })
        .catch(console.error);
}