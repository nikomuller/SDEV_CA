export interface Message {
    // -- Properties
    status: 'success' | 'error';
    message: string;
}