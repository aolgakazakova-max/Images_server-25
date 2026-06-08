document.addEventListener('DOMContentLoaded', () => {

    const fileUpload = document.getElementById('file-upload');
    const dropzone = document.querySelector('.upload__dropzone');
    const currentUploadInput = document.querySelector('.upload__input');
    const copyButton = document.querySelector('.upload__copy');
    const imagesButton = document.getElementById('images-tab-btn');
    const uploadButton = document.getElementById('upload-tab-btn');

    // NAVIGATION

    if (imagesButton) {
        imagesButton.addEventListener('click', () => {
            window.location.href = '/images-list';
        });
    }

    if (uploadButton) {
        uploadButton.addEventListener('click', () => {
            window.location.href = '/upload';
        });
    }

    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            window.location.href = '/';
        }
    });

    // VALIDATION

    const isValidFile = (file) => {

        const allowedTypes = [
            'image/jpeg',
            'image/png',
            'image/gif'
        ];

        const maxSize = 5 * 1024 * 1024;

        return (
            allowedTypes.includes(file.type) &&
            file.size <= maxSize
        );
    };

    // UPLOAD

    const handleFiles = async (files) => {

        if (!files || files.length === 0) {
            return;
        }

        for (const file of files) {

            if (!isValidFile(file)) {

                alert(
                    'Only JPG, PNG, GIF up to 5MB'
                );

                continue;
            }

            const formData = new FormData();

            formData.append(
                'image',
                file
            );

            try {

                const response = await fetch(
                    '/upload',
                    {
                        method: 'POST',
                        body: formData
                    }
                );

                const data =
                    await response.json();

                if (!response.ok) {

                    alert(
                        data.error ||
                        'Upload failed'
                    );

                    continue;
                }

                if (currentUploadInput) {
                    currentUploadInput.value =
                        data.full_url;
                }

                alert(
                    'Image uploaded successfully!'
                );

            } catch (error) {

                console.error(error);

                alert('Server error');
            }
        }
    };

    // COPY

    if (copyButton && currentUploadInput) {

        copyButton.addEventListener(
            'click',
            async () => {

                const text =
                    currentUploadInput.value;

                if (!text) {
                    return;
                }

                try {

                    await navigator.clipboard
                        .writeText(text);

                    copyButton.textContent =
                        'COPIED';

                    setTimeout(() => {

                        copyButton.textContent =
                            'COPY';

                    }, 1500);

                } catch (err) {

                    console.error(
                        'Copy failed:',
                        err
                    );
                }
            }
        );
    }

    // FILE INPUT

    if (fileUpload) {

        fileUpload.addEventListener(
            'change',
            (event) => {

                handleFiles(
                    event.target.files
                );

                fileUpload.value = '';
            }
        );
    }

    // DRAG AND DROP

    if (dropzone) {

        [
            'dragenter',
            'dragover',
            'dragleave',
            'drop'
        ].forEach(eventName => {

            dropzone.addEventListener(
                eventName,
                (e) => {

                    e.preventDefault();
                    e.stopPropagation();
                }
            );
        });

        dropzone.addEventListener(
            'drop',
            (event) => {

                handleFiles(
                    event.dataTransfer.files
                );
            }
        );
    }
});