/* document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const logo = document.querySelector('.logo');
    const submitButton = document.querySelector('.btn-primary');

    // Función para mostrar mensajes de error
    const showError = (message) => {
        errorMessage.textContent = message;
        errorMessage.style.display = "block";
    };

    // Función para limpiar los campos del formulario
    const clearFormFields = () => {
        document.getElementById('nombreUsuario').value = "";
        document.getElementById('password').value = "";
    };

    // Función para manejar el efecto del logo titilando
    const startLogoEffect = () => {
        logo.classList.add('loading');
        setTimeout(() => {
            logo.classList.remove('loading');
        }, 1500); // El logo titila durante 1.5 segundos
    };

    // Validación básica en el formulario de inicio de sesión
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita la recarga de la página

        const nombreUsuario = document.getElementById('nombreUsuario').value.trim();
        const password = document.getElementById('password').value.trim();

        // Validación básica de los campos
        if (!nombreUsuario || !password) {
            showError("Por favor, completa todos los campos.");
            startLogoEffect(); // Llama a la función para hacer titilar el logo
            return;
        }

        // Deshabilitar el botón de enviar para evitar múltiples envíos
        submitButton.disabled = true;
        submitButton.classList.add('loading');

        // Enviar el formulario de manera tradicional
        loginForm.submit();
    });

    // Manejar mensajes de error desde el backend
    const urlParams = new URLSearchParams(window.location.search);
    const error = urlParams.get('error');

    if (error) {
        showError(error); // Mostrar el mensaje de error si existe
        startLogoEffect(); // Hacer titilar el logo si hay un error
    }
}); */


document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const logo = document.querySelector('.logo');
    const submitButton = document.querySelector('.btn-primary');

    // Función para mostrar mensajes de error
    const showError = (message) => {
        errorMessage.textContent = message;
        errorMessage.style.display = "block";
    };

    // Función para limpiar los campos del formulario
    const clearFormFields = () => {
        document.getElementById('nombreUsuario').value = "";
        document.getElementById('password').value = "";
    };

    // Función para manejar el efecto del logo titilando
    const startLogoEffect = () => {
        logo.classList.add('loading');
        setTimeout(() => {
            logo.classList.remove('loading');
        }, 1500); // El logo titila durante 1.5 segundos
    };

    // Validación básica en el formulario de inicio de sesión
    loginForm.addEventListener('submit', (event) => {
        event.preventDefault(); // Evita la recarga de la página

        const nombreUsuario = document.getElementById('nombreUsuario').value.trim();
        const password = document.getElementById('password').value.trim();

        // Validación básica de los campos
        if (!nombreUsuario || !password) {
            showError("Por favor, completa todos los campos.");
            startLogoEffect(); // Llama a la función para hacer titilar el logo
            return;
        }

        // Deshabilitar el botón de enviar para evitar múltiples envíos
        submitButton.disabled = true;
        submitButton.classList.add('loading');

        // Simular el envío del formulario (el backend de Flask se encargará de la redirección)
        fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                nombreUsuario: nombreUsuario,
                password: password
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                // Si hay un error, mostrar el mensaje de error en la interfaz
                showError(data.error);
                startLogoEffect();
            }
        })
        .catch(error => {
            showError("Error de conexión. Por favor, intenta nuevamente.");
            startLogoEffect();
        })
        .finally(() => {
            // Rehabilitar el botón de enviar
            submitButton.disabled = false;
            submitButton.classList.remove('loading');
        });
    });



});