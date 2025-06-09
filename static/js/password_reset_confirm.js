// static/js/password_reset_confirm.js

document.addEventListener('DOMContentLoaded', () => {
    function setupToggle(fieldId, btnId) {
        const field = document.getElementById(fieldId);
        const btn = document.getElementById(btnId);
        if (!field || !btn) return;
        const openIcon = btn.querySelector('.toggle-open');
        const closeIcon = btn.querySelector('.toggle-close');
        btn.addEventListener('click', () => {
            const isPwd = field.type === 'password';
            field.type = isPwd ? 'text' : 'password';
            openIcon.classList.toggle('hidden');
            closeIcon.classList.toggle('hidden');
        });
        return field;
    }

    // enlazamos toggles
    const field1 = setupToggle('id_new_password1', 'toggleNew1');
    const field2 = setupToggle('id_new_password2', 'toggleNew2');
    const msg = document.getElementById('matchMessage');

    if (field1 && field2 && msg) {
        const checkMatch = () => {
            if (!field2.value) {
                msg.textContent = '';
            } else if (field1.value === field2.value) {
                msg.textContent = '✔ Las contraseñas coinciden';
                msg.className = 'mt-2 text-sm text-green-600';
            } else {
                msg.textContent = '✖ Las contraseñas no coinciden';
                msg.className = 'mt-2 text-sm text-red-600';
            }
        };
        field1.addEventListener('input', checkMatch);
        field2.addEventListener('input', checkMatch);
    }
});