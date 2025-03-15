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
    const logoPreview = document.getElementById("logoPreview"); // Elemento img para el logo
    const inputTipoFalla = document.getElementById('tipoFalla');
    const optionsList = document.getElementById('tipoFalla-list');
    const selectWrapper = document.querySelector('#tipoFalla-container .select-wrapper'); // Selecciona el select-wrapper dentro del contenedor correcto


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
                        logoPreview.style.display = "none"; // Oculta la imagen si hay error
                    } else {
                        console.log("Datos recibidos:", data);
                        marcaInput.value = data.marca;
                        if (data.logo) {
                            logoPreview.src = data.logo;
                            logoPreview.style.display = "block"; // Muestra la imagen si hay logo
                        } else {
                            logoPreview.style.display = "none"; // Oculta la imagen si no hay logo
                        }
                    }
                }) 
                .catch(error => console.error("Error al obtener el equipo:", error));
        });
    }

            // Carga las opciones desde el servidor
        fetch("/auth/getTiposFalla")
        .then(response => response.json())
        .then(data => {
            // Limpia la lista antes de agregar las nuevas opciones
            optionsList.innerHTML = "";

            // Agrega las opciones a la lista
            data.forEach(tipo => {
                let option = document.createElement("li");
                option.textContent = tipo.tipo;
                optionsList.appendChild(option);
            });

            // Agrega event listeners a las opciones
            optionsList.querySelectorAll('li').forEach(option => {
                option.addEventListener('click', () => {
                    inputTipoFalla.value = option.textContent;
                    optionsList.style.display = 'none'; // Cierra la lista
                });
            });
        })
        .catch(error => {
            console.error("Error al cargar tipos de falla:", error);
            inputTipoFalla.placeholder = "Error al cargar las opciones";
        });

        // Muestra/oculta la lista al hacer clic en el input
        inputTipoFalla.addEventListener('click', () => {
        optionsList.style.display = optionsList.style.display === 'block' ? 'none' : 'block';
        });

        // Cierra la lista si se hace clic fuera del select-wrapper
        document.addEventListener('click', (event) => {
        if (!selectWrapper.contains(event.target)) {
            optionsList.style.display = 'none';
        }
        });



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