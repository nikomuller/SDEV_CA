import { Message } from './index.d';

// -- Main element
const login_form = document.getElementById('login-form');


// -- Data
const endpoint = login_form.getAttribute('aria-endpoint') as string,
    csrf_token = login_form.getAttribute('aria-csrf-token') as string,
    redirect = login_form.getAttribute('aria-redirect') as string;

// -- Elements
const username = login_form.querySelector('#username') as HTMLInputElement,
    email = login_form.querySelector('#email') as HTMLInputElement,
    pass = login_form.querySelector('#password') as HTMLInputElement,
    pass2 = login_form.querySelector('#password2') as HTMLInputElement,
    btn = login_form.querySelector('#login-btn') as HTMLButtonElement;



// -- Popups 
const err_popup = document.getElementById('msg-warn'),
    suc_popup = document.getElementById('msg-suc');


// -- Login
btn.addEventListener('click', () => {
    // -- Get data
    const data = {
        username: username.value,
        email: email.value,
        password: pass.value,
        password2: pass2.value,
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
