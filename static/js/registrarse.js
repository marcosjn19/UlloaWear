// static/js/register.js
document.addEventListener('DOMContentLoaded', () => {
    function hookToggle(inputId, btnId) {
        const field = document.getElementById(inputId);
        const btn = document.getElementById(btnId);
        if (!field || !btn) return null;
        const openIc = btn.querySelector('.open-icon');
        const closeIc = btn.querySelector('.close-icon');
        btn.addEventListener('click', () => {
            const isPwd = field.type === 'password';
            field.type = isPwd ? 'text' : 'password';
            openIc.classList.toggle('hidden');
            closeIc.classList.toggle('hidden');
        });
        return field;
    }

    const pass1 = hookToggle('id_contraseña', 'togglePass1');
    const pass2 = hookToggle('id_confirmar_contraseña', 'togglePass2');
    const msg = document.getElementById('matchMsg');

    if (pass1 && pass2 && msg) {
        const check = () => {
            if (!pass2.value) {
                msg.textContent = '';
            } else if (pass1.value === pass2.value) {
                msg.textContent = '✔ Las contraseñas coinciden';
                msg.className = 'h-5 mt-2 text-sm text-green-600';
            } else {
                msg.textContent = '✖ Las contraseñas NO coinciden';
                msg.className = 'h-5 mt-2 text-sm text-red-600';
            }
        };
        pass1.addEventListener('input', check);
        pass2.addEventListener('input', check);
    }

});