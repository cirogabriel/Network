const http = require('http');

const host = 'localhost'
const port = 3000

const requestListener = (req, res) => {
    if (req.url === '/saludo') {
        res.writeHead(200, {
            "Content-Type": "text/plain",
            "Access-Control-Allow-Origin": "*"
        })

        res.end('Saludo desde el servidor');
    } else {
        res.writeHead(404);
        res.end('Recurso no encontrado');
    }
}

const server = http.createServer(requestListener);

server.listen(port, host, () => {
    console.log(`El servidor se esta ejecutando en http://${host}:${port}`)
})