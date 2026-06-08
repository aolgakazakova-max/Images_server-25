document.addEventListener('DOMContentLoaded', () => {

    const uploadTabBtn =
        document.getElementById(
            'upload-tab-btn'
        );

    const imagesTabBtn =
        document.getElementById(
            'images-tab-btn'
        );

    if (uploadTabBtn) {

        uploadTabBtn.addEventListener(
            'click',
            () => {

                window.location.href =
                    '/upload';
            }
        );
    }

    if (imagesTabBtn) {

        imagesTabBtn.addEventListener(
            'click',
            () => {

                window.location.href =
                    '/images-list';
            }
        );
    }

    document.addEventListener(
        'keydown',
        (e) => {

            if (e.key === 'Escape') {

                window.location.href =
                    '/upload';
            }
        }
    );

    document
        .querySelectorAll('.copy-btn')
        .forEach(btn => {

            btn.addEventListener(
                'click',
                async (e) => {

                    const url =
                        e.currentTarget
                            .dataset.url;

                    try {

                        await navigator
                            .clipboard
                            .writeText(url);

                        const oldText =
                            e.currentTarget
                                .textContent;

                        e.currentTarget
                            .textContent =
                            'COPIED';

                        setTimeout(() => {

                            e.currentTarget
                                .textContent =
                                oldText;

                        }, 1200);

                    } catch (err) {

                        console.error(
                            'Copy failed:',
                            err
                        );
                    }
                }
            );
        });
});