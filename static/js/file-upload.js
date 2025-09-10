
document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.getElementById('migration-form');
    const analyzeBtn = document.getElementById('analyze-btn');
    const fileInput = document.getElementById('inventory-file');
    const resultsDiv = document.getElementById('results');
    const loadingDiv = document.getElementById('loading');
    const inventoryTableBody = document.querySelector('#inventory-table tbody');
    const importBtn = document.getElementById('import-btn');

    analyzeBtn.addEventListener('click', function () {
        if (!fileInput.files || fileInput.files.length === 0) {
            alert('Please select a file to analyze.');
            return;
        }

        const file = fileInput.files[0];
        const formData = new FormData();
        formData.append('file', file);

        // Show loading indicator
        loadingDiv.style.display = 'block';
        resultsDiv.style.display = 'none';

        // 1. Upload the file to a temporary file sharing service (e.g., file.io)
        fetch('https://file.io/?expires=1d', { // Link expires in 1 day
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (!data.success) {
                throw new Error(data.error || 'Failed to upload file to sharing service.');
            }
            // 2. Send the public URL to our backend for analysis
            return fetch('/migrate/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ file_url: data.link })
            });
        })
        .then(response => response.json())
        .then(data => {
            loadingDiv.style.display = 'none';

            if (data.error) {
                throw new Error(data.error);
            }

            // Clear previous results
            inventoryTableBody.innerHTML = '';

            // Populate the table with the new results
            const items = data.inventory_items || [];
            items.forEach(item => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td contenteditable="true">${item.name || ''}</td>
                    <td contenteditable="true" class="numeric">${item.quantity || ''}</td>
                    <td contenteditable="true">${item.sku || ''}</td>
                    <td contenteditable="true" class="numeric">${item.price || ''}</td>
                `;
                inventoryTableBody.appendChild(row);
            });

            resultsDiv.style.display = 'block';
        })
        .catch(error => {
            loadingDiv.style.display = 'none';
            alert(`An error occurred: ${error.message}`);
        });
    });

    importBtn.addEventListener('click', function () {
        const rows = inventoryTableBody.querySelectorAll('tr');
        const inventory_items = [];

        rows.forEach(row => {
            const cells = row.querySelectorAll('td');
            const item = {
                name: cells[0].innerText,
                quantity: parseInt(cells[1].innerText) || 0,
                sku: cells[2].innerText,
                price: parseFloat(cells[3].innerText) || 0.0
            };
            inventory_items.push(item);
        });

        fetch('/migrate/import', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ inventory_items })
        })
        .then(response => response.json())
        .then(data => {
            alert(data.message || "Import process completed.");
            if (data.status === 'success') {
                resultsDiv.style.display = 'none'; // Hide table after successful import
            }
        })
        .catch(error => {
            alert(`An error occurred during import: ${error.message}`);
        });
    });
});
