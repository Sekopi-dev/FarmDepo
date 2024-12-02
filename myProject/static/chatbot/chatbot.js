// Toggle Chat Window Visibility
// Toggle Chat Window Visibility
function toggleChat() {
    const chatContainer = document.getElementById('chat-container');
    chatContainer.classList.toggle('open'); // Toggle open class
}

// Send Message Logic
function sendMessage() {
    const userInput = document.getElementById('user-input');
    const messageText = userInput.value.trim();

    if (messageText) {
        addMessage(messageText, 'user'); // Add user message to chat window
        userInput.value = ''; // Clear input field

        // Send message to server and get response
        fetch('chatbot_response', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({ message: messageText })
        })
        .then(response => response.json())
        .then(data => {
            if (data.response) {
                addMessage(data.response, 'bot'); // Add bot response
            }
        });
    }
}

// Add Message to Chat Window
function addMessage(message, sender) {
    const chatMessages = document.getElementById('chat-messages');
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', sender);
    messageDiv.textContent = message;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Scroll to bottom
}

// Handle Enter Key for Sending
function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

// Get CSRF Token
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
