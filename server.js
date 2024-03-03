import Server from 'net';

const HOST = 'localhost';
const PORT = 3000;
const END = 'END';

const listen = (port) => {
  const server = new Server();

  server.on('connection', (socket) => {
    const remoteSocket = `${socket.remoteAdress}:${socket.remoteSocket}`;
    console.log('New connection from', remoteSocket);
    socket.setEncoding('utf-8');

    socket.on('data', (message) => {
      pass
    })
  }
}


