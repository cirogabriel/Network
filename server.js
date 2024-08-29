const { Server } = require('net');

const HOST = 'localhost';
const END = 'END';

const connection = new Map();


const error = (message) => {
  console.error(message);
  process.exit(1);
}

const sendMessage = (message, origin) => {
  for (const socket of connection.keys()) {
    if (socket !== origin) {
      socket.write(message);
    }
  }
}


const listen = (port) => {
  const server = new Server();

  server.on('connection', (socket) => {
    const remoteSocket = `${socket.remoteAddress}:${socket.remotePort}`;
    console.log('New connection from', remoteSocket);
    socket.setEncoding('utf-8');

    socket.on('data', (message) => {
      connection.values();

      if (!connection.has(socket)){
        console.log(`Username ${message} set for connection ${remoteSocket}`);
        connection.set(socket, message);
      } else if (message === END) {
        connection.delete(socket);
        socket.end();
      } else {
        const fullMessage = `[${connection.get(socket)}]: ${message}`;
        console.log(`${remoteSocket} -> ${fullMessage}`);
        sendMessage(fullMessage, socket);
      }
     
    });

    socket.on('error', (err) => {
      console.error(`Connection ${remoteSocket} -> ${err.message}`);
    });

    socket.on('close', () => {
      console.log(`Connection with ${remoteSocket} closed`);
    })
    
  });

  
  server.listen({ host: HOST, port: port }, () => {
    console.log('Listening on port', port);
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