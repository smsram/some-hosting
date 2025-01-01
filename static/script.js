document.addEventListener('DOMContentLoaded', () => {
    const chatMessages = document.getElementById('chat-messages');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');

    // Function to add a message to the chat
    function addMessage(message, isUser) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', isUser ? 'user-message' : 'bot-message');
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to bottom
    }

    // Function to handle sending a message
    async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, true); // Add user message
    userInput.value = ''; // Clear input

    try {
        // Determine the backend URL (use window.location.origin in production)
        const backendUrl = window.location.origin + '/generate';  // This will adapt to production and local environments
        
        // Send request to backend
        const response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt: message }),
        });

        const data = await response.json();

        if (response.ok) {
            addMessage(data.reply, false); // Add bot reply
        } else {
            addMessage('Error: ' + (data.error || 'Something went wrong'), false);
        }
    } catch (error) {
        addMessage('Error: ' + error.message, false);
    }
}

    // Event listeners
    sendButton.addEventListener('click', sendMessage);
    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
});
