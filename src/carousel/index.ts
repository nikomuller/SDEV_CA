import { Image } from './index.d';

const class_name = 'game-carousel',
    carousels = document.querySelectorAll(`.${class_name}`);

function move_elm_to(image: Image, index: number) {
    // -- Move the element to the index provied
    // in the dom
    let parent = image.main_elm.parentElement;

    // -- Get the element at the index
    let elm = parent.children[index];

    // -- Move the element
    parent.insertBefore(image.main_elm, elm);
}

// -- Loop through each carousel
carousels.forEach((carousel) => {
    
    let image_arr: Array<Image> = [];

    const loop_every = parseInt(carousel.getAttribute('data-loop-every')) || 5000,
        anim_time = parseInt(carousel.getAttribute('data-anim-time')) || 750,
        max_images = parseInt(carousel.getAttribute('data-max-images')) || 4;

    // -- Loop through each image
    carousel.querySelectorAll('.item').forEach((item, i) => {
        // -- We know that the elm is a SPAN
        let elm = item as HTMLSpanElement,
            image_elm = elm.querySelector('.carousel_image') as HTMLDivElement,
            image: Image = {
                id: i,
                name: item.getAttribute('name-attr'),
                url: item.getAttribute('image-attr'),
                alt: item.getAttribute('image-alt'),
                django_url: item.getAttribute('django-url'),
    
                main_elm: elm,
                image_elm,
                visible: false,
                
                set_visibility: (visible: boolean) => {
                    elm.style.opacity = visible ? '1' : '0';
                    elm.style.display = visible ? 'block' : 'none';
                    image.visible = visible;
                },

                set_animation: (animation: string) => {
                    // -- Annimation will be an attribute
                    // of the main element
                    elm.setAttribute('animation', animation);

                    // -- Sleep for 750 ms
                    return sleep(anim_time).then(() => {
                        // -- Remove the attribute
                        elm.removeAttribute('animation');
                    });
                },

                set_absolute: (absolute: boolean) => {
                    // -- Set the element to be absolute
                    // or relative
                    elm.style.position = absolute ? 'absolute' : 'relative';
                }
            };

        // -- Create a new Image object
        // and push it to the array
        image_arr.push(image);

        // -- We need to add the image as a background
        // to the span element
        image_elm.style.backgroundImage = `url(${image.url})`;

        // -- Add the click event
        elm.addEventListener('click', () => {
            // -- Redirect to the django url
            window.location.href = image.django_url;
        });

        // -- Add an index attribute to the element
        elm.setAttribute('index', i.toString());

        // -- Set the visibility to false
        image.set_visibility(false);
    });
    

    // -- Get the controll buttons
    let left_btn = carousel.querySelector('.btn_left') as HTMLButtonElement,
        right_btn = carousel.querySelector('.btn_right') as HTMLButtonElement;

    
    //                                   //
    // State management for the carousel //
    //                                   //

    
    let visible: Array<Image> = [],
        running = false;

    const animations = {
        in: {
            left: 'in',
            right: 'in'
        },

        out: {
            left: 'out',
            right: 'out'
        }
    };


    // -- Loop trough the first DISP_MAX images
    // and set them to visible
    for (let i = 0; i < max_images; i++) {
        let image = image_arr[i];
        visible.push(image);
        image.set_visibility(true);
    }

    function index_after(index: number) {
        // -- Get the index after the index provied
        let new_index = index + 1;

        if (new_index >= image_arr.length - 1)
            return 0;
        
        return new_index;
    }

    function index_before(index: number) {
        // -- Get the index before the index provied
        let new_index = index - 1;

        if (new_index <= 0)
            return image_arr.length - 1;

        return new_index;
    }
    
    const set_cur = async(
        mode: 'next' | 'prev'
    ) => {
        // -- Wait for anitmations to finish
        if (running) return;

        let to_remove: Image = image_arr[0],
            to_add: Image = image_arr[0],

            to_add_animation: string = '',
            to_remove_animation: string = '';

        switch (mode) {
            case 'prev': {
                // -- GOING RIGHT -- //

                let index = index_before(visible[0].id);
                to_add = image_arr[index];
                visible.unshift(to_add);

                // -- Remove the last image
                to_remove = visible.pop();

                // -- Set the animation
                to_add_animation = animations.in.right;
                to_remove_animation = animations.out.right;
                break;
            };

            case 'next': {
                // -- GOING LEFT -- //
                
                let index = index_after(visible[visible.length - 1].id);
                to_add = image_arr[index];
                visible.push(to_add);

                // -- Remove the first image
                to_remove = visible.shift();

                // -- Set the animation
                to_add_animation = animations.in.left;
                to_remove_animation = animations.out.left;
                break;
            };
        }

        // -- Set the running state to true
        running = true;


        await to_remove.set_animation(to_remove_animation);
        to_remove.set_visibility(false);

        // -- Loop through the visible images
        // and set the visibility to true
        visible.forEach((image, i) => {
            move_elm_to(image, i);
            image.set_visibility(true);
        });

        // -- Set the animations
        await to_add.set_animation(to_add_animation);

        
        // -- Set the running state to false
        running = false;
    }

    set_cur('prev');



    left_btn.addEventListener('click', () => {
        // -- Go to the previous image
        set_cur('next');
    });

    right_btn.addEventListener('click', () => {
        // -- Go to the next image
        set_cur('prev');
    });


    // -- Loop every 3 seconds
    setInterval(() => {
        set_cur('prev');
    }, loop_every);
});

async function sleep(ms: number) {
    return new Promise(resolve => setTimeout(resolve, ms));
}