const socket = io();

const messageBox = document.getElementById('messages');
const online = document.getElementById('online');
const input = document.getElementById('input');
const roomLabel = document.getElementById('room');

let nickname = localStorage.getItem('nickname') || '';
let roomId = window.ROOM_ID || 'public';

localStorage.setItem('room', roomId);

socket.on('connect', () => {
    socket.emit('join_room', {
        username: nickname || 'Guest',
        room_id: roomId
    });
});

socket.on('room_history', messages => {
    messageBox.innerHTML='';
    messages.forEach(m=>{
        addMessage(m.username,m.content);
    });
});

socket.on('new_message', data => {
    addMessage(data.username, data.content);
});

socket.on('system_message', data => {
    addMessage('系统', data.message);
});

socket.on('online_count', data => {
    if(online) online.textContent=data.count;
});

function addMessage(user,text){
    const div=document.createElement('div');
    div.className='message';
    div.textContent=user+': '+text;
    messageBox.appendChild(div);
    messageBox.scrollTop=messageBox.scrollHeight;
}

function sendMessage(){
    const text=input.value.trim();
    if(!text)return;

    socket.emit('send_message',{
        content:text
    });

    input.value='';
}

input.addEventListener('keydown',e=>{
    if(e.key==='Enter')sendMessage();
});
