# Flask Socket.IO Anonymous Chat Room

一个基于 Flask + Socket.IO 的匿名实时聊天室项目。

## 功能

- 匿名游客身份生成
- WebSocket 实时通信
- 多用户消息广播
- 用户加入/离开提示
- Docker 一键部署

## 技术栈

- Python 3.11
- Flask
- Flask-SocketIO
- Socket.IO
- Docker

## 本地运行

安装依赖：

```bash
pip install -r requirements.txt
```

启动：

```bash
python app.py
```

访问：

```
http://localhost:5000
```

## Docker 部署

构建镜像：

```bash
docker build -t anonymous-chat .
```

运行：

```bash
docker run -p 5000:5000 anonymous-chat
```

## 后续计划

- Redis 消息队列
- 用户昵称自定义
- 聊天记录存储
- 内容过滤
- HTTPS 部署
