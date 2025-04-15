document.addEventListener('DOMContentLoaded', () => {
    const messageInput = document.getElementById('userMessage');
    const sendButton = document.getElementById('sendButton');
    const micButton = document.getElementById('micButton');
    const chatMessages = document.getElementById('chat-messages');
    let recognition;

    // check if browser supports speech --> init if supported
    const isSpeechRecognitionSupported = () => {
        return 'webkitSpeechRecognition' in window || 'SpeechRecognition' in window;
    };
    if (isSpeechRecognitionSupported()) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';

        recognition.onstart = () => {
            document.getElementById('chat-input-container').classList.add('listening');
        };

        recognition.onend = () => {
            document.getElementById('chat-input-container').classList.remove('listening');
        };

        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            messageInput.value = transcript;
            sendMessage();
        };

        recognition.onerror = (event) => {
            console.error('Speech recognition error', event.error);
            displayMessage('System', 'Voice input failed. Please try again.');
        };

        micButton.addEventListener('click', () => {
            if (messageInput.value.trim()) {
                messageInput.value = '';
            }
            recognition.start();
        });
    } else {
        micButton.style.display = 'none';
    }

    // send
    async function sendMessage() {
        const message = messageInput.value.trim();
        if (message === '') return;

        displayMessage('You', message, 'user-message');
        messageInput.value = '';

        try {
            // typing indicator
            const typingIndicator = displayMessage('DOGUI', '...', 'ai-message', true);
            
            // send for response, wait for it
            const response = await fetch('/chatbot', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();
            
            // output message when recieved
            typingIndicator.querySelector('.message-content').textContent = data.response;
            
        } catch (error) {
            console.error('Error:', error);
            displayMessage('DOGUI', 'Error: Could not get response.', 'ai-message');
        }
    }

    // display message in chat
    function displayMessage(sender, message, messageClass = '', isTyping = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('message');
        if (messageClass) messageElement.classList.add(messageClass);
        
        messageElement.innerHTML = `
            <div class="message-avatar">${sender}</div>
            <div class="message-content">${message}</div>
        `;
        
        chatMessages.appendChild(messageElement);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return messageElement;
    }

    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});