document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('userMessage');
    const sendButton = document.getElementById('sendButton');
    const chatMessages = document.getElementById('chat-messages');

    // sending message
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });

    async function sendMessage() {
        const message = messageInput.value.trim();
        if (message === '') return;

        // display user message in the chat
        displayMessage('You', message);
        
        // clear the input field
        messageInput.value = '';

        try {
            // send message to backend
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            displayMessage('DOGUI AI', data.response);
        } catch (error) {
            console.error('Error:', error);
            displayMessage('DOGUI AI', 'Error: Could not get response.');
        }
    }

    // function to display messages in the chat
    function displayMessage(sender, message) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
        chatMessages.appendChild(messageElement);

        // auto scroll to the latest message
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
