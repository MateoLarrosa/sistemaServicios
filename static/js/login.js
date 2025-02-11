// document.addEventListener('DOMContentLoaded', () => {
//     const loginForm = document.getElementById('loginForm');
//     const errorMessage = document.getElementById('errorMessage');

//     loginForm.addEventListener('submit', async (event) => {
//         event.preventDefault(); // Prevenir recarga de la página

//         const email = document.getElementById('email').value;
//         const password = document.getElementById('password').value;

//         try {
//             const response = await fetch('/auth/login', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({ email, password }),
//             });

//             const data = await response.json();

//             if (response.ok) {
//                 // Redirigir al usuario a la página de inicio
//                 window.location.href = "/auth/inicio";
//             } else {
//                 // Mostrar mensaje de error
//                 errorMessage.textContent = data.error || "Credenciales inválidas. Inténtalo de nuevo.";
//                 errorMessage.style.display = "block";
//             }
//         } catch (error) {
//             console.error('Error en el inicio de sesión:', error);
//             errorMessage.textContent = "Ocurrió un error al intentar iniciar sesión.";
//             errorMessage.style.display = "block";
            
//         }
//     });
// });

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('loginForm');
    const errorMessage = document.getElementById('errorMessage');

    // Función para mostrar mensajes de error de forma dinámica
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
        event.preventDefault(); // Prevenir recarga de la página

        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value.trim();

        // Validación básica del cliente
        if (!email || !password) {
            showError("Por favor, completa todos los campos.");
            return;
        }

        try {
            // Enviar los datos al servidor
            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ email, password }),
            });

            if (response.ok) {
                // Redirigir al usuario y limpiar los campos
                clearFormFields();
                window.location.href = "/auth/inicio";
            } else {
                // Mostrar el mensaje de error proporcionado por el servidor
                const data = await response.json();
                showError(data.error || "Credenciales inválidas. Inténtalo de nuevo.");
            }
        } catch (error) {
            console.error('Error en el inicio de sesión:', error);
            showError("Ocurrió un error inesperado. Por favor, intenta más tarde.");
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

