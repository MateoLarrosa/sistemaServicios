document.addEventListener('DOMContentLoaded', () => {
    const sidebar = document.querySelector('.sidebar');
    const toggleBtn = document.querySelector('.menu-toggle-btn');
    const closeBtn = document.querySelector('.close-btn');
    const mainContent = document.querySelector('.main-content');

    toggleBtn.addEventListener('click', () => {
        sidebar.style.left = sidebar.style.left === '0px' ? '-250px' : '0px';
        mainContent.classList.toggle('open');
    });

    closeBtn.addEventListener('click', () => {
        sidebar.style.left = '-250px';
        mainContent.classList.remove('open');
    });
});