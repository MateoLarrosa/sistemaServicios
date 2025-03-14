document.addEventListener("DOMContentLoaded", function () {
    // Elementos del DOM
    const solicitarServicioBtn = document.getElementById("solicitarServicioBtn");
    const formContainer = document.getElementById("formContainer");
    const solicitudForm = document.getElementById("solicitudForm");
    const loadingMessage = document.getElementById("loadingMessage");
    const fileInput = document.getElementById("logo");
    const fileNameSpan = document.getElementById("file-name");
    const closeFormArrow = document.getElementById("closeFormArrow");
    const modeloInput = document.getElementById("modelo");
    const marcaInput = document.getElementById("marca");
    const logoInput = document.getElementById("logo");
    const inputFalla = document.getElementById("falla");
    const dataListFallas = document.getElementById("fallas-list");

    // 🟢 Mostrar el formulario al hacer clic en "Solicitar nuevo servicio"
    if (solicitarServicioBtn && formContainer) {
        solicitarServicioBtn.addEventListener("click", function () {
            formContainer.style.display = "block";
            solicitarServicioBtn.style.display = "none";
        });
    }

    // 🟢 Cerrar formulario
    if (closeFormArrow) {
        closeFormArrow.addEventListener("click", function () {
            formContainer.style.display = "none"; 
            solicitarServicioBtn.style.display = "block";
        });
    }

    // 🟢 Generar fecha de solicitud automática
    const fechaActual = new Date().toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
    const fechaSolicitudInput = document.getElementById("fechaSolicitud");
    if (fechaSolicitudInput) fechaSolicitudInput.value = fechaActual;

    // 🟢 Detectar cambio en el input de "modelo" para buscar datos
    if (modeloInput) {
        modeloInput.addEventListener("change", function () {
            const modelo = modeloInput.value.trim();
            if (modelo === "") return;

            console.log("Ejecutando fetch con modelo:", modelo);
            fetch(`/auth/getEquipo?modelo=${modelo}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        console.error("Error:", data.error);
                        Swal.fire({
                            icon: 'error',
                            title: 'Error',
                            text: 'No se encontró el modelo solicitado. Por favor, verifica la información e intenta nuevamente.',
                        });
                        marcaInput.value = "";
                        logoInput.value = "";
                        fileNameSpan.textContent = "Ningún archivo seleccionado";
                    } else {
                        console.log("Datos recibidos:", data);
                        marcaInput.value = data.marca;
                        logoInput.value = data.logo || ""; // Evitar que sea undefined
                        fileNameSpan.textContent = data.logo || "Ningún archivo seleccionado";
                    }
                }) 
                .catch(error => console.error("Error al obtener el equipo:", error));
        });
    }

    // Cargar fallas en el datalist al hacer clic en el input
    if (inputFalla && dataListFallas) {
        // Cargar las fallas al hacer clic en el input
        inputFalla.addEventListener("focus", function () {
            if (dataListFallas.children.length === 0) { // Solo cargar si no hay opciones ya cargadas
                fetch('/auth/getTiposFalla', {
                    method: 'GET',
                    credentials: 'include' // Para enviar cookies de sesión
                })
                .then(response => response.json())
                .then(fallas => {
                    dataListFallas.innerHTML = ''; // Limpiar opciones anteriores

                    fallas.forEach(falla => {
                        const option = document.createElement("option");
                        option.value = `${falla.tipo} = ${falla.descripcion}`;
                        dataListFallas.appendChild(option);
                    });

                    // Forzar la visualización del datalist
                    inputFalla.setAttribute("list", "fallas-list");
                    inputFalla.focus(); // Forzar el focus nuevamente para mostrar el datalist
                })
                .catch(error => console.error("Error al obtener las fallas:", error));
            }
        });
    }

    // 🟢 Cargar imágenes desde el servidor para logos
    const logoSelect = document.getElementById("logo-select");
    const preview = document.getElementById("preview");
    if (logoSelect) {
        fetch("/auth/getLogos")
            .then(response => response.json())
            .then(logos => {
                logos.forEach(logo => {
                    const option = document.createElement("option");
                    option.value = `/uploads/logos/${logo}`;
                    option.textContent = logo;
                    logoSelect.appendChild(option);
                });
            })
            .catch(error => console.error("Error cargando los logos:", error));

        logoSelect.addEventListener("change", function () {
            const selectedLogo = this.value;
            if (selectedLogo) {
                preview.src = selectedLogo;
                preview.style.display = "block";
            } else {
                preview.style.display = "none";
            }
        });
    }

    // 🟢 Manejar el envío del formulario con mensaje de carga
    if (solicitudForm) {
        solicitudForm.addEventListener("submit", function (event) {
            event.preventDefault();

            solicitudForm.style.display = "none";
            loadingMessage.style.display = "block";

            setTimeout(function () {
                loadingMessage.style.display = "none";
                solicitudForm.style.display = "block";
                solicitudForm.reset();
                fileNameSpan.textContent = "Ningún archivo seleccionado";
                formContainer.style.display = "none";
                solicitarServicioBtn.style.display = "block";
            }, 1000);
        });
    }
});


























/* document.addEventListener("DOMContentLoaded", function() {
    // Cargar imágenes desde el servidor
    fetch("/getLogos")
    .then(response => response.json())
    .then(logos => {
        const select = document.getElementById("logo-select");
        logos.forEach(logo => {
            const option = document.createElement("option");
            option.value = `/uploads/logos/${logo}`;  // Ruta de la imagen
            option.textContent = logo;
            select.appendChild(option);
        });
    })
    .catch(error => console.error("Error cargando los logos:", error));

    // Mostrar vista previa al seleccionar un logo
    document.getElementById("logo-select").addEventListener("change", function() {
        const selectedLogo = this.value;
        if (selectedLogo) {
            document.getElementById("preview").src = selectedLogo;
            document.getElementById("preview").style.display = "block";
        } else {
            document.getElementById("preview").style.display = "none";
        }
    });
}); */







 /* // Manejar el envío del formulario
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
        
    }); */