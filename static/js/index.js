document.addEventListener(
    'DOMContentLoaded',
    () => {

        document.body.style.backgroundColor =
            '#151515';

        const heroBlocks =
            document.querySelectorAll(
                '.hero__img'
            );

        if (heroBlocks.length > 0) {

            const randomIndex =
                Math.floor(
                    Math.random() *
                    heroBlocks.length
                );

            heroBlocks[randomIndex]
                .classList
                .add('is-visible');
        }

        const showcaseButton =
            document.querySelector(
                '.header__button-btn'
            );

        if (showcaseButton) {

            showcaseButton.addEventListener(
                'click',
                () => {

                    window.location.href =
                        '/upload';
                }
            );
        }
    }
);

