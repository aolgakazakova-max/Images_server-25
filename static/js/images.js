document.addEventListener('DOMContentLoaded', () => {


    document.body.style.color = '#000';
    document.body.style.backgroundColor = '#f8f9fa';

    document.querySelectorAll('table, th, td, div, span, p, h1, h2, h3').forEach(el => {
        el.style.color = '#000';
    });

    document.querySelectorAll('a').forEach(a => {
        a.style.color = '#0d6efd';
    });



    const uploadTabBtn = document.getElementById('upload-tab-btn');
    const imagesTabBtn = document.getElementById('images-tab-btn');

    if (uploadTabBtn) {
        uploadTabBtn.addEventListener('click', () => {
            window.location.href = '/upload';
        });
    }

    if (imagesTabBtn) {
        imagesTabBtn.addEventListener('click', () => {
            window.location.href = '/images-list';
        });
    }


    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            window.location.href = '/upload';
        }
    });



    async function copyText(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {


            const textarea = document.createElement('textarea');
            textarea.value = text;
            document.body.appendChild(textarea);
            textarea.select();

            try {
                document.execCommand('copy');
                document.body.removeChild(textarea);
                return true;
            } catch (fallbackErr) {
                document.body.removeChild(textarea);
                console.error('Copy failed:', fallbackErr);
                return false;
            }
        }
    }

    document.querySelectorAll('.copy-btn').forEach(btn => {

        btn.addEventListener('click', async (e) => {

            const url = e.currentTarget.dataset.url;

            if (!url) return;

            const success = await copyText(url);

            if (success) {
                const oldText = e.currentTarget.textContent;
                e.currentTarget.textContent = 'Скопировано';

                setTimeout(() => {
                    e.currentTarget.textContent = oldText;
                }, 1200);
            }
        });
    });

});