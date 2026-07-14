const socket = io();

const messageBox = document.getElementById('messages');
const online = document.getElementById('online');
const input = document.getElementById('input');
const roomLabel = document.getElementById('room');

let nickname = localStorage.getItem('nickname') || '';
let roomId = localStorage.getItem('room') || 'public';

socket.on('connect', () => {
    socket.emit('join_room', {
        username: nickname || 'Guest',
        room_id: roomId
    });
    socket.emit('get_online_users', {room_id: roomId});
});

socket.on('new_message', data => {
    addMessage(data.username || data.user, data.content || data.text);
});

socket.on('system_message', data => {
    addMessage('系统', data.message);
});

socket.on('online_count', data => {
    online.textContent = data.count;
});

function addMessage(user, text){
    const div=document.createElement('div');
    div.className='message';
    div.textContent=user+': '+text;
    messageBox.appendChild(div);
    messageBox.scrollTop=messageBox.scrollHeight;
}

function sendMessage(){
    const text=input.value.trim();
    if(text){
        socket.emit('send_message', {
            username:nickname || 'Guest',
            room_id:roomId,
            content:text
        });
        input.value='';
    }
}

function changeRoom(){
    const next=prompt('输入聊天室名称', roomId);
    if(next){
        roomId=next.substring(0,32);
        localStorage.setItem('room', roomId);
        roomLabel.textContent=roomId;
        messageBox.innerHTML='';
        socket.emit('join_room', {
            username:nickname || 'Guest',
            room_id:roomId
        });
    }
}

function changeNickname(){
    const name=prompt('输入昵称',nickname);
    if(name){
        nickname=name;
        localStorage.setItem('nickname',nickname);
    }
}

function addEmoji(e){input.value+=e;}

input.addEventListener('keydown',e=>{
    if(e.key==='Enter') sendMessage();
});
