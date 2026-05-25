document.addEventListener('DOMContentLoaded', () => {

    // NAV
    const uploadTabBtn = document.getElementById('upload-tab-btn');
    const imagesTabBtn = document.getElementById('images-tab-btn');

    if (uploadTabBtn) {
        uploadTabBtn.addEventListener('click', () => {
            window.location.href = '/upload';
        });
    }

    if (imagesTabBtn) {
        imagesTabBtn.addEventListener('click', () => {
            window.location.href = '/images/';
        });
    }

    // ESC
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            window.location.href = '/upload';
        }
    });

    // COPY (оставь как есть)
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', async (e) => {

            const url = e.currentTarget.dataset.url;

            try {
                await navigator.clipboard.writeText(url);

                const oldText = e.currentTarget.textContent;
                e.currentTarget.textContent = 'COPIED';

                setTimeout(() => {
                    e.currentTarget.textContent = oldText;
                }, 1200);

            } catch (err) {
                console.error('Copy failed:', err);
            }

        });
    });

    // ✅ DELETE (ИСПРАВЛЕНО — EVENT DELEGATION)
    document.addEventListener('click', async (e) => {

        const btn = e.target.closest('.delete-btn');
        if (!btn) return;

        const filename = btn.dataset.filename;

        try {
            const response = await fetch(`/delete/${filename}`, {
                method: 'POST'
            });

            const data = await response.json();

            if (!response.ok) {
                alert(data.error || 'Delete failed');
                return;
            }

            const item = btn.closest('.file-list-item');
            if (item) item.remove();

        } catch (err) {
            console.error('Delete error:', err);
        }

    });

});