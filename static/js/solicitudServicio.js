document.addEventListener("DOMContentLoaded", function () {
    const solicitarServicioBtn = document.getElementById("solicitarServicioBtn");
    const formContainer = document.getElementById("formContainer");
    const solicitudForm = document.getElementById("solicitudForm");
    const loadingMessage = document.getElementById("loadingMessage");
    const fileInput = document.getElementById("logo");
    const fileNameSpan = document.getElementById("file-name");
    const closeFormArrow = document.getElementById("closeFormArrow");

    // Mostrar el formulario al hacer clic en "Solicitar nuevo servicio"
    solicitarServicioBtn.addEventListener("click", function () {
        formContainer.style.display = "block";
        solicitarServicioBtn.style.display = "none";
    });

    // Generar número de solicitud automático (simulado)
    const numeroSolicitud = Math.floor(Math.random() * 1000) + 1;
    document.getElementById("numero_solicitud").value = `SOL-${numeroSolicitud}`;

    // Generar fecha de solicitud automática
    const fechaActual = new Date().toLocaleDateString();
    document.getElementById("fecha_solicitud").value = fechaActual;

    // Lógica para autocompletar campos basados en el cliente
    const nroClienteInput = document.getElementById("nro_cliente");
    nroClienteInput.addEventListener("change", function () {
        const nroCliente = nroClienteInput.value;
        // Simulación de datos de cliente (deberías reemplazar esto con una llamada a tu backend)
        const cliente = {
            razonSocial: "Cliente Ejemplo S.A.",
            horarioAtencion: "09:00 - 18:00",
            calleNumero: "Calle Falsa 123",
            entreCalle: "Calle 1 y Calle 2",
            localidad: "CABA",
            provincia: "Buenos Aires",
            contactoPDV: "Juan Pérez",
            telefono: "1234-5678",
        };

        if (nroCliente === "123") {
            document.getElementById("razon_social").value = cliente.razonSocial;
            document.getElementById("horario_atencion").value = cliente.horarioAtencion;
            document.getElementById("calle_numero").value = cliente.calleNumero;
            document.getElementById("entre_calle").value = cliente.entreCalle;
            document.getElementById("localidad").value = cliente.localidad;
            document.getElementById("provincia").value = cliente.provincia;
            document.getElementById("contacto_pdv").value = cliente.contactoPDV;
            document.getElementById("telefono").value = cliente.telefono;
        }
    });

    // Manejar el envío del formulario
    solicitudForm.addEventListener("submit", function (event) {
        event.preventDefault();

        // Mostrar mensaje de carga
        solicitudForm.style.display = "none";
        loadingMessage.style.display = "block";

        // Simular una carga de 1 segundo
        setTimeout(function () {
            loadingMessage.style.display = "none";
            solicitudForm.style.display = "block";  // Vuelve a mostrar el formulario
            solicitudForm.reset(); // Reiniciar el formulario
            fileNameSpan.textContent = "Ningún archivo seleccionado";
            formContainer.style.display = "none";  // Oculta el formulario después de resetearlo
            solicitarServicioBtn.style.display = "block"; // Muestra el botón nuevamente
        }, 1000);
        
    });

    fileInput.addEventListener("change", function () {
        fileNameSpan.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : "Ningún archivo seleccionado";
    });

    document.getElementById("logo").addEventListener("change", function () {
        let fileName = this.files[0] ? this.files[0].name : "Ningún archivo seleccionado";
        document.getElementById("file-name").textContent = fileName;
    });
    
    closeFormArrow.addEventListener("click", function () {
    formContainer.style.display = "none"; // Oculta el formulario
    solicitarServicioBtn.style.display = "block"; // Muestra el botón "Solicitar nuevo servicio"
});

});