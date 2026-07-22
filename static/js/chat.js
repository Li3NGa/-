const socket = io();

const messageBox = document.getElementById('messages');
const online = document.getElementById('online');
const input = document.getElementById('input');
const onlineUsers = document.getElementById('online-users');
const emojiPicker = document.getElementById('emoji-picker');
const emojiGrid = document.querySelector('.emoji-grid');

let nickname = localStorage.getItem('nickname') || '';
let roomId = window.ROOM_ID || 'public';
let myUuid = '';

localStorage.setItem('room', roomId);

socket.on('connect', () => {
    console.log('Connected to server');
});

socket.on('user_info', data => {
    nickname = data.username;
    myUuid = data.uuid;
    localStorage.setItem('nickname', nickname);
    
    socket.emit('join_room', {
        username: nickname,
        room_id: roomId
    });
});

socket.on('room_history', messages => {
    messageBox.innerHTML = '';
    messages.forEach(m => {
        addMessage(m.username, m.content, m.time, m.username === nickname);
    });
});

socket.on('new_message', data => {
    addMessage(data.username, data.content, new Date().toISOString(), data.username === nickname);
});

socket.on('system_message', data => {
    addSystemMessage(data.message);
});

socket.on('online_count', data => {
    if (online) online.textContent = data.count;
});

socket.on('online_users', users => {
    renderOnlineUsers(users);
});

function addMessage(user, text, timeStr, isOwn) {
    const div = document.createElement('div');
    div.className = 'message' + (isOwn ? ' own' : '');
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = user.charAt(0).toUpperCase();
    
    const content = document.createElement('div');
    content.className = 'message-content';
    
    const header = document.createElement('div');
    header.className = 'message-header';
    
    const username = document.createElement('span');
    username.className = 'message-username';
    username.textContent = user;
    
    const time = document.createElement('span');
    time.className = 'message-time';
    time.textContent = formatTime(timeStr);
    
    header.appendChild(username);
    header.appendChild(time);
    
    const messageText = document.createElement('div');
    messageText.className = 'message-text';
    messageText.textContent = text;
    
    content.appendChild(header);
    content.appendChild(messageText);
    
    div.appendChild(avatar);
    div.appendChild(content);
    
    messageBox.appendChild(div);
    messageBox.scrollTop = messageBox.scrollHeight;
}

function addSystemMessage(text) {
    const div = document.createElement('div');
    div.className = 'message system';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.textContent = '⚙️';
    
    const content = document.createElement('div');
    content.className = 'message-content';
    content.textContent = text;
    
    div.appendChild(avatar);
    div.appendChild(content);
    
    messageBox.appendChild(div);
    messageBox.scrollTop = messageBox.scrollHeight;
}

function formatTime(isoString) {
    const date = new Date(isoString);
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${hours}:${minutes}`;
}

function sendMessage() {
    const text = input.value.trim();
    if (!text) return;

    socket.emit('send_message', {
        content: text
    });

    input.value = '';
    emojiPicker.classList.remove('show');
}

function toggleEmojiPicker() {
    emojiPicker.classList.toggle('show');
}

function insertEmoji(emoji) {
    const start = input.selectionStart;
    const end = input.selectionEnd;
    const text = input.value;
    input.value = text.substring(0, start) + emoji + text.substring(end);
    input.selectionStart = input.selectionEnd = start + emoji.length;
    input.focus();
}

emojiGrid.innerHTML = emojiGrid.textContent.split(' ').map(e => 
    `<span onclick="insertEmoji('${e}')">${e}</span>`
).join('');

input.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

document.addEventListener('click', e => {
    if (!emojiPicker.contains(e.target) && !e.target.classList.contains('emoji-picker-btn')) {
        emojiPicker.classList.remove('show');
    }
});

function renderOnlineUsers(users) {
    onlineUsers.innerHTML = users.map(u => `
        <div class="user-item">
            <div class="user-avatar">${u.nickname.charAt(0).toUpperCase()}</div>
            <div class="user-name">${u.nickname}</div>
            <div class="user-status"></div>
        </div>
    `).join('');
}