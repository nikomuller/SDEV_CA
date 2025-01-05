export interface Image {
    // -- Properties
    name: string;
    url: string;
    alt: string;
    visible: boolean;
    django_url: string;

    main_elm: HTMLElement;
    image_elm: HTMLDivElement;
    id: number;
    
    // -- Methods
    set_visibility(visible: boolean): void;
    set_animation(animation: string): Promise<void>;
    set_absolute(absoulute: boolean): void;
}