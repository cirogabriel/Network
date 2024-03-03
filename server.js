const { Server } = require('net');

const HOST = 'localhost';
const PORT = 3000;
const END = 'END';


const error = (message) => {
  console.error(message);
  process.exit(1);
}

const listen = (port) => {
  const server = new Server();

  server.on('connection', (socket) => {
    const remoteSocket = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log('New connection from', remoteSocket);
    socket.setEncoding('utf-8');

    socket.on('data', (message) => {
      console.log(`${remoteSocket} -> ${message}`);
      socket.write(message);
      if (message === END) {
        socket.end();
      }
    });

    socket.on('close', () => {
      console.log(`Connection with ${remoteSocket} closed`);
    })
    
  });

  
  server.listen({ host: HOST, port: PORT }, () => {
    console.log('Listening on port', PORT);
  });


}

const main = () => {
  if (process.argv.length !== 3) {
    error(`Usage: node ${__filename} port`)
  }
  let port = process.argv[2];

  if (isNaN(port)) {
    error(`Invalid port ${port}`)
  }
  
  port = Number(port);

  listen(port);
}

if (require.main === module) {
  main();
}