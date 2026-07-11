const socket = io();

const messageBox = document.getElementById('messages');

socket.on('message', function(msg) {
    const p = document.createElement('p');
    p.textContent = msg;
    messageBox.appendChild(p);
});

function sendMessage() {
    const input = document.getElementById('input');
    if (input.value.trim()) {
        socket.send(input.value);
        input.value = '';
    }
}
