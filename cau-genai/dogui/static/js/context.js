document.getElementById('add-context-form')?.addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData(this);
    const response = await fetch(this.action, {
        method: 'POST',
        body: formData
    });
    
    if (response.ok) {
        const newContext = await response.json();
        addContextToUI(newContext);
        this.reset();
    } else {
        alert('Error adding context');
    }
});

function addContextToUI(context) {
    const contextItem = document.createElement('div');
    contextItem.className = 'context-item';
    contextItem.dataset.contextId = context.id;
    contextItem.innerHTML = `
        <div class="context-text">${context.text}</div>
        <div class="context-actions">
            <button class="btn-edit-context">Edit</button>
        </div>
    `;
    
    document.querySelector('.context-list').appendChild(contextItem);
    addContextEventListeners(contextItem);
}

function addContextEventListeners(item) {
    item.querySelector('.btn-edit-context').addEventListener('click', () => {
        editContext(item);
    });
    
    item.querySelector('.btn-delete-context').addEventListener('click', () => {
        deleteContext(item);
    });
}


function editContext(item) {
    const textElement = item.querySelector('.context-text');
    const originalText = textElement.textContent;
    
    textElement.innerHTML = `
        <textarea class="context-edit">${originalText}</textarea>
        <button class="btn-save-edit">Save</button>
        <button class="btn-cancel-edit">Cancel</button>
    `;
    
    textElement.querySelector('.btn-save-edit').addEventListener('click', async () => {
        const newText = textElement.querySelector('textarea').value;
        const response = await fetch(`/update-context/${item.dataset.contextId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: newText })
        });
        
        if (response.ok) {
            textElement.textContent = newText;
        }
    });
    
    textElement.querySelector('.btn-cancel-edit').addEventListener('click', () => {
        textElement.textContent = originalText;
    });
}

document.querySelectorAll('.context-item').forEach(addContextEventListeners);