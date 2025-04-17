document.addEventListener('DOMContentLoaded', function() {
    const projectId = {{ project.id }};
    const addAssetBtn = document.getElementById('add-asset-btn');
    const assetSelector = document.getElementById('asset-selector');
    const availableAssets = document.getElementById('available-assets');
    const confirmAddBtn = document.getElementById('confirm-add-asset');
    const cancelAddBtn = document.getElementById('cancel-add-asset');
    
    // Toggle asset selector
    addAssetBtn.addEventListener('click', function() {
        assetSelector.style.display = assetSelector.style.display === 'none' ? 'block' : 'none';
    });
    
    cancelAddBtn.addEventListener('click', function() {
        assetSelector.style.display = 'none';
        availableAssets.value = '';
    });
    
    // Add asset to project
    confirmAddBtn.addEventListener('click', async function() {
        const assetId = availableAssets.value;
        if (!assetId) return;
        
        try {
            const response = await fetch(`/project/${projectId}/add-asset/${assetId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                const newAsset = await response.json();
                addAssetToUI(newAsset);
                assetSelector.style.display = 'none';
                availableAssets.value = '';
            } else {
                alert('Error adding asset');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Failed to add asset');
        }
    });
    
    // Remove asset from project
    document.querySelectorAll('.remove-asset-btn').forEach(btn => {
        btn.addEventListener('click', async function() {
            const assetId = this.dataset.assetId;
            if (confirm('Remove this asset from the project?')) {
                try {
                    const response = await fetch(`/project/${projectId}/remove-asset/${assetId}`, {
                        method: 'DELETE'
                    });
                    
                    if (response.ok) {
                        this.closest('.asset-card').remove();
                    } else {
                        alert('Error removing asset');
                    }
                } catch (error) {
                    console.error('Error:', error);
                    alert('Failed to remove asset');
                }
            }
        });
    });
    
    // Helper function to add new asset to UI
    function addAssetToUI(asset) {
        const assetsGrid = document.querySelector('.assets-grid');
        const assetCard = document.createElement('div');
        assetCard.className = 'asset-card glow';
        assetCard.innerHTML = `
            <div class="asset-icon">
                ${asset.type === 'image' ? 
                    `<img src="/static/assets/images/${asset.filename}" alt="${asset.name}">` : 
                    asset.type === 'model' ? 
                    `<img src="/static/img/navicons/cube.png" alt="3D Model">` :
                    `<img src="/static/img/navicons/drawing.png" alt="CAD Drawing">`}
            </div>
            <div class="asset-info">
                <h3>${asset.name}</h3>
                <span class="asset-type ${asset.type}">${asset.type.charAt(0).toUpperCase() + asset.type.slice(1)}</span>
            </div>
            <div class="asset-actions">
                <a href="/asset/download/${asset.type}/${asset.filename}" 
                   class="download-btn" title="Download ${asset.name}">
                    <img src="/static/img/navicons/download.png" alt="Download">
                </a>
                <button class="remove-asset-btn" data-asset-id="${asset.id}" title="Remove from project">
                    <img src="/static/img/navicons/trash.png" alt="Remove">
                </button>
            </div>
        `;
        
        // Insert before the "Add Asset" card
        assetsGrid.insertBefore(assetCard, addAssetBtn.parentNode);
        
        // Add event listener to new remove button
        assetCard.querySelector('.remove-asset-btn').addEventListener('click', function() {
            if (confirm('Remove this asset from the project?')) {
                fetch(`/project/${projectId}/remove-asset/${asset.id}`, {
                    method: 'DELETE'
                }).then(response => {
                    if (response.ok) {
                        assetCard.remove();
                    }
                });
            }
        });
    }
});