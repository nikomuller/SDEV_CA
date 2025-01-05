// -- Imports
import { 
    Product,
    SingleButton,
    MultipleButtons
} from './index.d';

const prod_container = document.getElementById('products-container') as HTMLDivElement,
    cont_children = Array.from(prod_container.children) as HTMLDivElement[],
    root_url = location.protocol + '//' + location.host;

let products: Product[] = [];

// -- Loop through each product
cont_children.forEach((child) => {
    const name = child.getAttribute('aria-product') as string,
        id = child.getAttribute('aria-id') as string,
        price = Number(child.getAttribute('aria-price')),
        max_qant = Number(child.getAttribute('aria-max-qant')),
        type = child.getAttribute('aria-type') as string,
        csrf = child.getAttribute('aria-csrf') as string,
        qty = Number(child.getAttribute('aria-qty')),
        endpoint = child.getAttribute('aria-endpoint') as string,
        buttons_elm = child.querySelector('.buttons') as HTMLDivElement;

    // - Check what type of buttons we're dealing with
    const buttons = (): SingleButton | MultipleButtons | undefined => {

        // -- Single button
        if (type === 'single')
            return buttons_elm.querySelector('[aria-btn="modify"]') as SingleButton;
        

        // -- Multiple buttons
        else if (type === 'multiple') {
            // -- Get buttons, aria-minus, aria-plus and aria-counter
            const decrement = buttons_elm.querySelector('[aria-btn="minus"]') as HTMLButtonElement,
                increment = buttons_elm.querySelector('[aria-btn="plus"]') as HTMLButtonElement,
                counter = buttons_elm.querySelector('[aria-btn="counter"]') as HTMLInputElement;
            

            // -- Remove the max attribute
            // since there is an unlimited 
            // amount of items  
            if (max_qant == 0)
                counter.max = '9999999';
            
            

            // -- Return buttons
            return {
                decrement,
                increment,
                counter
            } as MultipleButtons;
        }
    }

    // -- Create product object
    const product: Product = {
        name: name,
        id: id,
        csrf_token: csrf,
        price: price,
        qty: qty,
        endpoint: endpoint,
        type: type as 'single' | 'multiple',
        max_qant: max_qant,
        buttons: buttons() as SingleButton | MultipleButtons
    };

    // -- Push product to products array
    products.push(product);
});



function request(
    endpoint: string, 
    method: string,
    headers: any = null,
    data: any = null
): Promise<any> {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();

        xhr.open(method, root_url + endpoint);
        
        // -- Set headers
        if (headers) for (const key in headers) {
            xhr.setRequestHeader(key, headers[key]);
        }

        // -- Set data type
        xhr.setRequestHeader(
            'Content-Type', 
            'application/json'
        );
        

        xhr.onload = () => {
            if (xhr.status >= 200 && xhr.status < 300)
                resolve(xhr.response);
            else reject(xhr.statusText);
        };

        xhr.onerror = () => reject(xhr.statusText);
        xhr.send(JSON.stringify(data));
    });
}


function update_cart(
    product: Product,
    quantity: number
): Promise<any> {
    return request(product.endpoint, 'POST', 
        { 
            'X-CSRFToken': product.csrf_token 
        },
        { 
            'quantity': quantity,
            'pid': product.id
        }
    );
}



// -- Add event listeners to buttons
products.forEach((product) => {
    switch (product.type) {
        case 'single':
            const button = product.buttons as SingleButton;
            button.addEventListener('click', async() => {
                
                // -- Toggle button text
                const state = (
                    button.getAttribute('btn-state') as 
                    'not_in_cart' | 'in_cart'
                ).trim();

                // -- not_in_cart || in_cart
                switch (state) {
                    case 'not_in_cart':
                        button.setAttribute('btn-state', 'in_cart');
                        button.innerText = 'Remove from cart';
                        return await update_cart(product, 1);


                    case 'in_cart':
                        button.setAttribute('btn-state', 'not_in_cart');
                        button.innerText = 'Add to cart';
                        return await update_cart(product, 0);
                }
            });
        break;


        case 'multiple':
            const buttons = product.buttons as MultipleButtons;
            
            buttons.decrement.addEventListener('click', () => {
                if (buttons.counter.value == '0') return;

                buttons.counter.value = String(
                    Number(buttons.counter.value) - 1
                );

                product.qty = Number(buttons.counter.value);
                update_cart(product, product.qty);


                // -- If the quantity is 0, change the button state
                if (buttons.counter.value == '0') 
                    buttons.decrement.classList.add('disabled');
                
            });


            buttons.increment.addEventListener('click', () => {
                // 
                // If the product has a max quantity
                // and the product has a max quantity
                //
                if (
                    buttons.counter.value == product.max_qant.toString()
                    && product.max_qant != 0
                ) return;

                buttons.counter.value = String(
                    Number(buttons.counter.value) + 1
                );

                product.qty = Number(buttons.counter.value);
                update_cart(product, product.qty);


                // -- If the quantity is 0, change the button state
                // so that the user can't decrement the quantity
                if (buttons.counter.value != '0')
                    buttons.decrement.classList.remove('disabled');

                if (product.qty >= product.max_qant
                    && product.max_qant != 0
                ) buttons.increment.classList.add('disabled');
            });

            buttons.counter.addEventListener('change', () => {
                product.qty = Number(buttons.counter.value);
                update_cart(product, product.qty);
            });

        break;
    }
});