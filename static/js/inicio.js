if (verServiciosBtn) {
    verServiciosBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Evita que siga el href por defecto
        window.location.href = "/auth/misServicios"; // Redirige a la URL deseada
    });
}

if (verClientesBtn) {
    verClientesBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Evita que siga el href por defecto
        window.location.href = "/auth/gestionDeClientes"; // Redirige a la URL deseada
    }); 
}

if (verTecnicosBtn) {
    verTecnicosBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Evita que siga el href por defecto
        window.location.href = "/auth/gestionDeTecnicos"; // Redirige a la URL deseada
    }); 
}


if (solicitarServicioBtn) {
    solicitarServicioBtn.addEventListener('click', (event) => {
        event.preventDefault(); // Evita que siga el href por defecto
        window.location.href = "/auth/solicitudServicio"; // Redirige a la URL deseada
    }); 
}