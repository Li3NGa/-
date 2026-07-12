const socket = io();

const messageBox = document.getElementById('messages');
const online = document.getElementById('online');
const input = document.getElementById('input');

let nickname = localStorage.getItem('nickname') || '';

socket.on('connect', () => {
    if (nickname) {
        socket.emit('set_nickname', nickname);
    }
});

socket.on('message', data => {
    addMessage(data.user, data.text);
});

socket.on('system', msg => {
    addMessage('系统', msg);
});

socket.on('online_count', data => {
    if (online) online.textContent = data.count;
});

function addMessage(user, text) {
    const div = document.createElement('div');
    div.className = 'message';
    div.textContent = user + ': ' + text;
    messageBox.appendChild(div);
    messageBox.scrollTop = messageBox.scrollHeight;
}

function sendMessage(){
    const text=input.value.trim();
    if(text){
        socket.emit('message',text);
        input.value='';
    }
}

function changeNickname(){
    const name=prompt('输入新昵称',nickname);
    if(name){
        nickname=name.substring(0,16);
        localStorage.setItem('nickname',nickname);
        socket.emit('set_nickname',nickname);
    }
}

function addEmoji(e){
    input.value += e;
}

input.addEventListener('keydown',e=>{
    if(e.key==='Enter') sendMessage();
});
