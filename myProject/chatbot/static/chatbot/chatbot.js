function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const chatLog = document.getElementById('chat-log');

    if (userInput.trim() !== "") {
        // Add user message to chat log
        chatLog.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;

        // Send user message to the Django view
        fetch('/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': getCookie('csrftoken'),
            },
            body: `message=${encodeURIComponent(userInput)}`
        })
        .then(response => response.json())
        .then(data => {
            // Add bot response to chat log
            chatLog.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
        });
    }
}

// Get CSRF token for POST requests
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
