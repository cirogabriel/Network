const { Socket } = require('net');
const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout
});

const END = 'END';

const socket = new Socket();

socket.connect({
    host: 'localhost',
    port: 3000
})
socket.setEncoding('utf-8');

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