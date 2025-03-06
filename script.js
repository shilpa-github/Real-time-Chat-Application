const socket = io();

const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message');

function sendMessage() {
    const message = messageInput.value;
    if (message) {
        const data = {
            username: username, // Use the username passed from Flask
            message: message
        };
        socket.emit('message', data);
        messageInput.value = '';
    }
}

function clearChat() {
    socket.emit('clear_chat'); // Notify the server to clear the chat
    chatMessages.innerHTML = ''; // Clear all messages from the frontend
}

messageInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        sendMessage();
    }
});

socket.on('message', (data) => {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message');
    if (data.username === username) {
        messageElement.classList.add('user');
    } else if (data.username === 'System') {
        messageElement.classList.add('system');
    } else {
        messageElement.classList.add('other');
    }
    messageElement.innerHTML = `<strong>${data.username}:</strong> ${data.message}`;
    chatMessages.appendChild(messageElement);
    chatMessages.scrollTop = chatMessages.scrollHeight;
});