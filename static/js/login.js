document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');
    const logo = document.querySelector('.logo');
    const submitButton = document.querySelector('.btn-primary');
    const verServiciosBtn = document.getElementById('verServiciosBtn');

    // Función para mostrar mensajes de error
    const showError = (message) => {
        errorMessage.textContent = message;
        errorMessage.style.display = "block";
    };

    // Función para limpiar los campos del formulario
    const clearFormFields = () => {
        document.getElementById('email').value = "";
        document.getElementById('password').value = "";
    };

    loginForm.addEventListener('submit', async (event) => {
        event.preventDefault(); // Evita la recarga de la página

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        // Validación básica
        if (!email || !password) {
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
                body: JSON.stringify({ email, password }),
            });

            // **Aplica el setTimeout() en todos los casos**
            setTimeout(async () => {
                logo.classList.remove('loading');
                submitButton.classList.remove('loading');
                submitButton.disabled = false;

                if (response.ok) {
                    clearFormFields();
                    window.location.href = "/auth/inicioAdmin";
                } else {
                    const data = await response.json();
                    showError(data.error || "Credenciales inválidas. Inténtalo de nuevo.");
                }
            }, 2500); // Retraso de 2.5 segundos
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
    document.getElementById('email').addEventListener('input', () => {
        errorMessage.style.display = "none";
    });

    document.getElementById('password').addEventListener('input', () => {
        errorMessage.style.display = "none";
    });
});
