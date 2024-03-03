const { Server } = require('net');

const server = new Server();

/**
 * 
 * 
 */
server.on('connection', (socket) => {
    const remoteSocket = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log(`New connection from ${remoteSocket}`);
    socket.setEncoding('utf-8');
    socket.on('data', (data) => {
        console.log(data);
        socket.write(data);
    })
})


server.listen({
    port: 3000,
    host: 'localhost',
}, () => {
    console.log('Server is running at http://localhost:3000');
})