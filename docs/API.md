# Socket.IO API

## Events

### connect
创建匿名用户身份。

### join_room
```json
{
  "username": "BlueFox",
  "room_id": "main"
}
```

### send_message
```json
{
  "username": "BlueFox",
  "room_id": "main",
  "content": "hello"
}
```

### get_online_users
返回当前房间在线人数。
