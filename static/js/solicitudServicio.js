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

    // Generar fecha de solicitud automática
    const fechaActual = new Date().toLocaleDateString('es-ES', {day: '2-digit', month: '2-digit', year: 'numeric'});
    document.getElementById("fechaSolicitud").value = fechaActual;

    fileInput.addEventListener("change", function () {
        fileNameSpan.textContent = fileInput.files.length > 0 ? fileInput.files[0].name : "Ningún archivo seleccionado";
    });

    /* document.getElementById("logo").addEventListener("change", function () {
        let fileName = this.files[0] ? this.files[0].name : "Ningún archivo seleccionado";
        document.getElementById("file-name").textContent = fileName;
    }); */
    
    closeFormArrow.addEventListener("click", function () {
    formContainer.style.display = "none"; // Oculta el formulario
    solicitarServicioBtn.style.display = "block"; // Muestra el botón "Solicitar nuevo servicio"
});
});


document.addEventListener("DOMContentLoaded", function () {
    const modeloInput = document.getElementById("modelo");
    const marcaInput = document.getElementById("marca");
    const logoInput = document.getElementById("logo");

    modeloInput.addEventListener("change", function () {
        const modelo = modeloInput.value;

        if (modelo.trim() === "") return;
        console.log("Ejecutando fetch con modelo:", modelo);
        fetch(`http://127.0.0.1:5000/auth/getEquipo?modelo=${modelo}`)
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
                    document.getElementById("file-name").textContent = "Ningún archivo seleccionado";
                } else {
                    console.log("Datos recibidos:", data); // Para ver si llega respuesta del backend
                    marcaInput.value = data.marca;
                    logoInput.value = data.logo; // Si el logo es NULL, vendrá con la imagen por defecto
                    document.getElementById("file-name").textContent = data.logo;
                }
            })
            .catch(error => console.error("Error al obtener el equipo:", error));
    });
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