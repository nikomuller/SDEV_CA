export type SingleButton = HTMLButtonElement;
export type MultipleButtons = {
    decrement: HTMLButtonElement;
    counter: HTMLInputElement;
    increment: HTMLButtonElement;
};


export interface Product {
    // -- Properties
    name: string;
    id: string;
    price: number;
    max_qant: number;
    endpoint: string;
    csrf_token: string;
    qty: number;
    type: 'single' | 'multiple';
    
    // -- Elements
    buttons: SingleButton | MultipleButtons;

    // -- Methods
}