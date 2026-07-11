const socket = io();

let username = '';
const roomId = 'main';
const messageBox = document.getElementById('messages');

socket.on('user_info', data => {
    username = data.username;
    document.getElementById('username').textContent = username;

    socket.emit('join_room', {
        username,
        room_id: roomId
    });

    socket.emit('get_online_users', {
        room_id: roomId
    });
});

socket.on('new_message', msg => {
    addMessage(`${msg.username}: ${msg.content}`);
});

socket.on('system_message', data => {
    addMessage(data.message);
});

socket.on('online_count', data => {
    document.getElementById('online').textContent = data.count;
});

function addMessage(text) {
    const p = document.createElement('p');
    p.className = 'message';
    p.textContent = text;
    messageBox.appendChild(p);
    messageBox.scrollTop = messageBox.scrollHeight;
}

function sendMessage() {
    const input = document.getElementById('input');

    if (input.value.trim()) {
        socket.emit('send_message', {
            username,
            room_id: roomId,
            content: input.value
        });
        input.value = '';
    }
}
