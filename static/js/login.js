// static/js/login.js

document.addEventListener('DOMContentLoaded', () => {
    const pwdField = document.getElementById('password');
    const toggleBtn = document.getElementById('togglePassword');
    if (!pwdField || !toggleBtn) return;

    const openIcon = toggleBtn.querySelector('.toggle-open');
    const closeIcon = toggleBtn.querySelector('.toggle-close');

    toggleBtn.addEventListener('click', () => {
        const isPwd = pwdField.type === 'password';
        // alterna tipo
        pwdField.type = isPwd ? 'text' : 'password';
        // alterna iconos
        openIcon.classList.toggle('hidden');
        closeIcon.classList.toggle('hidden');
    });
});