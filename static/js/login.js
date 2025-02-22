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

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Evita la recarga de la página

        const nombreUsuario = document.getElementById('nombreUsuario').value.trim();
        const password = document.getElementById('password').value.trim();

        // Validación básica
        if (!nombreUsuario || !password) {
            showError("Por favor, completa todos los campos.");
            return;
        }

        // Inicia el efecto de carga
        logo.classList.add('loading');
        submitButton.classList.add('loading');
        submitButton.disabled = true;

        try {
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ nombreUsuario, password }), // ✅ Enviar nombreUsuario en lugar de email
            });

            // **Aplica el setTimeout() en todos los casos**
            setTimeout(async () => {
                logo.classList.remove('loading');
                submitButton.classList.remove('loading');
                submitButton.disabled = false;
                const data = await response.json();
                if (response.ok) {
                    clearFormFields();
                    sessionStorage.setItem("token", data.token); // Guardar token en sessionStorage
                    window.location.href = "/auth/inicio";
                } else {
                    /* const data = await response.json(); */
                    showError(data.error || "Credenciales inválidas. Inténtalo de nuevo.");
                }
            }, 1500); // Retraso de 1.5 segundos
        } catch (error) {
            console.error('Error en el inicio de sesión:', error);
            setTimeout(() => {
                showError("Ocurrió un error inesperado. Por favor, intenta más tarde.");
                logo.classList.remove('loading');
                submitButton.classList.remove('loading');
                submitButton.disabled = false;
            }, 2500); // Retraso de 2.5 segundos también en caso de error
        }
    });

    // Limpia el mensaje de error cuando se empieza a escribir en los campos
    document.getElementById('nombreUsuario').addEventListener('input', () => {
        errorMessage.style.display = "none";
    });

    document.getElementById('password').addEventListener('input', () => {
        errorMessage.style.display = "none";
    });
});
