const Websocket = require('ws');
const server = new Websocket.Server({ port: 8080 });

server.on('connection', socket => {
    socket.on('message', message => {
        socket.send(`You said: ${message}`);
    });
})