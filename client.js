const { Socket } = require('net');
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

const END = 'END';

const error = (message) => {
    console.error(message);
    process.exit(1);
}


const connect = (host, port) => {
    console.log(`Connecting to ${host}:${port}`);

    const socket = new Socket();
    socket.connect({ host, port });
    socket.setEncoding('utf-8');

    socket.on('connect', () => {
        console.log('Connected');

        readline.on('line', (line) => {
            socket.write(line);
            if (line === END) {
                socket.end();
            }
        });

        socket.on('data', (data) => {
            console.log(data);
        });

        socket.on('close', () => {
            console.log('Connection closed');
            process.exit(0);
        })
        
    });
}



const main = () => {
    if (process.argv.lenth !== 4) 
        error(`Usage: node ${__filename} host port`)

    let [, , host, port] = process.argv;

    if (isNaN(port)) 
        error(`Invalid port ${port}`);

    port = Number(port);

    connect(host, port);
    
}

if (require.main === module) {
    main();
}