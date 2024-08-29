const http = require('http');

const options = {
    hostname: 'localhost',
    port: 3000,
    path: '/saludo',
    method: 'GET'
}

const client = http.request(options, (res) => {
     console.log(`Codigo de estado: ${res.statusCode}`)
     res.setEncoding('utf8');
     
     res.on('data', (chunk) => {
        console.log(`Cuerpo: ${chunk}`);
     })

     res.on('end', () => {
        console.log('No hay mas datos en la respuesta.')
     })
})

client.on("error", (e) => {
    console.error(`Error en el cliente ${e.message}`)
})

client.end();

