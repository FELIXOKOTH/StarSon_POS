document.addEventListener('DOMContentLoaded', () => {
    const inventoryForm = document.getElementById('inventoryForm');
    const imageFile = document.getElementById('imageFile');
    const resultsDiv = document.getElementById('results');

    inventoryForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const formData = new FormData();
        formData.append('image', imageFile.files[0]);

        try {
            const response = await fetch('http://localhost:8080/api/analyze_image', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const inventory = await response.json();
                resultsDiv.innerHTML = `<pre>${JSON.stringify(inventory, null, 2)}</pre>`;
            } else {
                resultsDiv.innerHTML = `<p>Error: ${response.statusText}</p>`;
            }
        } catch (error) {
            resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
        }
    });
});
