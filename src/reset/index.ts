import { Message } from "./index.d";


// -- Main element
const reset_form = document.getElementById('reset-form') as HTMLDivElement;

// -- Data
const endpoint = reset_form.getAttribute('aria-endpoint') as string,
    csrf_token = reset_form.getAttribute('aria-csrf-token') as string,
    redirect = reset_form.getAttribute('aria-redirect') as string;

// -- Popups 
const err_popup = document.getElementById('msg-warn'),
    suc_popup = document.getElementById('msg-suc');

const old_password = reset_form.querySelector('#old_password') as HTMLInputElement,
    new_password = reset_form.querySelector('#new_password') as HTMLInputElement,
    new_password2 = reset_form.querySelector('#new_password2') as HTMLInputElement,
    btn = reset_form.querySelector('#reset-btn') as HTMLButtonElement;



// -- Reset
btn.addEventListener('click', () => {
    // -- Get data
    const data = {
        old_password: old_password.value,
        new_password: new_password.value,
        new_password2: new_password2.value,
    };

    // -- Send request
    fetch(endpoint, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then((res: Message) => {
        switch (res.status) {
            case 'success':
                create_alert(res.message, 'success');
                break;

            case 'error':
                create_alert(res.message, 'error');
                break;
        }
    });
});


// -- Popup (bootstrap5)
function create_alert(
    message: string,
    type: 'success' | 'error'
) {
    switch (type) {
        case 'success':
            suc_popup.style.display = 'block';
            err_popup.style.display = 'none';

            suc_popup.querySelector('.alert').innerHTML = message;
            
            setTimeout(() => {
                window.location.href = redirect;
            }, 2000);
            break;
        
        case 'error':
            suc_popup.style.display = 'none';
            err_popup.style.display = 'block';

            err_popup.querySelector('.alert').innerHTML = message;
            break;
    }
}

export { Message };
