const socket = new WebSocket('ws://localhost:8080');

socket.onmessage = ({ data }) => {
    console.log(data);
}

const btnMessage = document.querySelector('.btnMessage');

btnMessage.addEventListener('click', () => {
    socket.send('hola');
})

