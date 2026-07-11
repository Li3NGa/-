const socket = io();

const messageBox = document.getElementById('messages');

socket.on('message', data => {
    addMessage(`${data.user}: ${data.text}`);
});

socket.on('system', msg => {
    addMessage(msg);
});

function addMessage(text) {
    const p = document.createElement('p');
    p.textContent = text;
    messageBox.appendChild(p);
    messageBox.scrollTop = messageBox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('input');
    const text = input.value.trim();
    if (text) {
        socket.emit('message', text);
        input.value = '';
    }
}
